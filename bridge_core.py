"""Codex CLI task runner used by the Telegram handlers."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from config import CONFIG, VERSION_LABEL
from metrics import Metrics
from url_fetchers import detect_urls, preprocess_urls, save_fetch_output


logger = logging.getLogger(__name__)


@dataclass
class TaskState:
    process: Optional[asyncio.subprocess.Process] = None
    started_at: Optional[float] = None
    prompt_preview: str = ""
    run_id: str = ""
    last_event: str = ""
    last_output_path: Optional[Path] = None
    event_counts: Dict[str, int] = field(default_factory=dict)


class CodexBridge:
    def __init__(self) -> None:
        self.metrics = Metrics(CONFIG["STATS_FILE"])
        self.state = TaskState()
        self._lock = asyncio.Lock()

    def is_authorized(self, user_id: int) -> bool:
        allowed = CONFIG["ALLOWED_USER_IDS"]
        return not allowed or user_id in allowed

    def status_text(self) -> str:
        busy = self.state.process is not None and self.state.process.returncode is None
        extra = "; ".join(CONFIG["CODEX_EXTRA_DIRS"]) or "(none)"
        if busy and self.state.started_at:
            elapsed = int(time.monotonic() - self.state.started_at)
            task = (
                f"running for {elapsed}s\n"
                f"- run: {self.state.run_id}\n"
                f"- current: {self.state.last_event or '(waiting for first event)'}"
            )
        else:
            task = "idle"
        return (
            f"{VERSION_LABEL}\n"
            f"- task: {task}\n"
            f"- cwd: {CONFIG['WORKING_DIR']}\n"
            f"- extra dirs: {extra}\n"
            f"- model: {CONFIG['CODEX_MODEL'] or '(codex default)'}\n"
            f"- search: {'on' if CONFIG['CODEX_SEARCH'] else 'off'}\n"
            f"- full auto: {'on' if CONFIG['CODEX_FULL_AUTO'] else 'off'}"
        )

    async def cancel_current(self) -> str:
        proc = self.state.process
        if not proc or proc.returncode is not None:
            self.state = TaskState()
            return "No active Codex task. Cleared bridge task state."

        pid = proc.pid
        logger.info("[cancel] stopping codex process tree pid=%s", pid)
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True, timeout=10)
            else:
                proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=10)
            except asyncio.TimeoutError:
                proc.kill()
        except Exception as exc:
            logger.warning("[cancel] failed: %s", exc)
            self.metrics.record_error("cancel", exc)
            return f"Failed to cancel task: {exc}"
        finally:
            self.state = TaskState()
        return "Stopped the active Codex task and cleared bridge task state."

    async def run_user_message(self, text: str, progress_cb=None) -> Tuple[str, Optional[str]]:
        if self._lock.locked():
            return "Codex is already running a task. Use /cancel to stop it first.", None

        async with self._lock:
            self.metrics.record_message()
            preprocessed = await preprocess_urls(text, config=CONFIG, metrics=self.metrics)
            if len(preprocessed) == 3:
                enhanced_text, url_summaries, _obsidian_queue = preprocessed
            else:
                enhanced_text, url_summaries = preprocessed
            url_status = "\n".join(url_summaries) if url_summaries else None

            detected_urls = detect_urls(text)
            prompt = self._build_codex_prompt(text, enhanced_text, detected_urls)
            response = await self._run_codex(prompt, progress_cb=progress_cb)

            if detected_urls:
                try:
                    first_url = detected_urls[0][0]
                    user_note = text.replace(first_url, "").strip()
                    await asyncio.get_running_loop().run_in_executor(
                        None,
                        save_fetch_output,
                        first_url,
                        enhanced_text,
                        response,
                        user_note,
                        CONFIG,
                    )
                except Exception as exc:
                    logger.warning("[fetch_output] save failed: %s", exc)
            return response, url_status

    def _build_codex_prompt(self, original_text: str, enhanced_text: str, detected_urls: List[Tuple[str, str]]) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        url_hint = ""
        if detected_urls:
            url_hint = (
                "\n\nURL handling note:\n"
                "- The bridge may have included fetched URL content below.\n"
                "- If the content looks thin or dynamic, use Codex's available browser/computer tools only when present.\n"
                "- Cite or name sources when you rely on fetched content.\n"
            )
        return (
            "You are running inside Telegram Codex Bridge, a self-hosted bridge that forwards a "
            "Telegram message to a local Codex CLI task.\n\n"
            "## User message\n"
            f"{original_text}\n\n"
            "## Runtime guidance\n"
            f"- Current local time: {now}\n"
            "- Default response language: match the user's language.\n"
            "- Be concise but complete.\n"
            "- If you inspect or modify local files, mention exact paths.\n"
            "- Treat this as a maintainer workflow: prefer bounded, reviewable actions.\n"
            "- Do not request interactive terminal approval; choose safe actions or explain the blocker.\n"
            f"{url_hint}\n"
            "## Bridge-preprocessed instruction/content\n"
            f"{enhanced_text}"
        )

    async def _run_codex(self, prompt: str, progress_cb=None) -> str:
        CONFIG["RUN_DIR"].mkdir(parents=True, exist_ok=True)
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = CONFIG["RUN_DIR"] / f"codex-last-{run_id}.txt"
        prompt_path = CONFIG["RUN_DIR"] / f"codex-prompt-{run_id}.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        self.state = TaskState(
            started_at=time.monotonic(),
            prompt_preview=prompt[:120],
            run_id=run_id,
            last_output_path=output_path,
        )

        cmd = self.codex_command(output_path)
        logger.info("[codex] start run=%s cmd=%s", run_id, self._redact_cmd(cmd))
        start = time.monotonic()
        ok = False
        stderr_tail: List[str] = []

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(CONFIG["WORKING_DIR"]),
            )
            self.state.process = proc
            if proc.stdin:
                proc.stdin.write(prompt.encode("utf-8"))
                await proc.stdin.drain()
                proc.stdin.close()
                try:
                    await proc.stdin.wait_closed()
                except Exception:
                    pass

            await asyncio.wait_for(
                self._consume_codex(proc, progress_cb, stderr_tail),
                timeout=CONFIG["CODEX_TIMEOUT"],
            )
            rc = await proc.wait()
            ok = rc == 0
            if not ok:
                self.metrics.record_error("codex", f"exit code {rc}; stderr={self._tail_text(stderr_tail)}")
        except asyncio.TimeoutError:
            self.metrics.record_error("codex", f"timeout after {CONFIG['CODEX_TIMEOUT']}s")
            await self.cancel_current()
            return f"Codex task timed out after {CONFIG['CODEX_TIMEOUT']} seconds."
        except Exception as exc:
            self.metrics.record_error("codex", exc)
            logger.exception("[codex] run failed")
            return f"Codex task failed: {type(exc).__name__}: {exc}"
        finally:
            self.metrics.record_codex_call(time.monotonic() - start, ok)
            self.state.process = None

        result = output_path.read_text(encoding="utf-8", errors="replace").strip() if output_path.exists() else ""
        if not result:
            result = "(Codex produced no final output.)"
        if not ok:
            result += "\n\n---\nCodex process returned a non-zero exit code."
            tail = self._tail_text(stderr_tail)
            if tail:
                result += f"\n\nstderr tail:\n{tail}"
        return self._format_output(result)

    def codex_command(self, output_path: Path, codex_executable: str | None = None) -> List[str]:
        codex = codex_executable or shutil.which("codex")
        if not codex:
            raise RuntimeError("codex CLI was not found in PATH.")

        if codex.lower().endswith(".ps1"):
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", codex]
        else:
            cmd = [codex]

        if CONFIG["CODEX_SEARCH"]:
            cmd.append("--search")

        cmd.extend(["exec", "--json"])
        if CONFIG["CODEX_SKIP_GIT_REPO_CHECK"]:
            cmd.append("--skip-git-repo-check")
        if CONFIG["CODEX_FULL_AUTO"]:
            cmd.append("--full-auto")
        cmd.extend(["-C", str(CONFIG["WORKING_DIR"]), "-o", str(output_path)])
        if CONFIG["CODEX_MODEL"]:
            cmd.extend(["-m", CONFIG["CODEX_MODEL"]])
        for extra_dir in CONFIG["CODEX_EXTRA_DIRS"]:
            cmd.extend(["--add-dir", extra_dir])
        cmd.append("-")
        return cmd

    async def _consume_codex(self, proc, progress_cb, stderr_tail: List[str]) -> None:
        async def read_stdout() -> None:
            assert proc.stdout
            while True:
                raw = await proc.stdout.readline()
                if not raw:
                    break
                line = raw.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                summary = self._summarize_event(line)
                if summary:
                    self.state.last_event = summary
                    if progress_cb:
                        await progress_cb(summary)

        async def read_stderr() -> None:
            assert proc.stderr
            while True:
                raw = await proc.stderr.readline()
                if not raw:
                    break
                line = raw.decode("utf-8", errors="replace").strip()
                if line:
                    if self._is_stderr_noise(line):
                        logger.debug("[codex stderr ignored] %s", line[:500])
                    else:
                        stderr_tail.append(line[:1000])
                        del stderr_tail[:-20]
                        logger.warning("[codex stderr] %s", line[:1000])

        await asyncio.gather(read_stdout(), read_stderr())

    def _summarize_event(self, line: str) -> Optional[str]:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            logger.info("[codex] %s", line[:300])
            return None

        event_type = str(event.get("type") or event.get("event") or "")
        self.state.event_counts[event_type] = self.state.event_counts.get(event_type, 0) + 1

        blob = json.dumps(event, ensure_ascii=False)
        lower_blob = blob.lower()
        lower_type = event_type.lower()
        if "turn.started" in lower_type:
            return "Codex started the task."
        if "turn.completed" in lower_type:
            return "Codex completed the task."
        if "error" in lower_type:
            return f"Codex reported an error event: {event_type}"
        if "plan" in lower_blob:
            return "Codex is planning the task."
        if "command" in lower_blob or "exec" in lower_blob:
            cmd = self._extract_field(event, ("command", "cmd", "shell_command"))
            return f"Codex is running a local command: {cmd[:160] if cmd else 'local command'}"
        if "mcp" in lower_blob or "tool" in lower_blob:
            name = self._extract_field(event, ("name", "tool_name", "server_label"))
            return f"Codex is using a tool: {name or event_type or 'tool'}"
        if self.state.event_counts[event_type] == 1 and event_type:
            return f"Codex event: {event_type}"
        return None

    def _extract_field(self, value: Any, keys: Tuple[str, ...]) -> Optional[str]:
        if isinstance(value, dict):
            for key in keys:
                if key in value and isinstance(value[key], str):
                    return value[key]
            for child in value.values():
                found = self._extract_field(child, keys)
                if found:
                    return found
        elif isinstance(value, list):
            for item in value:
                found = self._extract_field(item, keys)
                if found:
                    return found
        return None

    def _format_output(self, text: str) -> str:
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        text = ansi_escape.sub("", text)
        max_chars = CONFIG["OUTPUT_MAX_CHARS"]
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n...(truncated by Telegram Codex Bridge)"
        return text

    def _tail_text(self, lines: List[str]) -> str:
        return "\n".join(lines[-12:])

    def _is_stderr_noise(self, line: str) -> bool:
        noise_patterns = (
            "WARN codex_core::plugins::manager: failed to warm featured plugin ids cache",
            "WARN codex_core::plugins::startup_sync: startup remote plugin sync failed",
            "WARN codex_core::plugins::manifest: ignoring interface.defaultPrompt",
            "WARN codex_core::plugins::manager: failed to refresh curated plugin cache",
            "WARN codex_protocol::openai_models: Model personality requested",
            "WARN codex_core::shell_snapshot: Failed to create shell snapshot for powershell",
            "Reading additional input from stdin",
            "Enable JavaScript and cookies to continue",
            "window._cf_chl_opt",
            "/cdn-cgi/challenge-platform/",
        )
        stripped = line.strip()
        if stripped.startswith(("<style", "<svg", "<path", "<div", "<script", "</", "xmlns=", "fill=", "strokeWidth=")):
            return True
        return any(pattern in line for pattern in noise_patterns)

    def _redact_cmd(self, cmd: List[str]) -> str:
        safe = cmd[:]
        if safe and safe[-1] == "-":
            safe[-1] = "<stdin-prompt>"
        return " ".join(safe)
