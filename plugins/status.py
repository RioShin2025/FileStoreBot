from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
import asyncio
import time
import platform
import sys

print("✅ status.py loaded")

# -------------------------
# Bot start time (session uptime)
# -------------------------
BOT_START_TIME = time.time()

# -------------------------
# OPTIONAL: Replace these with real DB values later
# -------------------------
def get_total_users() -> int:
    # TODO: replace with your DB count
    return 1234

def get_total_admins() -> int:
    # TODO: replace with your admin list length / DB count
    return 5

# -------------------------
# Close button handler
# -------------------------
@Client.on_callback_query(filters.regex(r"^close$"))
async def close_btn(client: Client, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
    try:
        await query.answer("Closed ✅", show_alert=False)
    except:
        pass

# -------------------------
# /status command
# -------------------------
@Client.on_message(filters.command("status") & filters.private)
async def status_handler(client: Client, message):
    # Step 1: Temp loading
    temp = await message.reply("<code>Fᴇᴛᴄʜɪɴɢ ʙᴏᴛ ᴅᴀᴛᴀ...</code>")
    await asyncio.sleep(2)
    await temp.edit("<code>ᴅᴏɴᴇ ɢᴀᴛʜᴇʀɪɴɢ...</code>")
    await asyncio.sleep(1)
    await temp.delete()

    # Step 2: Firework sticker (optional)
    try:
        await client.send_sticker(
            chat_id=message.chat.id,
            sticker="CAACAgUAAxkBAAEin5FoTUn9ef0gFsZtJhlgTWCtH5jI-gACHgoAAsmuGVVnKBvEVZZMvDYE"
        )
    except:
        # If sticker invalid or blocked, ignore
        pass

    # Step 3: Uptime calc
    uptime = time.time() - BOT_START_TIME
    uptime_str = time.strftime("%Hh %Mm %Ss", time.gmtime(uptime))

    # Step 4: Get stats (replace with DB later)
    total_users = get_total_users()
    total_admins = get_total_admins()

    # Extra info (safe)
    py_ver = sys.version.split()[0]
    os_name = platform.system() + " " + platform.release()

    # Step 5: Send status report
    await client.send_photo(
        chat_id=message.chat.id,
        photo="https://i.rj1.dev/TEBEb.jpg",
        caption=(
            "<b><i> » Bᴏᴛ Sᴛᴀᴛᴜꜱ ʀᴇᴘᴏʀᴛ</i></b>\n\n"
            "⫸ <b>Tᴏᴛᴀʟ Uꜱᴇʀꜱ</b> : <code>{}</code>\n"
            "⫸ <b>Aᴅᴍɪɴꜱ</b> : <code>{}</code>\n"
            "⫸ <b>Uᴘᴛɪᴍᴇ</b> : <code>{}</code>\n\n"
            "⫸ <b>Pʏᴛʜᴏɴ</b> : <code>{}</code>\n"
            "⫸ <b>Oꜱ</b> : <code>{}</code>\n\n"
            "<i>Lᴇɢᴇɴᴅs ɴᴇᴠᴇʀ sʟᴇᴇᴘꜱ...</i>"
        ).format(total_users, total_admins, uptime_str, py_ver, os_name),
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RioShin"),
                InlineKeyboardButton("Cʟᴏꜱᴇ ✖️", callback_data="close")
            ]
        ])
    )
