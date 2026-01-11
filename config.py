# ---------------------------------------------------
# File Name: Config.py
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
import logging

# --- Bot Credentials --- #
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
API_ID = int(os.environ.get("API_ID", "20366634"))
API_HASH = os.environ.get("API_HASH", "72095ec36984aa9ceb0dbaa9cec31559")

OWNER_ID = int(os.environ.get("OWNER_ID", "8476571786"))
DB_URL = os.environ.get("DB_URL", "mongodb+srv://botskingdom1:gf3vWBaZi5hKwWd0@cluster0.7tu4jk0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "FileStoreRioShin")

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003383795299"))
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003383795299"))
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1003383795299"))

FILE_AUTO_DELETE = int(os.environ.get("FILE_AUTO_DELETE", "300"))  # auto delete in seconds
PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
SHORT_URL = "arolinks.com"      # without https://
SHORT_API = "2ad041b1b4f8ce90b3ecadbbedbc904709bc8138"
SHORTENER_ENABLED = True

# --- Admins --- #
ADMINS = [8476571786]
try:
    for x in os.environ.get("ADMINS", "841851780").split():
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")
ADMINS.append(OWNER_ID)

SUPER_PREMIUM_USERS = [8476571786, 987654321]
# --- Bot Messages --- #
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False") == "True"
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "True") == "True"

BOT_UPTIME_TEXT = "<b><i>Bᴏᴛ Uᴘᴛɪᴍᴇ</i> :</b>\n{uptime}"
USER_REPLY_TEXT = "<b><i>Baka !! You are not my Senpai 😏</i></b>"

START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b><i>Hᴇʟʟᴏ {mention} ✨ \n\nI ᴀᴍ Pᴇʀᴍᴀɴᴇɴᴛ Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ.\n"
    "Dᴇᴠᴇʟᴏᴘᴇᴅ Bʏ <a href=\"tg://user?id=841851780\">NᴇᴏɴAɴᴜʀᴀɢ</a>.\n\n"
    "Gᴇᴛ Rᴇᴅɪʀᴇᴄᴛᴇᴅ Fʀᴏᴍ Cᴏʀʀᴇᴄᴛ Lɪɴᴋs Tᴏ Gᴇᴛ Tʜᴇ Fɪʟᴇs 🖇️</i></b>"
)

START_PIC = os.environ.get("START_PIC", "https://files.catbox.moe/6e5mpx.jpg")

FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE",
    "<b><i>🚫 Aᴄᴄᴇss Rᴇsᴛʀɪᴄᴛᴇᴅ 🚫\n\n"
    "Tᴏ Usᴇ Tʜɪs ʙᴏᴛ ᴀɴᴅ Aᴄᴄᴇss Fɪʟᴇs ᴏʀ Fᴇᴀᴛᴜʀᴇs, ʏᴏᴜ Nᴇᴇᴅ ᴛᴏ Bᴇ ᴀ Pᴀʀᴛ ᴏғ Oᴜʀ Mᴀɪɴ Cʜᴀɴɴᴇʟ 🗓️</i></b>"
)

# --- Logging (Console only) --- #
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# --- Keep-Alive URL --- #
KEEP_ALIVE_URL = os.environ.get("KEEP_ALIVE_URL", "")


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
