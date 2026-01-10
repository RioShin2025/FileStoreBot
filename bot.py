# ---------------------------------------------------
# File Name: Bot.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

import os
import sys
import asyncio
import logging
import aiohttp
from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, BotCommand
from datetime import datetime, timedelta, timezone
from config import (
    API_HASH, API_ID, BOT_TOKEN, TG_BOT_WORKERS,
    FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, LOG_CHANNEL, KEEP_ALIVE_URL
)
import pyrogram.utils
import pyrogram  # ✅ For version info

pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

IST = timezone(timedelta(hours=5, minutes=30))

RESTART_BANNER = "https://i.rj1.dev/nVeqm.jpg"

def get_all_plugins(path="plugins"):
    """
    Recursively find all .py files in the plugins folder (excluding __init__.py and this loader)
    and return a dict suitable for Client(plugins=...)
    """
    plugins_dict = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                module_path = rel_path.replace(os.sep, ".")[:-3]  # remove .py
                plugins_dict[module_path] = {}
    return plugins_dict

async def keep_alive():
    """Send a request every 100 seconds to keep the bot alive (if required)."""
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await session.get(KEEP_ALIVE_URL)
                logging.info("Sent keep-alive request.")
            except Exception as e:
                logging.error(f"Keep-alive request failed: {e}")
            await asyncio.sleep(100)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins", **get_all_plugins("plugins")},  # ✅ Auto-load all plugins
            workers=TG_BOT_WORKERS,
            bot_token=BOT_TOKEN
        )

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.username = usr_bot_me.username  # store username
        bot_mention = f"@{usr_bot_me.username}"  # ✅ Use username mention for logs

        # ✅ Set default parse mode to HTML (we use blockquote + links)
        self.set_parse_mode(ParseMode.HTML)

        # Force Sub Check
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                await self.send_message(
                    LOG_CHANNEL,
                    f"❌ Failed to get invite link for FORCE_SUB_CHANNEL\n\nError: <code>{a}</code>",
                    disable_web_page_preview=True
                )
                sys.exit()

        # DB Channel Check
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
        except Exception as e:
            await self.send_message(
                LOG_CHANNEL,
                f"❌ Failed to connect DB channel.<br>Error: <code>{e}</code><br><br>Check CHANNEL_ID: <code>{CHANNEL_ID}</code>",
                disable_web_page_preview=True
            )
            sys.exit()

        # ✅ Bot Restart Log (Premium + Image + No Inline Buttons)
        now = datetime.now(IST)
        date = now.strftime("%d/%m/%y")
        time = now.strftime("%I:%M:%S %p")

        restart_text = f"""<blockquote>
🔥 <b>SYSTEMS ONLINE. READY TO RUMBLE.</b> 🔥<br><br>
Bot: <b>@{self.username}</b><br>
{date} · {time} IST<br>
v3.0.8-x · Render<br>
Reason: Manual restart<br>
Uptime: Reset<br><br>
<i>Sleep mode deactivated.<br>
Neural cores at 100%.<br>
Feed me tasks, and watch magic happen.</i><br><br>
— <a href="https://t.me/RioShin">RioShin</a> ·
<a href="https://github.com/RioShin2025/FilestoreBot">Repo</a> ·
<a href="https://t.me/+t_wcYC3jAb40ZTJl">Logs</a>
</blockquote>"""

        try:
            await self.send_photo(
                chat_id=LOG_CHANNEL,
                photo=RESTART_BANNER,
                caption=restart_text,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            # fallback text-only if banner fails
            await self.send_message(
                LOG_CHANNEL,
                restart_text + f"<br><br><i>(Banner failed: <code>{e}</code>)</i>",
                disable_web_page_preview=True
            )

        # Web response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        # ✅ Start keep-alive loop in background
        if KEEP_ALIVE_URL:
            asyncio.create_task(keep_alive())

    async def stop(self, *args):
        try:
            await self.send_message(LOG_CHANNEL, "❌ Bot Stopped!", disable_web_page_preview=True)
        except Exception:
            pass
        await super().stop()

# 🔹 Log New Users (HTML only, because bot default parse_mode is HTML)
@Bot.on_message(filters.command("start") & filters.private)
async def log_new_user(client: Bot, message: Message):
    user = message.from_user

    now = datetime.now(IST)
    date = now.strftime("%d/%m/%y")
    time = now.strftime("%I:%M:%S %p")  # ✅ fixed (was %I:%M.%S)

    log_text = (
        f"<blockquote>"
        f"<b>⌬ 🆕👤 #NewUser</b><br>"
        f"<b>Bot:</b> <b>@{client.username}</b><br>"
        f"<b>User:</b> {user.mention}<br>"
        f"<b>User ID:</b> <code>{user.id}</code><br>"
        f"<b>Date:</b> {date}<br>"
        f"<b>Time:</b> {time}"
        f"</blockquote>"
    )

    await client.send_message(LOG_CHANNEL, log_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    await message.reply_text("👋 Hello! You started the bot ✅")

# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
