# ---------------------------------------------------
# File Name: Restart.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from config import ADMINS


@Client.on_message(filters.command("restart") & filters.private)
async def restart_bot(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply("<code>🛑 Bᴀʙʏ ɴᴏ, ʏᴏᴜ ʟᴀᴄᴋ ᴛʜᴇ ᴄʀᴏᴡɴ ғᴏʀ ᴛʜɪꜱ ᴏʀᴅᴇʀ 👑</code>")

    # Step 1: Send dramatic goodbye 😭
    bye = await message.reply_photo(
        photo="https://i.ibb.co/mHTMbmM/630b4ff5ccf9.jpg",
        caption="<b>💔 Rᴇsᴛᴀʀᴛɪɴɢ... Dᴏɴ'ᴛ ʏᴏᴜ ᴅᴀʀᴇ ᴍɪss ᴍᴇ ʙᴀʙʏ!</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛠️ Dᴇᴠ", url="https://t.me/RioShin"),
             InlineKeyboardButton("❌ Cʟᴏꜱᴇ", callback_data="close")]
        ])
    )

    # Step 2: Delay for drama 😏
    await asyncio.sleep(3)

    # Step 3: Restart process (real reload)
    os.execvp("python", ["python", "-m", "bot"])
