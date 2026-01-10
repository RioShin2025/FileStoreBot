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

import os
import sys
import asyncio
from pyrogram import filters
from bot import Bot
from config import OWNER_ID

# === CONFIG ===
MYSELFNEON = [OWNER_ID]  # Uses OWNER_ID from config.py
TEMP_FOLDERS = ["downloads", "temp"]

ongoing_tasks = []

def track_task(task: asyncio.Task):
    ongoing_tasks.append(task)
    task.add_done_callback(lambda t: ongoing_tasks.remove(t))

@Bot.on_message(filters.command("restart") & filters.user(MYSELFNEON))
async def restart_bot(client, message):
    # Send initial message
    msg = await message.reply_text("♻️ Restart initiated...\n\nStarting process:",quote=True)

    steps = [
        "⏳ Cancelling all ongoing tasks...",
        "🗑 Clearing temporary folders...",
        "🔄 Restarting bot..."
    ]

    # Step 1: Cancel all ongoing tasks
    await asyncio.sleep(0.5)
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[0]}")
    for task in ongoing_tasks[:]:
        task.cancel()
    ongoing_tasks.clear()
    await asyncio.sleep(1)

    # Step 2: Clear temp folders
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[1]}")
    for folder in TEMP_FOLDERS:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                try:
                    os.remove(os.path.join(folder, file))
                except Exception:
                    pass
    await asyncio.sleep(1)

    # Step 3: Restart bot
    await msg.edit_text(f"♻️ Restart initiated...\n\n{steps[2]}")
    await asyncio.sleep(1)

    # ✅ Delete the message before restarting
    try:
        await msg.delete()
    except:
        pass

    # Hard restart
    os.execv(sys.executable, [sys.executable] + sys.argv)


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
