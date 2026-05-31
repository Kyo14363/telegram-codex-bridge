"""Telegram command and message handlers."""

from __future__ import annotations

import logging
import subprocess
import time

from telegram import Update
from telegram.ext import ContextTypes

from bridge_core import CodexBridge
from config import CONFIG, VERSION_LABEL
from url_fetchers import detect_urls


logger = logging.getLogger(__name__)


def get_bridge(context: ContextTypes.DEFAULT_TYPE) -> CodexBridge:
    return context.application.bot_data["bridge"]


def is_authorized(update: Update, bridge: CodexBridge) -> bool:
    user_id = update.effective_user.id if update.effective_user else 0
    return bridge.is_authorized(user_id)


def make_progress_cb(message, interval: float):
    state = {"last": 0.0, "text": ""}

    async def cb(text: str) -> None:
        now = time.monotonic()
        if text == state["text"] or now - state["last"] < interval:
            return
        state["last"] = now
        state["text"] = text
        try:
            await message.edit_text(f"Codex is working...\n{text}")
        except Exception as exc:
            logger.debug("progress edit failed: %s", exc)

    return cb


async def reply_long(update: Update, text: str, prefix: str = "") -> None:
    if not update.message:
        return
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)] or [""]
    for idx, chunk in enumerate(chunks):
        head = prefix
        if len(chunks) > 1:
            head += f"[{idx + 1}/{len(chunks)}]\n\n"
        await update.message.reply_text(head + chunk)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text(f"Unauthorized. Your Telegram user id is: {update.effective_user.id}")
        return
    await update.message.reply_text(
        f"{VERSION_LABEL}\n\n"
        "Send a message to run a bounded Codex CLI task from Telegram.\n"
        "Use /help for commands and /status for runtime state."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text(
        "Telegram Codex Bridge commands\n"
        "/start - show startup status\n"
        "/help - show this help\n"
        "/status - show bridge and Codex runtime state\n"
        "/stats - show lightweight usage metrics\n"
        "/cwd - show Codex working directory and extra directories\n"
        "/cancel - stop the active Codex task\n"
        "/clear - alias for /cancel\n"
        "/bridge [n] - show the last n bridge log lines, capped at 120\n"
        "/ps - show local python/node/codex processes\n\n"
        "General use: send a plain message, optionally with a URL or GitHub repo link."
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text(bridge.status_text())


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text(bridge.metrics.summary())


async def cwd_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    extra = "\n".join(CONFIG["CODEX_EXTRA_DIRS"]) or "(none)"
    await update.message.reply_text(f"Codex cwd:\n{CONFIG['WORKING_DIR']}\n\nExtra dirs:\n{extra}")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    await update.message.reply_text(await bridge.cancel_current())


async def bridge_log_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    n = 40
    if context.args:
        try:
            n = max(1, min(int(context.args[0]), 120))
        except ValueError:
            pass
    path = CONFIG["LOG_DIR"] / "bridge.log"
    if not path.exists():
        await update.message.reply_text("No bridge log exists yet.")
        return
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    await reply_long(update, "\n".join(lines) or "(empty)")


async def ps_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text("Unauthorized.")
        return
    script = r"""
$targets = @('python', 'node', 'codex')
Get-Process | Where-Object {
    $name = $_.ProcessName
    $targets | ForEach-Object { if ($name -like "*$_*") { $true } }
} | Select-Object ProcessName,
    @{N='CPU(s)';E={[math]::Round($_.CPU,1)}},
    @{N='Mem(MB)';E={[math]::Round($_.WorkingSet64/1MB,1)}},
    @{N='PID';E={$_.Id}},
    @{N='Runtime';E={
        try {
            $ts = (Get-Date) - $_.StartTime
            if ($ts.TotalHours -ge 1) { '{0:0}h{1:00}m' -f [math]::Floor($ts.TotalHours), $ts.Minutes }
            else { '{0}m{1:00}s' -f $ts.Minutes, $ts.Seconds }
        } catch { '-' }
    }} | Format-Table -AutoSize | Out-String
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        await reply_long(update, result.stdout or result.stderr or "(no process output)")
    except Exception as exc:
        await update.message.reply_text(f"/ps failed: {exc}")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bridge = get_bridge(context)
    if not is_authorized(update, bridge):
        await update.message.reply_text(f"Unauthorized. Your Telegram user id is: {update.effective_user.id}")
        return
    text = (update.message.text or "").strip()
    if not text:
        return

    urls = detect_urls(text)
    if urls:
        processing = await update.message.reply_text("Fetching URL context, then starting Codex...")
    else:
        processing = await update.message.reply_text("Starting Codex...")

    progress_cb = make_progress_cb(processing, CONFIG["PROGRESS_EDIT_INTERVAL"])
    result, url_status = await bridge.run_user_message(text, progress_cb=progress_cb)

    try:
        await processing.delete()
    except Exception:
        pass

    if url_status:
        await reply_long(update, url_status, prefix="URL preprocessing\n\n")
    await reply_long(update, result, prefix="Codex result\n\n")


async def unsupported_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("This bridge currently handles text messages and commands only.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Telegram handler error", exc_info=context.error)
