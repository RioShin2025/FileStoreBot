import asyncio
import time
import platform
import sys

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot import Bot   # ✅ IMPORTANT: import the running client instance

print("✅ status.py loaded")

BOT_START_TIME = time.time()

@Bot.on_callback_query(filters.regex("^close$"))
async def close_btn(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
    await query.answer()

@Bot.on_message(filters.command("status") & filters.private)
async def status_handler(_, message):
    temp = await message.reply("<code>Fᴇᴛᴄʜɪɴɢ ʙᴏᴛ ᴅᴀᴛᴀ...</code>")
    await asyncio.sleep(2)
    await temp.edit("<code>ᴅᴏɴᴇ ɢᴀᴛʜᴇʀɪɴɢ...</code>")
    await asyncio.sleep(1)
    await temp.delete()

    uptime = time.time() - BOT_START_TIME
    uptime_str = time.strftime("%Hh %Mm %Ss", time.gmtime(uptime))

    py_ver = sys.version.split()[0]
    os_name = platform.system()

    await message.reply_photo(
        photo="https://i.ibb.co/vx2JCHD/ca944da5a91d.jpg",
        caption=(
            "<b><i> » Bᴏᴛ Sᴛᴀᴛᴜꜱ</i></b>\n\n"
            f"⫸ <b>Uᴘᴛɪᴍᴇ</b> : <code>{uptime_str}</code>\n"
            f"⫸ <b>Pʏᴛʜᴏɴ</b> : <code>{py_ver}</code>\n"
            f"⫸ <b>Oꜱ</b> : <code>{os_name}</code>\n\n"
            "<i>ʜᴜɴᴛᴇʀ x ɴᴇᴠᴇʀ sʟᴇᴇᴘꜱ...</i>"
        ),
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Developer", url="https://t.me/Otakukart7"),
                InlineKeyboardButton("Close ✖️", callback_data="close")
            ]]
        )
    )
