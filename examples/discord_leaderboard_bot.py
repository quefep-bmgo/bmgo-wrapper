"""Minimal Discord leaderboard bot.

Install optional dependencies:
    python -m pip install discord.py

Set these in the environment or in an ignored ``.env``:
    DISCORD_TOKEN=...
    BMG_USERNAME=...
    BMG_PASSWORD=...
    BMG_DEVICE_ID=...
    BMG_BMDDH_ID=...
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from blockmango import BmgAccount

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("Set DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # prefix commands
bot = commands.Bot(command_prefix="!", intents=intents)
account: BmgAccount | None = None


@bot.event
async def on_ready() -> None:
    global account
    account = BmgAccount.from_env()
    if not await account.async_login():
        raise RuntimeError("Blockman GO login failed")
    print(f"Logged in as {bot.user} and Blockman GO user {account.uid}")


@bot.command(name="rank")
async def rank(ctx: commands.Context, game_id: str = "g1055", period: str = "all") -> None:
    if account is None or not account.is_logged_in:
        await ctx.send("Blockman GO account is not ready yet.")
        return
    rows = await account.ranking.async_get_game_leaderboard_entries(
        game_id, period=period, page=0, size=5
    )
    if not rows:
        await ctx.send(f"No {period} leaderboard rows for {game_id}.")
        return
    lines = [f"**{game_id} / {period}**"]
    for entry in rows:
        score = entry.display_value or entry.score
        lines.append(f"#{entry.rank} {entry.nick_name} — {score}")
    await ctx.send("\n".join(lines))


if __name__ == "__main__":
    bot.run(TOKEN)
