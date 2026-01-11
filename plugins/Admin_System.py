# plugins/Admin_System.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from database.database import add_admin, remove_admin, get_all_admins
import asyncio



# ➕ Add Admin
@Client.on_message(filters.command("add_admin") & filters.private)
async def add_admin_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("<code>Oɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ, ʙᴀʙʏ...</code>")

    try:
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply("<code>Gɪᴠᴇ ᴀ ᴘʀᴏᴘᴇʀ ᴜꜱᴇʀ ɪᴅ, ʜᴜɴᴛᴇʀ</code>")

    add_admin(user_id)
    await message.reply(
        f"<code>➥ Aᴅᴅᴇᴅ {user_id} ᴛᴏ ᴍʏ ʟᴏʏᴀʟ ᴀᴅᴍɪɴꜱ ♨️</code>"
    )

# ➖ Remove Admin
@Client.on_message(filters.command("remove_admin") & filters.private)
async def remove_admin_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("<code>Yᴏᴜ ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴘᴏᴡᴇʀ, ʜᴏɴᴇʏ...</code>")

    try:
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply("<code>Pᴜᴛ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ, ᴅᴏɴ'ᴛ ᴍᴇss ᴡɪᴛʜ ᴍᴇ</code>")

    remove_admin(user_id)
    await message.reply(
        f"<code>➥ {user_id} ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴏɴ ᴛʜᴇ ᴛʜʀᴏɴᴇ 💔</code>"
    )

# 📜 List Admins
@Client.on_message(filters.command("admins_list") & filters.private)
async def admins_list_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("<code>Oɴʟʏ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ʀᴜʟᴇꜱ ᴄᴀɴ ʟɪꜱᴛ ᴛʜᴇ ʟᴏʏᴀʟ</code>")

    admins = get_all_admins()
    if not admins:
        return await message.reply("<code>Nᴏ ᴀᴅᴍɪɴꜱ ʏᴇᴛ, ᴍʏ ʟᴏʀᴅ</code>")

    admins_text = "\n".join([f"➥ <code>{uid}</code>" for uid in admins])
    await message.reply(
        f"<b>⚙️ Aᴄᴛɪᴠᴇ Aᴅᴍɪɴꜱ:</b>\n{admins_text}",
        parse_mode="html"
  )
