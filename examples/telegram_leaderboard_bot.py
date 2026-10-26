"""Minimal Telegram leaderboard bot.

Install optional dependencies:
    python -m pip install python-telegram-bot

Set these in the environment or in an ignored ``.env``:
    TELEGRAM_TOKEN=...
    BMG_USERNAME=...
    BMG_PASSWORD=...
    BMG_DEVICE_ID=...
    BMG_BMDDH_ID=...
"""

import asyncio
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from blockmango import BmgAccount

load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise SystemExit("Set TELEGRAM_TOKEN")

account: BmgAccount | None = None


async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if account is None or not account.is_logged_in:
        await update.message.reply_text("Blockman GO account is not ready yet.")
        return
    args = context.args or []
    game_id = args[0] if args else "g1055"
    period = args[1] if len(args) > 1 else "all"
    rows = await account.ranking.async_get_game_leaderboard_entries(
        game_id, period=period, page=0, size=5
    )
    if not rows:
        await update.message.reply_text(f"No {period} leaderboard rows for {game_id}.")
        return
    lines = [f"{game_id} / {period}"]
    for entry in rows:
        score = entry.display_value or entry.score
        lines.append(f"#{entry.rank} {entry.nick_name} — {score}")
    await update.message.reply_text("\n".join(lines))


async def main() -> None:
    global account
    account = BmgAccount.from_env()
    if not await account.async_login():
        raise RuntimeError("Blockman GO login failed")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("rank", rank))
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
