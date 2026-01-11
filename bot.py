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
from datetime import datetime, timedelta, timezone

from plugins import web_server

# ✅ IMPORTANT: this must be imported BEFORE pyrogram Client import
from pyromod import listen  # noqa: F401

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    Message,
    BotCommand,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    API_HASH, API_ID, BOT_TOKEN, TG_BOT_WORKERS,
    FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, LOG_CHANNEL, KEEP_ALIVE_URL
)

import pyrogram.utils
import pyrogram

pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

IST = timezone(timedelta(hours=5, minutes=30))

# ✅ Add your image link here (must be direct .jpg/.png/.webp) OR telegram file_id
RESTART_BANNER = "https://i.rj1.dev/nVeqm.jpg"

# ✅ Button Links (edit these)
START_NOW_DEEPLINK_PARAM = "start"  # will open t.me/<bot>?start=start
CHANNEL_URL = "https://t.me/Botskingdoms"  # replace


def get_all_plugins(path="plugins"):
    """
    Recursively find all .py files in the plugins folder (excluding __init__.py)
    and return a dict suitable for Client(plugins=...)
    """
    plugins_dict = {}
    for root, _, files in os.walk(path):
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
                await session.get(KEEP_ALIVE_URL, timeout=20)
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
            bot_token=BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins", **get_all_plugins("plugins")},
            # ✅ default parse mode
            parse_mode=ParseMode.HTML,
        )

        # ✅ CRITICAL FIX:
        # Pyromod expects these keys to exist in client.listeners.
        # Different pyromod/pyrogram builds may use enum keys OR string keys.
        # We add BOTH → no KeyError ever.
        self.listeners.setdefault("message", [])
        self.listeners.setdefault("callback_query", [])

        try:
            from pyromod.listen import ListenerTypes
            self.listeners.setdefault(ListenerTypes.MESSAGE, [])
            self.listeners.setdefault(ListenerTypes.CALLBACK_QUERY, [])
        except Exception:
            pass

    async def start(self):
        await super().start()

        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.username = usr_bot_me.username  # store username

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
                    f"❌ Failed to get invite link for FORCE_SUB_CHANNEL<br><br>Error: <code>{a}</code>",
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

        # ✅ Restart Log (blockquote + buttons)
        restart_caption = (
            "<blockquote>\n"
            "🔥 sʏsᴛᴇᴍs ᴏɴʟɪɴᴇ. ʀᴇᴀᴅʏᴛᴏ ʀᴜᴍʙʟᴇ. 🔥\n"
            "ᴅᴄ ᴍᴏᴅᴇ: 𝟼𝟽\n"
            "sʟᴇᴇᴘ ᴍᴏᴅᴇ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ. ɴᴇᴜʀᴀʟ ᴄᴏʀᴇs ᴀᴛ 𝟷𝟶𝟶%. "
            "ғᴇᴇᴅ ᴍᴇ ᴛᴀsᴋs, ᴀɴᴅ ᴡᴀᴛᴄʜ ᴍᴀɢɪᴄ ʜᴀᴘᴘᴇɴ. "
            "ʟᴇᴛ’s. ɢᴇᴛ. ᴅᴀɴɢᴇʀᴏᴜs.\n"
            "</blockquote>"
        )

        restart_buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Start Now",
                        url=f"https://t.me/{self.username}?start={START_NOW_DEEPLINK_PARAM}"
                    ),
                    InlineKeyboardButton(
                        "Channel",
                        url=CHANNEL_URL
                    ),
                ]
            ]
        )

        try:
            await self.send_photo(
                chat_id=LOG_CHANNEL,
                photo=RESTART_BANNER,
                caption=restart_caption,
                parse_mode=ParseMode.HTML,
                reply_markup=restart_buttons
            )
        except Exception as e:
            await self.send_message(
                LOG_CHANNEL,
                restart_caption + f"<br><br><i>(Banner failed: <code>{e}</code>)</i>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=restart_buttons
            )

        # Web server
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        # Keep-alive
        if KEEP_ALIVE_URL:
            asyncio.create_task(keep_alive())

    async def stop(self, *args):
        try:
            await self.send_message(LOG_CHANNEL, "Bot is stopping...", disable_web_page_preview=True)
        except Exception:
            pass
        await super().stop()


# 🔹 Log New Users
@Bot.on_message(filters.command("start") & filters.private)
async def log_new_user(client: Bot, message: Message):
    user = message.from_user

    now = datetime.now(IST)
    date = now.strftime("%d/%m/%y")
    time_ = now.strftime("%I:%M:%S %p")

    log_text = (
        f"<blockquote>"
        f"<b>⌬ 🆕👤 #NewUser</b><br>"
        f"<b>Bot:</b> <b>@{client.username}</b><br>"
        f"<b>User:</b> {user.mention}<br>"
        f"<b>User ID:</b> <code>{user.id}</code><br>"
        f"<b>Date:</b> {date}<br>"
        f"<b>Time:</b> {time_}"
        f"</blockquote>"
    )

    await client.send_message(LOG_CHANNEL, log_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    await message.reply_text("👋 Hello! You started the bot ✅")
