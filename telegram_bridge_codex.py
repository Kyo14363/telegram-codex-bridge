"""Entry point for Telegram Codex Bridge."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bridge_core import CodexBridge
from config import CONFIG, VERSION_LABEL, ensure_runtime_dirs, setup_logging
from handlers import (
    bridge_log_command,
    cancel_command,
    cwd_command,
    error_handler,
    help_command,
    message_handler,
    ps_command,
    start_command,
    stats_command,
    status_command,
    unsupported_handler,
)


logger = logging.getLogger(__name__)


def build_application() -> Application:
    token = CONFIG["TELEGRAM_BOT_TOKEN"]
    if not token:
        raise RuntimeError(
            "Missing TELEGRAM_CODEX_BOT_TOKEN. Copy .env.example to .env and set your Telegram bot token."
        )

    bridge = CodexBridge()
    app = Application.builder().token(token).build()
    app.bot_data["bridge"] = bridge
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("cwd", cwd_command))
    app.add_handler(CommandHandler("clear", cancel_command))
    app.add_handler(CommandHandler("cancel", cancel_command))
    app.add_handler(CommandHandler("bridge", bridge_log_command))
    app.add_handler(CommandHandler("ps", ps_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(MessageHandler(filters.ALL, unsupported_handler))
    app.add_error_handler(error_handler)
    return app


def main() -> None:
    setup_logging()
    ensure_runtime_dirs()
    logger.info("%s starting", VERSION_LABEL)
    logger.info("cwd=%s extra_dirs=%s", CONFIG["WORKING_DIR"], CONFIG["CODEX_EXTRA_DIRS"])
    app = build_application()
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
