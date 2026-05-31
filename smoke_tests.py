"""Small smoke tests that avoid network, Telegram, and live Codex calls."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bridge_core import CodexBridge
from config import BASE_DIR, CONFIG, resolve_path
from url_fetchers import detect_urls


class SmokeTests(unittest.TestCase):
    def test_detect_github_url(self) -> None:
        urls = detect_urls("please inspect https://github.com/openai/openai-python")
        self.assertTrue(urls)
        self.assertEqual(urls[0][1], "github")

    def test_relative_paths_resolve_from_repo_root(self) -> None:
        self.assertEqual(resolve_path(".\\workspace"), (BASE_DIR / "workspace").resolve())

    def test_default_command_does_not_enable_full_auto(self) -> None:
        bridge = CodexBridge()
        with tempfile.TemporaryDirectory() as tmp:
            old_working_dir = CONFIG["WORKING_DIR"]
            old_search = CONFIG["CODEX_SEARCH"]
            old_full_auto = CONFIG["CODEX_FULL_AUTO"]
            old_model = CONFIG["CODEX_MODEL"]
            try:
                CONFIG["WORKING_DIR"] = Path(tmp)
                CONFIG["CODEX_SEARCH"] = False
                CONFIG["CODEX_FULL_AUTO"] = False
                CONFIG["CODEX_MODEL"] = ""
                cmd = bridge.codex_command(Path(tmp) / "out.txt", codex_executable="codex")
            finally:
                CONFIG["WORKING_DIR"] = old_working_dir
                CONFIG["CODEX_SEARCH"] = old_search
                CONFIG["CODEX_FULL_AUTO"] = old_full_auto
                CONFIG["CODEX_MODEL"] = old_model

        self.assertNotIn("--full-auto", cmd)
        self.assertNotIn("--search", cmd)
        self.assertNotIn("-m", cmd)
        self.assertIn("--skip-git-repo-check", cmd)

    def test_build_codex_command_with_fake_executable(self) -> None:
        bridge = CodexBridge()
        with tempfile.TemporaryDirectory() as tmp:
            old_working_dir = CONFIG["WORKING_DIR"]
            old_extra_dirs = CONFIG["CODEX_EXTRA_DIRS"]
            old_model = CONFIG["CODEX_MODEL"]
            old_search = CONFIG["CODEX_SEARCH"]
            old_full_auto = CONFIG["CODEX_FULL_AUTO"]
            try:
                CONFIG["WORKING_DIR"] = Path(tmp)
                CONFIG["CODEX_EXTRA_DIRS"] = [str(Path(tmp) / "extra")]
                CONFIG["CODEX_MODEL"] = "test-model"
                CONFIG["CODEX_SEARCH"] = True
                CONFIG["CODEX_FULL_AUTO"] = True
                cmd = bridge.codex_command(Path(tmp) / "out.txt", codex_executable="codex")
            finally:
                CONFIG["WORKING_DIR"] = old_working_dir
                CONFIG["CODEX_EXTRA_DIRS"] = old_extra_dirs
                CONFIG["CODEX_MODEL"] = old_model
                CONFIG["CODEX_SEARCH"] = old_search
                CONFIG["CODEX_FULL_AUTO"] = old_full_auto

        self.assertEqual(cmd[0], "codex")
        self.assertIn("--search", cmd)
        self.assertIn("exec", cmd)
        self.assertIn("--json", cmd)
        self.assertIn("--full-auto", cmd)
        self.assertIn("-m", cmd)
        self.assertEqual(cmd[-1], "-")

    def test_prompt_with_url_includes_browser_hint(self) -> None:
        bridge = CodexBridge()
        original = "Review https://github.com/openai/openai-python for maintainer signals"
        detected_urls = detect_urls(original)
        prompt = bridge._build_codex_prompt(original, original, detected_urls)
        self.assertIn("URL handling note", prompt)
        self.assertIn("fetched URL content", prompt)
        self.assertIn(original, prompt)

    def test_codex_event_summaries(self) -> None:
        bridge = CodexBridge()
        self.assertEqual(
            bridge._summarize_event('{"type":"turn.started"}'),
            "Codex started the task.",
        )
        self.assertEqual(
            bridge._summarize_event('{"type":"turn.completed"}'),
            "Codex completed the task.",
        )
        tool_summary = bridge._summarize_event('{"type":"tool.call","name":"shell"}')
        self.assertEqual(tool_summary, "Codex is using a tool: shell")

    def test_authorization_allowlist(self) -> None:
        bridge = CodexBridge()
        old_allowed = CONFIG["ALLOWED_USER_IDS"]
        try:
            CONFIG["ALLOWED_USER_IDS"] = [123]
            self.assertTrue(bridge.is_authorized(123))
            self.assertFalse(bridge.is_authorized(456))
            CONFIG["ALLOWED_USER_IDS"] = []
            self.assertTrue(bridge.is_authorized(456))
        finally:
            CONFIG["ALLOWED_USER_IDS"] = old_allowed

    def test_format_output_strips_ansi_and_truncates(self) -> None:
        bridge = CodexBridge()
        old_max = CONFIG["OUTPUT_MAX_CHARS"]
        try:
            CONFIG["OUTPUT_MAX_CHARS"] = 10
            formatted = bridge._format_output("\x1b[31mABCDEFGHIJKLMNO\x1b[0m")
        finally:
            CONFIG["OUTPUT_MAX_CHARS"] = old_max

        self.assertNotIn("\x1b[31m", formatted)
        self.assertIn("ABCDEFGHIJ", formatted)
        self.assertIn("truncated by Telegram Codex Bridge", formatted)

    def test_stderr_noise_filter_keeps_real_errors(self) -> None:
        bridge = CodexBridge()
        self.assertTrue(
            bridge._is_stderr_noise(
                "WARN codex_core::plugins::manager: failed to warm featured plugin ids cache"
            )
        )
        self.assertTrue(bridge._is_stderr_noise("<script>window._cf_chl_opt={}</script>"))
        self.assertFalse(bridge._is_stderr_noise("Error: system cannot find the file specified"))

    def test_prompt_templates_are_present_and_bounded(self) -> None:
        prompt_dir = BASE_DIR / "prompts"
        expected = {
            "issue-triage.md",
            "pr-review.md",
            "release-checklist.md",
            "ci-failure-triage.md",
            "repo-context-review.md",
        }
        existing = {path.name for path in prompt_dir.glob("*.md")}
        self.assertTrue(expected.issubset(existing))

        for path in prompt_dir.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("```text", text)
            self.assertIn("Do not", text)
            self.assertLess(len(text), 1400)


if __name__ == "__main__":
    unittest.main()
