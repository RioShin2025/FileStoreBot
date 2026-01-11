# ---------------------------------------------------
# File Name: restart.py
# Author: NeonAnurag (Modified by RioShin)
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# ---------------------------------------------------

import asyncio
import os
import signal

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.errors import WebpageMediaEmpty
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS


RESTART_PIC = "https://i.rj1.dev/TEBEb.jpg"
RESTART_TEXT = "<b>💔 Rᴇsᴛᴀʀᴛɪɴɢ... Dᴏɴ'ᴛ ʏᴏᴜ ᴅᴀʀᴇ ᴛᴏ ᴍᴇss ᴡɪᴛʜ ᴍᴇ ʙᴀʙʏ!</b>"


def restart_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🛠️ Dᴇᴠ", url="https://t.me/RioShin"),
                InlineKeyboardButton("❌ Cʟᴏꜱᴇ", callback_data="close")
            ]
        ]
    )


async def safe_reply_photo(message, photo: str, caption: str, reply_markup=None):
    """
    If Telegram can't fetch the URL as media (WEBPAGE_MEDIA_EMPTY),
    fallback to text message instead of crashing.
    """
    try:
        return await message.reply_photo(
            photo=photo,
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    except WebpageMediaEmpty:
        return await message.reply_text(
            text=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception:
        return await message.reply_text(
            text=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )


@Client.on_message(filters.command("restart") & filters.private)
async def restart_bot(client: Client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply(
            "<code>🛑 Bᴀʙʏ ɴᴏ, ʏᴏᴜ ʟᴀᴄᴋ ᴛʜᴇ ᴄʀᴏᴡɴ ғᴏʀ ᴛʜɪꜱ ᴏʀᴅᴇʀ 👑</code>"
        )

    # Step 1: Send dramatic goodbye 😭 (with safe fallback)
    await safe_reply_photo(
        message,
        photo=RESTART_PIC,
        caption=RESTART_TEXT,
        reply_markup=restart_buttons()
    )

    # Step 2: Delay for drama 😏
    await asyncio.sleep(2)

    # Step 3: Heroku-safe restart
    # Don't use os.execvp on Heroku. Just terminate; dyno manager restarts it.
    os.kill(os.getpid(), signal.SIGTERM)
