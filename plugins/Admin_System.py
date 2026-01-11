
# plugins/Admin_System.py

from pyrogram import filters
from config import OWNER_ID
from database.database import add_admin, remove_admin, get_all_admins
from pyrogram.enums import ParseMode

from bot import Bot  # ✅ IMPORTANT: use the running client instance


# ➕ Add Admin
@Bot.on_message(filters.command("add_admin") & filters.private)
async def add_admin_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("<code>Oɴʟʏ ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴ ᴅᴏ ᴛʜɪꜱ, ʙᴀʙʏ...</code>", parse_mode="html")

    try:
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply_text("<code>Gɪᴠᴇ ᴀ ᴘʀᴏᴘᴇʀ ᴜꜱᴇʀ ɪᴅ, ʜᴜɴᴛᴇʀ</code>", parse_mode="html")

    add_admin(user_id)
    await message.reply_text(
        f"<code>➥ Aᴅᴅᴇᴅ {user_id} ᴛᴏ ᴍʏ ʟᴏʏᴀʟ ᴀᴅᴍɪɴꜱ ♨️</code>",
        parse_mode=ParseMode.HTML
    )


# ➖ Remove Admin
@Bot.on_message(filters.command("remove_admin") & filters.private)
async def remove_admin_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("<code>Yᴏᴜ ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴘᴏᴡᴇʀ, ʜᴏɴᴇʏ...</code>", parse_mode="html")

    try:
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply_text("<code>Pᴜᴛ ᴀ ᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ, ᴅᴏɴ'ᴛ ᴍᴇss ᴡɪᴛʜ ᴍᴇ</code>", parse_mode="html")

    remove_admin(user_id)
    await message.reply_text(
        f"<code>➥ {user_id} ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴏɴ ᴛʜᴇ ᴛʜʀᴏɴᴇ 💔</code>",
        parse_mode=ParseMode.HTML
    )


# 📜 List Admins
@Bot.on_message(filters.command("admins_list") & filters.private)
async def admins_list_handler(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("<code>Oɴʟʏ ᴛʜᴇ ᴏɴᴇ ᴡʜᴏ ʀᴜʟᴇꜱ ᴄᴀɴ ʟɪꜱᴛ ᴛʜᴇ ʟᴏʏᴀʟ</code>", parse_mode="html")

    admins = get_all_admins()
    if not admins:
        return await message.reply_text("<code>Nᴏ ᴀᴅᴍɪɴꜱ ʏᴇᴛ, ᴍʏ ʟᴏʀᴅ</code>", parse_mode="html")

    admins_text = "\n".join([f"➥ <code>{uid}</code>" for uid in admins])

    await message.reply_text(
        f"<b>⚙️ Aᴄᴛɪᴠᴇ Aᴅᴍɪɴꜱ:</b>\n{admins_text}",
        parse_mode=ParseMode.HTML
    )
