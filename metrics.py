"""Lightweight file-backed runtime metrics."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


logger = logging.getLogger(__name__)


class Metrics:
    def __init__(self, stats_file: Path):
        self.stats_file = stats_file
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            if self.stats_file.exists():
                return json.loads(self.stats_file.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("[metrics] failed to load stats: %s", exc)
        return {
            "since": datetime.now().strftime("%Y-%m-%d"),
            "totals": {
                "messages": 0,
                "codex_calls": 0,
                "codex_errors": 0,
                "fetch_success": 0,
                "fetch_fail": 0,
            },
            "timing": {"codex_total_sec": 0.0, "codex_count": 0},
            "recent_errors": [],
        }

    def _save(self) -> None:
        try:
            self.stats_file.parent.mkdir(parents=True, exist_ok=True)
            self.stats_file.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            logger.warning("[metrics] failed to save stats: %s", exc)

    def record_message(self) -> None:
        self._data["totals"]["messages"] += 1
        self._save()

    def record_codex_call(self, duration_sec: float, success: bool) -> None:
        self._data["totals"]["codex_calls"] += 1
        if not success:
            self._data["totals"]["codex_errors"] += 1
        self._data["timing"]["codex_total_sec"] += duration_sec
        self._data["timing"]["codex_count"] += 1
        self._save()

    def record_fetch(self, url: str, platform: str, method: str, success: bool, duration_sec: float) -> None:
        key = "fetch_success" if success else "fetch_fail"
        self._data["totals"][key] += 1
        self._save()

    def record_error(self, context: str, error_msg: object) -> None:
        self._data["recent_errors"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "context": context,
            "error": str(error_msg)[:500],
        })
        self._data["recent_errors"] = self._data["recent_errors"][-20:]
        self._save()

    def summary(self) -> str:
        totals = self._data["totals"]
        timing = self._data["timing"]
        total_fetch = totals["fetch_success"] + totals["fetch_fail"]
        fetch_rate = (totals["fetch_success"] / total_fetch * 100) if total_fetch else 0.0
        avg = (timing["codex_total_sec"] / timing["codex_count"]) if timing["codex_count"] else 0.0
        recent = self._data.get("recent_errors", [])[-5:]
        err_lines = "\n".join(f"- {e['time']} {e['context']}: {e['error']}" for e in recent) or "(none)"
        return (
            "Telegram Codex Bridge stats\n"
            f"- messages: {totals['messages']}\n"
            f"- codex calls: {totals['codex_calls']} (errors {totals['codex_errors']})\n"
            f"- avg codex time: {avg:.1f}s\n"
            f"- fetch success: {totals['fetch_success']}/{total_fetch} ({fetch_rate:.0f}%)\n"
            f"- recent errors:\n{err_lines}"
        )
