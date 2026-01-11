import asyncio
import time
import platform
import sys

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot import Bot

print("✅ status.py loaded")

BOT_START_TIME = time.time()


@Bot.on_callback_query(filters.regex(r"^close$"))
async def close_btn(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
    try:
        await query.answer()
    except:
        pass


@Bot.on_message(filters.command("status") & filters.private)
async def status_handler(_, message):
    # Loading
    temp = await message.reply_text("Fetching bot data...", quote=True)
    await asyncio.sleep(2)
    await temp.edit_text("Done gathering...")
    await asyncio.sleep(1)
    await temp.delete()

    # Uptime
    uptime = time.time() - BOT_START_TIME
    uptime_str = time.strftime("%Hh %Mm %Ss", time.gmtime(uptime))

    # System info
    py_ver = sys.version.split()[0]
    os_name = f"{platform.system()} {platform.release()}"

    # ✅ SAFE HTML (plain text inside tags)
    caption = (
        "<b>» Bot Status</b>\n\n"
        f"⫸ <b>Uptime</b> : <code>{uptime_str}</code>\n"
        f"⫸ <b>Python</b> : <code>{py_ver}</code>\n"
        f"⫸ <b>OS</b> : <code>{os_name}</code>\n\n"
        "<i>Hunter x Never Sleeps...</i>"
    )

    await message.reply_photo(
        photo="https://i.rj1.dev/TEBEb.jpg",
        caption=caption,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Developer", url="https://t.me/Otakukart7"),
                InlineKeyboardButton("Close ✖️", callback_data="close")
            ]]
        )
        )
