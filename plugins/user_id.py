# ---------------------------------------------------
# File Name: UserID.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from pyrogram import filters, enums
from pyrogram.types import Message
from bot import Bot

@Bot.on_message(filters.command("id") & filters.private)
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        await message.reply_text(
            f"<b>__Yᴏᴜʀ Usᴇʀ ID Is__ :</b> <code>{user_id}</code>", 
            quote=True
        )        


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
