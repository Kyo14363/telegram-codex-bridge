"""Small smoke tests that avoid network, Telegram, and live Codex calls."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bridge_core import CodexBridge
from config import CONFIG
from url_fetchers import detect_urls


class SmokeTests(unittest.TestCase):
    def test_detect_github_url(self) -> None:
        urls = detect_urls("please inspect https://github.com/openai/openai-python")
        self.assertTrue(urls)
        self.assertEqual(urls[0][1], "github")

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


if __name__ == "__main__":
    unittest.main()
