"""Configuration and logging helpers for Telegram Codex Bridge."""

from __future__ import annotations

import logging
import os
import re
import sys
from pathlib import Path
from typing import Iterable, List


VERSION = "0.1.0"
VERSION_LABEL = f"Telegram Codex Bridge v{VERSION}"
BASE_DIR = Path(__file__).resolve().parent


def load_dotenv(path: Path | None = None) -> None:
    """Load a small .env file without requiring python-dotenv."""
    env_path = path or (BASE_DIR / ".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except ValueError:
        return default


def parse_float(value: str | None, default: float) -> float:
    try:
        return float(value) if value not in (None, "") else default
    except ValueError:
        return default


def parse_paths(value: str | None) -> List[str]:
    if not value:
        return []
    return [part.strip() for part in re.split(r"[;\n]+", value) if part.strip()]


def resolve_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return path.resolve()


def resolve_paths(values: Iterable[str]) -> List[str]:
    return [str(resolve_path(value)) for value in values]


def parse_allowed_users(value: str | None) -> List[int]:
    ids: List[int] = []
    for part in re.split(r"[,\s;]+", (value or "").strip()):
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue
    return ids


load_dotenv()

CONFIG = {
    "BASE_DIR": BASE_DIR,
    "LOG_DIR": resolve_path(os.getenv("TCB_LOG_DIR", "logs")),
    "RUN_DIR": resolve_path(os.getenv("TCB_RUN_DIR", "runs")),
    "FETCH_OUTPUT_DIR": resolve_path(os.getenv("TCB_FETCH_OUTPUT_DIR", "fetch_outputs")),
    "STATS_FILE": resolve_path(os.getenv("TCB_STATS_FILE", "stats.json")),
    "WORKING_DIR": resolve_path(os.getenv("TCB_WORKING_DIR", "workspace")),
    "CODEX_EXTRA_DIRS": resolve_paths(parse_paths(os.getenv("TCB_CODEX_EXTRA_DIRS"))),
    "CODEX_MODEL": os.getenv("TCB_CODEX_MODEL", "").strip(),
    "CODEX_SEARCH": parse_bool(os.getenv("TCB_CODEX_SEARCH"), default=False),
    "CODEX_FULL_AUTO": parse_bool(os.getenv("TCB_CODEX_FULL_AUTO"), default=False),
    "CODEX_SKIP_GIT_REPO_CHECK": parse_bool(os.getenv("TCB_CODEX_SKIP_GIT_REPO_CHECK"), default=True),
    "CODEX_TIMEOUT": parse_int(os.getenv("TCB_CODEX_TIMEOUT"), 1800),
    "PROGRESS_EDIT_INTERVAL": parse_float(os.getenv("TCB_PROGRESS_EDIT_INTERVAL"), 2.0),
    "OUTPUT_MAX_CHARS": parse_int(os.getenv("TCB_OUTPUT_MAX_CHARS"), 12000),
    "URL_FETCH_TIMEOUT": parse_int(os.getenv("TCB_URL_FETCH_TIMEOUT"), 20),
    "FETCH_MAX_RETRIES": parse_int(os.getenv("TCB_FETCH_MAX_RETRIES"), 2),
    "MAX_IMAGES_PER_MESSAGE": parse_int(os.getenv("TCB_MAX_IMAGES_PER_MESSAGE"), 5),
    "IMAGE_ANALYSIS_ENABLED": parse_bool(os.getenv("TCB_IMAGE_ANALYSIS_ENABLED"), default=False),
    "IMAGE_ANALYSIS_TIMEOUT": parse_int(os.getenv("TCB_IMAGE_ANALYSIS_TIMEOUT"), 30),
    "GITHUB_README_MAX_LEN": parse_int(os.getenv("TCB_GITHUB_README_MAX_LEN"), 8000),
    "THIN_CONTENT_THRESHOLD": parse_int(os.getenv("TCB_THIN_CONTENT_THRESHOLD"), 200),
    "OBSIDIAN_MOBILE_DIR": resolve_path(os.getenv("TCB_OBSIDIAN_MOBILE_DIR", "obsidian_clippings")),
    "ALLOWED_USER_IDS": parse_allowed_users(os.getenv("TCB_ALLOWED_USER_IDS") or os.getenv("ALLOWED_USER_IDS")),
    "TELEGRAM_BOT_TOKEN": (
        os.getenv("TELEGRAM_CODEX_BOT_TOKEN")
        or os.getenv("TCB_TELEGRAM_BOT_TOKEN")
        or os.getenv("TELEGRAM_BOT_TOKEN")
        or ""
    ),
}


class SecretRedactionFilter(logging.Filter):
    TOKEN_PATTERNS: Iterable[re.Pattern[str]] = (
        re.compile(r"bot\d{6,}:[A-Za-z0-9_-]{20,}"),
        re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    )

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pattern in self.TOKEN_PATTERNS:
            msg = pattern.sub("[REDACTED_SECRET]", msg)
        record.msg = msg
        record.args = ()
        return True


def setup_logging() -> None:
    CONFIG["LOG_DIR"].mkdir(parents=True, exist_ok=True)
    log_file = CONFIG["LOG_DIR"] / "bridge.log"
    redactor = SecretRedactionFilter()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)
    for handler in (file_handler, stream_handler):
        handler.addFilter(redactor)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[file_handler, stream_handler],
    )
    for logger_name in ("httpx", "telegram"):
        logging.getLogger(logger_name).addFilter(redactor)
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def ensure_runtime_dirs() -> None:
    for key in ("LOG_DIR", "RUN_DIR", "FETCH_OUTPUT_DIR", "WORKING_DIR", "OBSIDIAN_MOBILE_DIR"):
        CONFIG[key].mkdir(parents=True, exist_ok=True)
