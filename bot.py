# ---------------------------------------------------
# File Name: bot.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# License: MIT
# ---------------------------------------------------

import os
import sys
import asyncio
import logging
import aiohttp
from aiohttp import web
from datetime import datetime, timedelta, timezone

from plugins import web_server

# ✅ IMPORTANT: must be imported BEFORE pyrogram Client import
from pyromod import listen  # noqa: F401

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    API_HASH, API_ID, BOT_TOKEN, TG_BOT_WORKERS,
    FORCE_SUB_CHANNEL, CHANNEL_ID, PORT, LOG_CHANNEL, KEEP_ALIVE_URL
)

import pyrogram.utils
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

IST = timezone(timedelta(hours=5, minutes=30))

# ✅ Restart banner (direct image link OR Telegram file_id)
RESTART_BANNER = "https://i.rj1.dev/nVeqm.jpg"

# ✅ Button Links
START_NOW_DEEPLINK_PARAM = "start"   # t.me/<bot>?start=start
CHANNEL_URL = "https://t.me/Botskingdoms"


def get_all_plugins(path="plugins"):
    """
    Recursively find all .py files in plugins folder (excluding __init__.py)
    and return dict for Client(plugins=...)
    """
    plugins_dict = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, file), path)
                module_path = rel_path.replace(os.sep, ".")[:-3]
                plugins_dict[module_path] = {}
    return plugins_dict


async def keep_alive():
    """Send a request every 100 seconds to keep the bot alive."""
    if not KEEP_ALIVE_URL:
        return
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
            parse_mode=ParseMode.HTML,
        )

        # ✅ Pyromod listener fix (supports both string keys + enum keys)
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

        me = await self.get_me()
        self.username = me.username
        self.uptime = datetime.now()

        # ✅ Force Sub invite link (optional)
        if FORCE_SUB_CHANNEL:
            try:
                chat = await self.get_chat(FORCE_SUB_CHANNEL)
                link = chat.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    chat = await self.get_chat(FORCE_SUB_CHANNEL)
                    link = chat.invite_link
                self.invitelink = link
            except Exception as a:
                await self.send_message(
                    LOG_CHANNEL,
                    f"❌ Failed to get invite link for FORCE_SUB_CHANNEL<br><br>Error: <code>{a}</code>",
                    disable_web_page_preview=True
                )
                sys.exit(1)

        # ✅ DB channel check
        try:
            self.db_channel = await self.get_chat(CHANNEL_ID)
        except Exception as e:
            await self.send_message(
                LOG_CHANNEL,
                f"❌ Failed to connect DB channel.<br>Error: <code>{e}</code><br><br>Check CHANNEL_ID: <code>{CHANNEL_ID}</code>",
                disable_web_page_preview=True
            )
            sys.exit(1)

        # ✅ Restart caption (BLOCKQUOTE FIXED)
        restart_caption = (
            "<blockquote>\n"
            "🔥 sʏsᴛᴇᴍs ᴏɴʟɪɴᴇ. ʀᴇᴀᴅʏᴛᴏ ʀᴜᴍʙʟᴇ. 🔥\n"
            "ᴅᴄ ᴍᴏᴅᴇ: 𝟼𝟽\n"
            "sʟᴇᴇᴘ ᴍᴏᴅᴇ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ. ɴᴇᴜʀᴀʟ ᴄᴏʀᴇs ᴀᴛ 𝟷𝟶𝟶%.\n"
            "ғᴇᴇᴅ ᴍᴇ ᴛᴀsᴋs, ᴀɴᴅ ᴡᴀᴛᴄʜ ᴍᴀɢɪᴄ ʜᴀᴘᴘᴇɴ.\n"
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
                    InlineKeyboardButton("Channel", url=CHANNEL_URL),
                ]
            ]
        )

        try:
            await self.send_photo(
                chat_id=LOG_CHANNEL,
                photo=RESTART_BANNER,
                caption=restart_caption,
                reply_markup=restart_buttons
            )
        except Exception as e:
            await self.send_message(
                LOG_CHANNEL,
                restart_caption + f"<br><br><i>(Banner failed: <code>{e}</code>)</i>",
                disable_web_page_preview=True,
                reply_markup=restart_buttons
            )

        # ✅ Web server
        runner = web.AppRunner(await web_server())
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", PORT).start()

        # ✅ keep alive task
        if KEEP_ALIVE_URL:
            asyncio.create_task(keep_alive())

    async def stop(self, *args):
        try:
            await self.send_message(LOG_CHANNEL, "Bot is stopping...", disable_web_page_preview=True)
        except Exception:
            pass
        await super().stop()


# ✅ Log new users (ONLY THIS FUNCTION, NO DUPLICATES)
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

    await client.send_message(LOG_CHANNEL, log_text, disable_web_page_preview=True)
    await message.reply_text("👋 Hello! You started the bot ✅")
