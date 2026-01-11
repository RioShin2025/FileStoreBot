# ---------------------------------------------------
# File Name: Database.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# YouTube: https://youtube.com/@MyselfNeon
# Created: 2025-10-21
# Last Modified: 2025-10-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

import pymongo, os, json
from config import DB_URL, DB_NAME

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]
user_data = database['users']


async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)


async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return


async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids


async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

admins = set()

def add_admin(user_id: int):
    admins.add(int(user_id))

def remove_admin(user_id: int):
    admins.discard(int(user_id))

def get_all_admins():
    return list(admins)
    
_ADMINS_FILE = "admins.json"

def _load_admins():
    if not os.path.exists(_ADMINS_FILE):
        return []
    with open(_ADMINS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def _save_admins(admins):
    with open(_ADMINS_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(set(admins))), f)

def add_admin(user_id: int):
    admins = _load_admins()
    if user_id not in admins:
        admins.append(user_id)
    _save_admins(admins)

def remove_admin(user_id: int):
    admins = _load_admins()
    admins = [x for x in admins if x != user_id]
    _save_admins(admins)

def get_all_admins():
    return _load_admins()
# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
