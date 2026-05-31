"""Repository sanity checks for CI.

This script intentionally avoids network calls and live Telegram/Codex work. It
checks only tracked repository files so local ignored runtime data such as
`.env`, `logs/`, and `runs/` does not make local verification noisy.
"""

from __future__ import annotations

import os
import re
import subprocess
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_TRACKED_PATH_PARTS = {
    ".env",
    "logs",
    "runs",
    "fetch_outputs",
    "workspace",
    "obsidian_clippings",
    "__pycache__",
    ".pytest_cache",
    "stats.json",
}

PRIVATE_TEXT_PATTERNS = {
    "private Windows user path": re.compile("Rescue" + "Admin", re.IGNORECASE),
    "private Obsidian vault path": re.compile("Obsidian" + "_SV", re.IGNORECASE),
    "private T-M-B path": re.compile("telegram-" + "MCP-bridge", re.IGNORECASE),
    "Telegram bot token": re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{20,}\b"),
    "OpenAI-style API key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
}

TEXT_SUFFIXES = {
    "",
    ".bat",
    ".cfg",
    ".example",
    ".gitignore",
    ".gitattributes",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".toml",
    ".yml",
    ".yaml",
}


def run_git_ls_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", "requirements.txt", "dev-requirements.txt"}


def check_tracked_paths(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        parts = set(Path(rel).parts)
        if rel == ".env":
            errors.append("Tracked .env file is not allowed")
        for forbidden in FORBIDDEN_TRACKED_PATH_PARTS:
            if forbidden in parts or rel == forbidden:
                errors.append(f"Tracked runtime/private path is not allowed: {rel}")
    return errors


def check_private_text(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if not is_text_file(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PRIVATE_TEXT_PATTERNS.items():
            for match in pattern.finditer(text):
                line_no = text.count("\n", 0, match.start()) + 1
                errors.append(f"{label} found in {rel}:{line_no}")
    return errors


def check_markdown_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in link_pattern.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target or target.startswith("<"):
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                errors.append(f"Markdown link escapes repo in {rel}: {target}")
                continue
            if not candidate.exists():
                line_no = text.count("\n", 0, match.start()) + 1
                errors.append(f"Broken markdown link in {rel}:{line_no}: {target}")
    return errors


def check_version_consistency() -> list[str]:
    errors: list[str] = []
    config_text = (ROOT / "config.py").read_text(encoding="utf-8")
    match = re.search(r'^VERSION = "([^"]+)"', config_text, flags=re.MULTILINE)
    if not match:
        return ["VERSION not found in config.py"]
    version = match.group(1)
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## {version} " not in changelog and f"## {version} -" not in changelog:
        errors.append(f"CHANGELOG.md has no section for config.py VERSION={version}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if f"`v{version}`" not in readme:
        errors.append(f"README.md does not mention `v{version}`")
    pyproject_path = ROOT / "pyproject.toml"
    if pyproject_path.exists():
        project = tomllib.loads(pyproject_path.read_text(encoding="utf-8")).get("project", {})
        if project.get("version") != version:
            errors.append(
                "pyproject.toml project.version does not match "
                f"config.py VERSION={version}"
            )
    return errors


def main() -> int:
    os.chdir(ROOT)
    files = run_git_ls_files()
    errors: list[str] = []
    errors.extend(check_tracked_paths(files))
    errors.extend(check_private_text(files))
    errors.extend(check_markdown_links(files))
    errors.extend(check_version_consistency())

    if errors:
        print("Sanity check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Sanity check passed ({len(files)} tracked files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
