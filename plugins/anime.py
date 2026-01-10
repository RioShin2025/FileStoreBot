# ---------------------------------------------------
# File Name: Anime.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from bot import Bot
from neonfiles import script

@Bot.on_message(filters.command('anime') & filters.private)
async def send_anime_texts(client: Client, message: Message):
    max_lines_per_page = 40
    max_chars_per_page = 3800
    pages = []
    current_page = []

    total_animes = len(script.NEON_TXT)  # ✅ Count total animes dynamically

    for entry in script.NEON_TXT:
        # Convert plain text to clickable HTML link
        if " - " in entry:
            text_part, url_part = entry.split(" - ", 1)
            entry_html = f"<a href='{url_part}'>{text_part}</a>"
        else:
            entry_html = entry

        entry_html = f"<b><i>{entry_html}</i></b>"

        current_text_length = sum(len(l) + 1 for l in current_page)
        if (len(current_page) >= max_lines_per_page) or (current_text_length + len(entry_html) > max_chars_per_page):
            pages.append(current_page)
            current_page = []
        current_page.append(entry_html)

    if current_page:
        pages.append(current_page)

    sent_messages = []

    for idx, page_links in enumerate(pages):
        if idx == 0:
            page_text = (
                f'<b><i>🍿 {total_animes} Total Animes at <a href="https://t.me/NeonFiles">NeonFiles</a>\n🔰 Managed by <a href="tg://user?id=841851780">MyselfNeon</a></i></b>\n\n'
                + "\n".join(page_links)
            )
        else:
            page_text = "\n".join(page_links)

        sent_msg = await message.reply_text(
            text=page_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        sent_messages.append(sent_msg)

    # ✅ Send sticker after last page
    await message.reply_sticker("CAACAgUAAxkBAAI6eWjpNJUmsaD6O-PzuDOtGxZDg95lAAJFHAACwutJV4qF4DMw0uAwHgQ")

    # ⏳ Auto-delete after 5 minutes
    await asyncio.sleep(300)
    try:
        for msg in sent_messages:
            await msg.delete()
    except Exception as e:
        print(f"**__Auto-Delete Failed:** {e}__")


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
