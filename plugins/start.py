# ---------------------------------------------------
# File Name: start.py
# Author: BotsKingdoms x RioShin (Modified)
# GitHub: https://github.com/BotsKingdoms/
# Telegram: https://t.me/Botskingdoms
# Developer: https://t.me/RioShin
# Created: 2025-10-21
# Last Modified: 2026-01-11
# Version: Latest
# License: MIT License
# ---------------------------------------------------

import os
import asyncio
import humanize

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import (
    ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION,
    DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT,
    FILE_AUTO_DELETE, START_PIC
)
from helper_func import subscribed, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

# ✅ Branding change (neonfiles -> Rioshin)
from rioshin import script  # noqa: F401

# ✅ Branding variables (keep original logic)
file_auto_delete = humanize.naturaldelta(FILE_AUTO_DELETE)


# =========================
# Helper: Start UI
# =========================
async def send_start_ui(client: Client, message: Message):
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💖 Uᴘᴅᴀᴛᴇs", url="https://t.me/Botskingdoms"),
                InlineKeyboardButton("😎 Aʙᴏᴜᴛ", callback_data="about")
            ],
            [
                InlineKeyboardButton("👨‍💻 Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RioShin")
            ]
        ]
    )
    await message.reply_photo(
        photo=START_PIC,
        caption=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=reply_markup,
        quote=True
    )


# =========================
# Delete files helper
# =========================
async def delete_files(messages, client, k):
    await asyncio.sleep(FILE_AUTO_DELETE)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            print(f"Tʜᴇ Aᴛᴛᴇᴍᴘᴛ ᴛᴏ Dᴇʟᴇᴛᴇ Tʜᴇ Mᴇᴅɪᴀ {msg.id} Wᴀs Uɴsᴜᴄᴄᴇssғᴜʟ: {e}")
    await k.edit_text("<b><i>Yᴏᴜʀ Vɪᴅᴇᴏ / Fɪʟᴇ ɪs Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ ✅</i></b>")


@Bot.on_message(filters.command("start") & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    # user db
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except:
            pass

    # -------------------------
    # ✅ SAFE PAYLOAD PARSING
    # -------------------------
    text = (message.text or "").strip()
    base64_string = ""

    if " " in text:
        base64_string = text.split(" ", 1)[1].strip()

    # no payload => normal start
    if not base64_string:
        return await send_start_ui(client, message)

    # decode payload
    try:
        string = await decode(base64_string)
    except Exception:
        return await send_start_ui(client, message)

    # decode failed or invalid => normal start
    if not string or not isinstance(string, str):
        return await send_start_ui(client, message)

    argument = string.split("-")

    # -------------------------
    # rget- handler
    # -------------------------
    if string.startswith("rget-"):
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return await send_start_ui(client, message)

            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return await send_start_ui(client, message)
        else:
            return await send_start_ui(client, message)

        temp_msg = await message.reply("<b><i>Pʟᴇᴀsᴇ Wᴀɪᴛ...⚡</i></b>")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("<b><i>Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ...❌</i></b>")
            return
        await temp_msg.delete()

        sent_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) and bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                )
            else:
                caption = "" if not msg.caption else msg.caption.html

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                copied = await msg.copy(
                    chat_id=user_id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=True
                )
                sent_msgs.append(copied)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied = await msg.copy(
                    chat_id=user_id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=True
                )
                sent_msgs.append(copied)
            except:
                pass

        k = await client.send_message(
            chat_id=user_id,
            text=f"<b>❗️ <u><i>Iᴍᴘᴏʀᴛᴀɴᴛ</i></u> ❗️</b>\n\n"
                 f"<b><i>💢 Fɪʟᴇs Wɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ {file_auto_delete} (Dᴜᴇ ᴛᴏ Cᴏᴘʏʀɪɢʜᴛ Issᴜᴇs).\n\n"
                 f"💢 Sᴀᴠᴇ Tʜᴇsᴇ Fɪʟᴇs ᴛᴏ ʏᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Tʜᴇʀᴇ 📂</i></b>"
        )

        asyncio.create_task(delete_files(sent_msgs, client, k))
        return

    # -------------------------
    # Normal handler (non-rget)
    # -------------------------
    if len(argument) == 3:
        try:
            start = int(int(argument[1]) / abs(client.db_channel.id))
            end = int(int(argument[2]) / abs(client.db_channel.id))
        except:
            return await send_start_ui(client, message)

        if start <= end:
            ids = range(start, end + 1)
        else:
            ids = []
            i = start
            while True:
                ids.append(i)
                i -= 1
                if i < end:
                    break

    elif len(argument) == 2:
        try:
            ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        except:
            return await send_start_ui(client, message)
    else:
        return await send_start_ui(client, message)

    temp_msg = await message.reply("<b><i>Pʟᴇᴀsᴇ Wᴀɪᴛ...⚡</i></b>")
    try:
        messages = await get_messages(client, ids)
    except:
        await message.reply_text("<b><i>Sᴏᴍᴇᴛʜɪɴɢ Wᴇɴᴛ Wʀᴏɴɢ...❌</i></b>")
        return
    await temp_msg.delete()

    sent_msgs = []

    for msg in messages:
        if bool(CUSTOM_CAPTION) and bool(msg.document):
            caption = CUSTOM_CAPTION.format(
                previouscaption="" if not msg.caption else msg.caption.html,
                filename=msg.document.file_name
            )
        else:
            caption = "" if not msg.caption else msg.caption.html

        reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

        try:
            copied = await msg.copy(
                chat_id=user_id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT
            )
            sent_msgs.append(copied)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            copied = await msg.copy(
                chat_id=user_id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT
            )
            sent_msgs.append(copied)
        except:
            pass

    k = await client.send_message(
        chat_id=user_id,
        text=f"<b>❗️ <u><i>Iᴍᴘᴏʀᴛᴀɴᴛ</i></u> ❗️</b>\n\n"
             f"<b><i>💢 Fɪʟᴇs Wɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ {file_auto_delete} (Dᴜᴇ ᴛᴏ Cᴏᴘʏʀɪɢʜᴛ Issᴜᴇs).\n\n"
             f"💢 Sᴀᴠᴇ Tʜᴇsᴇ Fɪʟᴇs ᴛᴏ ʏᴏᴜʀ Sᴀᴠᴇᴅ Mᴇssᴀɢᴇs Aɴᴅ Dᴏᴡɴʟᴏᴀᴅ Tʜᴇʀᴇ 📂</i></b>"
    )

    asyncio.create_task(delete_files(sent_msgs, client, k))
    return


@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [[InlineKeyboardButton(text="Jᴏɪɴ Cʜᴀɴɴᴇʟ", url=client.invitelink)]]

    payload = ""
    if getattr(message, "command", None) and len(message.command) > 1:
        payload = (message.command[1] or "").strip()

    if payload:
        buttons.append(
            [InlineKeyboardButton(text="Tʀʏ Aɢᴀɪɴ", url=f"https://t.me/{client.username}?start={payload}")]
        )

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.command("users") & filters.private)
async def get_users(client: Bot, message: Message):
    msg = await message.reply_text("⏳ <b><i>Preparing User Data...</i></b>", quote=True)

    users = await full_userbase()
    total = len(users)

    await msg.edit(
        f"""
🌀 <b><i>User Analytics Update</i></b> 🌀

<b><i>👥 Total Registered Users:</b> {total}</i>
<b><i>🛰 System Status:</b> Active</i> ✅
<b><i>🧠 Data Source:</b> Real Time DB data</i>
"""
    )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if not message.reply_to_message:
        msg = await message.reply(
            "<b><i>Rᴇᴘʟʏ Tᴏ Aɴʏ Mᴇssᴀɢᴇ Aɴᴅ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ Tᴏ Bʀᴏᴀᴅᴄᴀsᴛ 🔊.</i></b>",
            quote=True
        )
        await asyncio.sleep(8)
        await msg.delete()
        return

    query = await full_userbase()
    broadcast_msg = message.reply_to_message

    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await message.reply("<i><b>⏰ Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Yᴏᴜʀ Mᴇssᴀɢᴇs</b></i>", quote=True)

    for chat_id in query:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""<b><u><i>🎯 Bʀᴏᴀᴅᴄᴀsᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ Nɪᴄᴇʟʏ</i></u></b>

<b><i>👥 Tᴏᴛᴀʟ ᴜsᴇʀs</b> : {total}</i>
<b><i>✅ Sᴜᴄᴄᴇssғᴜʟ</b> : {successful}</i>
<b><i>🚫 Bʟᴏᴄᴋᴇᴅ Usᴇʀs</b> : {blocked}</i>
<b><i>🚮 Dᴇᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛs</b> : {deleted}</i>
<b><i>☢️ Uɴsᴜᴄᴄᴇssғᴜʟ</b> : {unsuccessful}</i>"""

    await pls_wait.edit(status)
