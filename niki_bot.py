# ==============dequeMONGO SETUP (FINAL CLEAN) =================
from pymongo import MongoClient

MONGO_URL = "mongodb+srv://vishal:VISHAL123@vishal07.espy0qo.mongodb.net/?appName=Vishal07"

client = MongoClient(MONGO_URL)

# ========= 1️⃣ MAIN DATA (BALANCE, BACKUP) =========
db_main = client["mydatabase"]
backup = db_main["backup"]   # ⚡ IMPORTANT (error fix)
col = db_main["chats"]       # groups/users save  ✅ (IMPORTANT)
filters_col = db_main["filters"]



# =================== WEB SERVER (RENDER FIX) ===================

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Handler(BaseHTTPRequestHandler):

    # ✅ GET request
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    # ✅ HEAD request FIX (UptimeRobot)
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)

    print(f"🌐 Web server running on port {port}")

    server.serve_forever()

# ✅ Daemon thread
threading.Thread(target=run_web, daemon=True).start()


# =================== IMPORTS ===================
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatPermissions, Update
from datetime import datetime, timedelta
from collections import deque
from openai import OpenAI
from deep_translator import GoogleTranslator
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import json
import time
import random
import os
import re

# =================== GLOBALS ===================
kill_cooldown = {}
rob_cooldown = {}


# =================== BOT TOKEN =======================
BOT_TOKEN= "8614646410:AAEDw9e9dJLxeElsixxCfolh2yrn8pBjxD4"
BOT_USERNAME= "@iim_Nikibot"
# =================== DATABASE FILE ===================
DATABASE_FILE = "database.json"

# =================== HELPERS ===================
# =================== START COMMAND ===================
# =================== START COMMAND ===================
# =================== START COMMAND ===================

# =================== START COMMAND ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_bot_active(update, context):
        return
    
    user = update.effective_user
    chat = update.effective_chat

    # ✅ SAVE USER / GROUP
    col.update_one(
        {"chat_id": chat.id},
        {"$set": {"chat_id": chat.id, "type": chat.type}},
        upsert=True
    )

    uid = str(user.id)

    if uid not in data:
        data[uid] = {"name": user.first_name, "money": 1000, "kills": 0}
        save_data()
        

    welcome_text = (
        f"👋 Hᴇʟʟᴏ {user.first_name}!\n\n"
        "💝 Mʏ Nᴀᴍᴇ Iꜱ Nɪᴋɪ\n"
        "Wᴇʟᴄᴏᴍᴇ Tᴏ Nɪᴋɪ'ꜱ Wᴏʀʟᴅ 🌸\n\n"
        "I'ᴍ Nᴏᴛ Jᴜꜱᴛ A Bᴏᴛ…\n"
        "I'ᴍ Yᴏᴜʀ Vɪʀᴛᴜᴀʟ Gɪʀʟ 😌✨\n\n"
        "💰 Eᴀʀɴ Mᴏɴᴇʏ\n"
        "⚔ Fɪɢʜᴛ Eɴᴇᴍɪᴇꜱ\n"
        "😈 Rᴏʙ Pᴇᴏᴘʟᴇ\n"
        "🛡 Pʀᴏᴛᴇᴄᴛ Yᴏᴜʀꜱᴇʟꜰ\n"
        "🏆 Cʟɪᴍʙ Tʜᴇ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ\n\n"
        "❗ Nɪᴋɪ Iꜱ Aʟᴡᴀʏꜱ Wᴀᴛᴄʜɪɴɢ Yᴏᴜ 👀🔥\n\n"
        "⚡ Tʏᴘᴇ /economy Tᴏ Sᴇᴇ Aʟʟ Cᴏᴍᴍᴀɴᴅꜱ\n\n"
        "👑 Oᴡɴᴇʀ: @YTT_BISHAL"
    )

    # ✅ Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/YTT_BISHAL"),
            InlineKeyboardButton("🎮 Game", callback_data="start_game")
        ],
        [
            InlineKeyboardButton("➕ Add me", url="https://t.me/iim_Nikibot?startgroup=true")
        ]
    ]

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# =================== CALLBACK HANDLER FOR GAME & BACK ===================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # ❌ Skip other systems
    if data.startswith("marry_") or data.startswith("duel_"):
        return

    # ================= GAME MENU =================
    if data == "start_game":
        keyboard = [
            [
                InlineKeyboardButton("💰 Economy", callback_data="start_economy"),
                InlineKeyboardButton("❓ Help", callback_data="start_help")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="start_back")
            ]
        ]

        await query.edit_message_text(
            "🎲 Game Menu:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "start_economy":
        economy_text = (
                       "💰 *Nɪᴋɪ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Oᴠᴇʀᴠɪᴇᴡ*\n\n"
                      "💬 *Hᴏᴡ Iᴛ Wᴏʀᴋꜱ:*\n"
                      "Uꜱᴇ Nɪᴋɪ’ꜱ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Tᴏ Eᴀʀɴ, Mᴀɴᴀɢᴇ, Gɪꜰᴛ, Aɴᴅ Pʀᴏᴛᴇᴄᴛ Vɪʀᴛᴜᴀʟ Mᴏɴᴇʏ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ.\n\n"
                      "• /daily — Cʟᴀɪᴍ $1500 Dᴀɪʟʏ Rᴇᴡᴀʀᴅ\n"
                      "• /claim — Uɴʟᴏᴄᴋ Gʀᴏᴜᴘ Rᴇᴡᴀʀᴅꜱ Bᴀꜱᴇᴅ Oɴ Mᴇᴍʙᴇʀꜱ\n"
                      "• /bal — Cʜᴇᴄᴋ Yᴏᴜʀ Oʀ Aɴᴏᴛʜᴇʀ Uꜱᴇʀ’ꜱ Bᴀʟᴀɴᴄᴇ\n"
                      "• /rob (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Rᴏʙ Mᴏɴᴇʏ Fʀᴏᴍ A Uꜱᴇʀ\n"
                      "• /kill (ʀᴇᴘʟʏ) — Kɪʟʟ A Uꜱᴇʀ & Eᴀʀɴ $200–$600\n"
                      "• /revive — Rᴇᴠɪᴠᴇ Yᴏᴜʀꜱᴇʟꜰ Oʀ A Rᴇᴘʟɪᴇᴅ Uꜱᴇʀ\n"
                      "• /protect 1ᴅ|2ᴅ|3ᴅ — Bᴜʏ Pʀᴏᴛᴇᴄᴛɪᴏɴ Fʀᴏᴍ Rᴏʙʙᴇʀʏ\n"
                      "• /give (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Tʀᴀɴꜱꜰᴇʀ Mᴏɴᴇʏ\n"
                      "• /shop — Sʜᴏᴘ Fᴏʀ Gɪꜰᴛ Iᴛᴇᴍꜱ\n"
                      "• /items (ʀᴇᴘʟʏ) — Vɪᴇᴡ Yᴏᴜʀ / Oᴛʜᴇʀꜱ Iɴᴠᴇɴᴛᴏʀʏ\n"
                      "• /toprich — Tᴏᴘ 10 Rɪᴄʜᴇꜱᴛ Uꜱᴇʀꜱ\n"
                      "• /topkill — Tᴏᴘ 10 Kɪʟʟᴇʀꜱ\n"
                      "• /check — Cʜᴇᴄᴋ Pʀᴏᴛᴇᴄᴛɪᴏɴ Sᴛᴀᴛᴜꜱ (Cᴏꜱᴛꜱ $2000)\n"

        )
        keyboard = [
            [InlineKeyboardButton("🔙 Back", callback_data="start_back")]
        ]
        await query.edit_message_text(
            economy_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "start_help":
        help_text = "💡 Help ke liye apna owner dekho 👑"
        keyboard = [
            [InlineKeyboardButton("👑 Owner", url="https://t.me/YTT_BISHAL")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_game")]
        ]

        await query.edit_message_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "start_back":
        user = query.from_user

        welcome_text = (
            f"👋 Hᴇʟʟᴏ {user.first_name}!\n\n"
            "💝 Mʏ Nᴀᴍᴇ Iꜱ Nɪᴋɪ\n"
            "Wᴇʟᴄᴏᴍᴇ Tᴏ Nɪᴋɪ'ꜱ Wᴏʀʟᴅ 🌸\n\n"
            "I'ᴍ Nᴏᴛ Jᴜꜱᴛ A Bᴏᴛ…\n"
            "I'ᴍ Yᴏᴜʀ Vɪʀᴛᴜᴀʟ Gɪʀʟ 😌✨\n\n"
            "💰 Eᴀʀɴ Mᴏɴᴇʏ\n"
            "⚔ Fɪɢʜᴛ Eɴᴇᴍɪᴇꜱ\n"
            "😈 Rᴏʙ Pᴇᴏᴘʟᴇ\n"
            "🛡 Pʀᴏᴛᴇᴄᴛ Yᴏᴜʀꜱᴇʟꜰ\n"
            "🏆 Cʟɪᴍʙ Tʜᴇ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ\n\n"
            "❗ Nɪᴋɪ Iꜱ Aʟᴡᴀʏꜱ Wᴀᴛᴄʜɪɴɢ Yᴏᴜ 👀🔥\n\n"
            "⚡ Tʏᴘᴇ /economy Tᴏ Sᴇᴇ Aʟʟ Cᴏᴍᴍᴀɴᴅꜱ\n\n"
            "👑 Oᴡɴᴇʀ: @YTT_BISHAL"
        )

        keyboard = [
            [
                InlineKeyboardButton("👑 Owner", url="https://t.me/YTT_BISHAL"),
                InlineKeyboardButton("🎮 Game", callback_data="start_game")
            ],
            [
                InlineKeyboardButton("➕ Add me", url="https://t.me/iim_Nikibot?startgroup=true")
            ]
        ]


        await query.edit_message_text(
            welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
            )

    
# =================== TOP RICHEST COMMAND ===================
async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_bot_active(update, context):
        return
    

    # ✅ sirf real users filter karo
    users_only = {
        uid: u for uid, u in data.items()
        if isinstance(u, dict) and "money" in u
    }

    if not users_only:
        await update.message.reply_text("❌ No data found!")
        return

    sorted_rich = sorted(users_only.items(), key=lambda x: x[1]["money"], reverse=True)[:10]

    msg = "🏆 Top 10 Richest Users:\n\n"
    for idx, (uid, user) in enumerate(sorted_rich, 1):
        msg += f"{idx}. {user.get('name','Unknown')} — ₹{user.get('money',0)}\n"

    await update.message.reply_text(msg)
# =================== TOP KILLERS COMMAND ===================
async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_bot_active(update, context):
        return

    users_only = {
        uid: u for uid, u in data.items()
        if isinstance(u, dict) and "kills" in u
    }

    if not users_only:
        await update.message.reply_text("❌ No data found!")
        return

    sorted_kills = sorted(users_only.items(), key=lambda x: x[1]["kills"], reverse=True)[:10]

    msg = "⚔ Top 10 Killers:\n\n"
    for idx, (uid, user) in enumerate(sorted_kills, 1):
        msg += f"{idx}. {user.get('name','Unknown')} — {user.get('kills',0)} kills\n"

    await update.message.reply_text(msg)


# ===================== PART 2 FULL ECONOMY BOT =====================
# ------------------ GLOBAL DATA ------------------
DATA_FILE = "database.json"
jail_users = {}
rob_cooldown = {}
kill_cooldown = {}
temp_rob = {}

OWNER_ID = 6175559434  # Apna Telegram ID
#====================load/save===================

def load_data():
    global data, shop_items

    mongo_data = load_from_mongo()

    if mongo_data:
        print("✅ Data loaded from Mongo")
        data = mongo_data
    else:
        print("⚠️ Mongo empty, loading JSON")
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
            else:
                data = {}
        except:
            data = {}

    # shop items
    if "shop_items" in data:
        for name in shop_items:
            if name in data["shop_items"]:
                shop_items[name]["gifs"] = data["shop_items"][name].get("gifs", [])
                
def load_from_mongo():
    result = backup.find_one({"_id": "main_data"})
    
    if result and "data" in result:
        return result["data"]
    
    return {}
    
def save_data():
    global data

    # 🔥 CLEAN DATA (only safe types)
    safe_data = {}

    for k, v in data.items():
        if isinstance(v, (dict, list, str, int, float, bool)):
            safe_data[k] = v

    # JSON save (optional)
    with open(DATA_FILE, "w") as f:
        json.dump(safe_data, f, indent=2)

    # 🔥 MongoDB save
    backup.update_one(
        {"_id": "main_data"},
        {"$set": {"data": safe_data}},
        upsert=True
    )
# ------------------ USER HELP ------------------

def get_user(user_id, name):
    global data
    uid = str(user_id)

    if uid not in data:
        data[uid] = {
            "name": name,
            "money": 1000,
            "kills": 0,
            "inventory": {},
            "dead": False,
            "dead_until": 0,
            "protection_until": 0,
            "last_daily": 0
        }
        save_data()
        

    return data[uid]   # ✅ correct

    
def format_time(sec):
    sec = int(sec)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h}h {m}m {s}s"
# ------------------ PROTECTION CHECK ------------------
def is_protected(user_data):
    now = time.time()
    return user_data.get("protection_until", 0) > now
# ------------------ DAILY COMMAND ------------------
# ------------------ DAILY COMMAND ------------------
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if not await check_bot_active(update, context):
        return

    user = get_user(update.effective_user.id, update.effective_user.first_name)

    now = time.time()

    if now - user.get("last_daily", 0) < 86400:
        remain = 86400 - (now - user.get("last_daily", 0))

        await update.message.reply_text(
            f"⏳ Daily already claimed. Try after {format_time(remain)}"
        )
        return

    # 💰 MONEY
    user["money"] += 1500

    # update time
    user["last_daily"] = now

    save_data()
    

    # ✅ FINAL MESSAGE (ONLY ONE)
    await update.message.reply_text(
        "💰 Daily reward: ₹1500\nNext daily available after 24h"
    )

    
# ------------------ BALANCE COMMAND ------------------

# ------------------ BALANCE COMMAND ------------------

# ------------------ BALANCE COMMAND ------------------

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if not await check_bot_active(update, context):
        return

    if update.message and update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    else:
        target_user = update.effective_user

    user_data = get_user(target_user.id, target_user.first_name)
    
    # ✅ sirf real users filter karo
    users_only = {
        uid: u for uid, u in data.items()
        if isinstance(u, dict) and "money" in u
    }

    sorted_users = sorted(users_only.items(), key=lambda x: x[1]["money"], reverse=True)

    rank = next((i+1 for i,(uid,u) in enumerate(sorted_users) if uid==str(target_user.id)), "N/A")

    status_text = "Alive ❤️" if not user_data.get("dead", False) else "Dead ☠️"

    await update.message.reply_text(
        f"┏━━━ 💼 PROFILE ━━━\n"
        f"👤 Name   : {target_user.first_name}\n"
        f"💰 Bal    : ₹{user_data.get('money',0)}\n"
        f"🏆 Rank   : {rank}\n"
        f"❤️ Status : {status_text}\n"
        f"⚔ Kills  : {user_data.get('kills',0)}\n"
        f"┗━━━━━━━━━━━━━━━"
    )
# ------------------ PROTECT COMMAND ------------------
async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    user = get_user(update.effective_user.id, update.effective_user.first_name)
    now = time.time()
    cost_map = {"1d":(800,86400), "2d":(1000,172800), "3d":(2000,259200)}
    if not context.args:
        await update.message.reply_text("👑 Vishal Boss kya keh rahe hai suno 😎🔥\n"
                                         "/protect 1d -->> ₹800\n"
                                         "/protect 2d -->> ₹1000\n"
                                         "/protect 3d -->> ₹2000\n"

                                      "👍 Ye Vishal Boss ka hukum he, follow karo!\n")
        return
    choice = context.args[0].lower()
    if choice not in cost_map:
        await update.message.reply_text("❌ Invalid option! Use 1d,2d,3d")
        return
    cost, duration = cost_map[choice]
    if user.get("protection_until",0) > now:
        rem = user["protection_until"] - now
        await update.message.reply_text(f"🛡You are already protected for {format_time(rem)} more")
        return
    if user["money"] < cost:
        await update.message.reply_text("💸 Paisa kam hai!")
        return
    user["money"] -= cost
    user["protection_until"] = now + duration
    save_data()
    
    await update.message.reply_text(f"🛡 Protection enabled for {choice}")

# ------------------ CLAIM GROUP ------------------
# ------------------ CLAIM GROUP ------------------
async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    

    chat = update.effective_chat
    user = update.effective_user

    # Only group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ Works in groups only")
        return

    # 🔥 Ensure claimed_groups exists in data
    if "claimed_groups" not in data:
        data["claimed_groups"] = {}

    # Already claimed check (PERMANENT)
    if str(chat.id) in data["claimed_groups"]:
        await update.message.reply_text("⚠️ This group has already claimed rewards")
        return

    # Member count
    try:
        members_count = await chat.get_member_count()
    except:
        members_count = 0

    # ❌ Minimum 100 members required
    if members_count < 100:
        await update.message.reply_text("❌ 100 members hone chahiye claim ke liye!")
        return

    # 💰 Reward logic
    if members_count >= 1000:
        reward = 30000
    elif members_count >= 500:
        reward = 20000
    else:
        reward = 10000

    # User data
    user_data = get_user(user.id, user.first_name)
    user_data["money"] += reward

    # 🔥 SAVE CLAIM PERMANENTLY (GROUP LOCK)
    data["claimed_groups"][str(chat.id)] = {
        "claimed_by": user.id,
        "reward": reward
    }

    save_data()
    

    await update.message.reply_text(
        f"💰 {user.first_name} claimed {reward} coins for this group!\n"
        f"⚠️ Ab is group me dubara kabhi claim nahi hoga!"
    )




#===================register=====================


# ------------------ ROB COMMAND ------------------
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    now = time.time()

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply karke rob karo!")
        return

    robber = update.message.from_user
    victim = update.message.reply_to_message.from_user

    robber_data = get_user(robber.id, robber.first_name)
    victim_data = get_user(victim.id, victim.first_name)

    robber_id = str(robber.id)
    victim_id = str(victim.id)

    # ⛓ Jail check
    if robber_id in jail_users:
        if now < jail_users[robber_id]:
            fine = 500
            robber_data["money"] -= fine
            jail_users[robber_id] += 120
            save_data()
            

            await update.message.reply_text(
                f"🚨 Jail me hoke chori karega?! 😡⛓\n"
                f"💸 ₹{fine} aur kat gaya tumhara!\n"
                f"⛓ Tum aur 2 minute jail me rahoge!\n"
                f"👑 Vishal Boss ko inform kar diya police ne! 🚔\n"
                f"💰 ₹1000 dekar bail le sakte ho.\n(Command: /bail)\n\n"
                f"🕒 Ab tum {int(jail_users[robber_id]-now)//60} minute {int(jail_users[robber_id]-now)%60} second baad bahar aaoge 😈"
            )
            return
        else:
            del jail_users[robber_id]

    # Self rob
    if robber.id == victim.id:
        await update.message.reply_text("🤡 Khud ko rob nahi kar sakte!")
        return

    # Owner protection
    if victim.id == OWNER_ID:
        await update.message.reply_text("☠️ Owner ko rob nahi kar sakte.. ☠️")
        return

    # Bot check
    if victim.is_bot:
        await update.message.reply_text("🤖 Bot ko rob nahi kar sakte!")
        return

    # Protection check
    if is_protected(victim_data):
        await update.message.reply_text(f"🛡 {victim.first_name} abhi protected hai!")
        return

    # Cooldown check
    if robber_id in rob_cooldown and now < rob_cooldown[robber_id]:
        await update.message.reply_text("⏱ Rob cooldown active! Wait 6 sec")
        return

    # Victim money check
    if victim_data["money"] <= 0:
        await update.message.reply_text("Victim ke paas paisa nahi hai!")
        return
# Amount check
# Amount check
    if not context.args:
        await update.message.reply_text(
            "⚠️ Amount likho!\n\nExample:\n/rob 1000"
        )
        return
    else:
        try:
            amount = int(context.args[0])
            if amount <= 0:
                raise ValueError
            stolen = min(amount, victim_data["money"], 100000)
        except:
            await update.message.reply_text("Invalid amount!")
            return

    # Save original balance for restore
    if victim_id not in temp_rob:
        temp_rob[victim_id] = {
            "original_balance": victim_data["money"],
            "restore_time": now + 86400
        }

    # 🚔 30% police chance
    if random.random() < 0.3:
        fine = 300
        robber_data["money"] -= fine
        victim_data["money"] += fine

        jail_users[robber_id] = now + 180
        rob_cooldown[robber_id] = now + 6

        save_data()
        

        await update.message.reply_text(
            f"🚔 Police ne pakad liya!\n"
            f"💸 ₹{fine} fine!\n"
            f"⛓ 3 min jail\n"
            f"💰 Robbery fail!"
        )
        return

    # Successful rob
    victim_data["money"] -= stolen
    robber_data["money"] += stolen

    rob_cooldown[robber_id] = now + 6

    save_data()
    

    
    try:
        await update.message.reply_text(
            f"👤 {robber.first_name} robbed ₹{stolen} from {victim.first_name}\n"
            f"💰 {victim.first_name}'s balance: ₹{victim_data['money']}\n"
            f"💰 {robber.first_name}'s balance: ₹{robber_data['money']}"
        ) 
    except Exception as e:
        print("ROB ERROR:", e)
# ------------------ KILL COMMAND ------------------
# ------------------ KILL COMMAND ------------------
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    print("KILL START")

    

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to someone to kill.")
        return

    killer = update.effective_user
    victim = update.message.reply_to_message.from_user
    now = time.time()

    killer_data = get_user(killer.id, killer.first_name)
    victim_data = get_user(victim.id, victim.first_name)

    # 🔥 SAFETY FIX (IMPORTANT)

    # Auto revive
    if killer_data.get("dead", False):
        if now >= killer_data.get("dead_until", 0):
            killer_data["dead"] = False
            killer_data["dead_until"] = 0
            save_data()
            
        else:
            await update.message.reply_text("💀 Tum already dead ho! 24hr baad revive hoga 😢")
            return

    if victim_data.get("dead", False):
        if now >= victim_data.get("dead_until", 0):
            victim_data["dead"] = False
            victim_data["dead_until"] = 0
            save_data()
            
        else:
            await update.message.reply_text(
                "😂 Wow beta! Wo already dead hai ☠️\n"
                "Kisi aur ko try karo 😎"
            )
            return

    # Bot owner / self / bot checks
    if victim.id == OWNER_ID:
        await update.message.reply_text("☠️ Owner ko kill nahi kar sakte 😎 vo pesa ka malik he ☠️")
        return

    if victim.is_bot:
        await update.message.reply_text(
            f"😼 Meri billi mujhe meow?\n"
            f"Mujhe kill karoge? No chalakii 😌\n"
            f"Mere Owner se bol dunga 😏\n"
            f"👉 https://t.me/YTT_BISHAL\n"
        )
        return

    if killer.id == victim.id:
        await update.message.reply_text("🤡 Khud ko kill nahi kar sakte!")
        return

    if is_protected(victim_data):
        await update.message.reply_text(f"🛡 {victim.first_name} abhi protected hai!")
        return

    if str(killer.id) in kill_cooldown and now < kill_cooldown[str(killer.id)]:
        await update.message.reply_text("⏳ Wait 6 seconds before killing again!")
        return

    # 🔥 KILL LOGIC
    victim_data["dead"] = True
    victim_data["dead_until"] = now + 86400

    reward = random.randint(200, 600)
    killer_data["money"] = killer_data.get("money", 1000) + reward
    killer_data["kills"] = killer_data.get("kills", 0) + 1

    # cooldown + save
    kill_cooldown[str(killer.id)] = now + 6
    save_data()
    

    # ✅ SAME MESSAGE (UNCHANGED)
    
    try:
        await update.message.reply_text(
            f"☠️ {killer.first_name} killed {victim.first_name}!\n"
            f"💰 Earned: ₹{reward}\n"
            f"⏳ Victim 24hr baad revive hoga!"
        )
    except Exception as e:
        print("KILL ERROR:", e)

# ------------------ BAIL COMMAND ------------------
# ------------------ BAIL COMMAND ------------------
async def bail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    user = update.effective_user
    user_id = str(user.id)
    now = time.time()

    # ❌ Not in jail
    if user_id not in jail_users:
        await update.message.reply_text("😎 Tum jail me nahi ho!")
        return

    # ✅ Auto free if time completed
    if now >= jail_users[user_id]:
        del jail_users[user_id]
        save_data()
        
        await update.message.reply_text("😎 Tum already free ho!")
        return

    user_data = get_user(user.id, user.first_name)

    # 💸 Not enough money
    if user_data["money"] < 1000:
        await update.message.reply_text("₹1000 chahiye bail ke liye!")
        return

    # 💰 Deduct money
    user_data["money"] -= 1000

    # 🔓 Remove jail
    del jail_users[user_id]

    save_data()
    

    await update.message.reply_text("💸 Bail mil gayi! Ab free ho 😈")


# ================= SHOP & GIFT COMMANDS (Part 1 JSON style) =================

# ---------------- DATA STORAGE ----------------
DATA_FILE = "database.json"


# ---------------- SHOP ITEMS ----------------
shop_items = {
    "rose": {"emoji": "🌹", "price": 500},
    "chocolate": {"emoji": "🍫", "price": 800},
    "ring": {"emoji": "💍", "price": 2000},
    "teddy": {"emoji": "🧸", "price": 1500},
    "pizza": {"emoji": "🍕", "price": 600},
    "surprise_box": {"emoji": "🎁", "price": 2500},
    "puppy": {"emoji": "🐶", "price": 3000},
    "cake": {"emoji": "🎂", "price": 1000},
    "love_letter": {"emoji": "💌", "price": 400},
    "cat": {"emoji": "🐱", "price": 2500},
}

# ---------------- GIF STORAGE ----------------
for name in shop_items:
    if "gifs" not in shop_items[name]:
        shop_items[name]["gifs"] = []

# ---------------- MESSAGES ----------------
def make_messages(name):
    nice = name.replace("_"," ").title()
    return [
        f"Ye {nice} sirf tumhare liye ❤️",
        f"Ek pyarisi {nice} tumhare naam 💖",
        f"Dil se bheja {nice} 💕",
        f"Tumhari smile ke liye {nice} 😁",
        f"Special {nice} just for you 😍",
        f"Ek cute {nice} gift 💖",
        f"Surprise {nice} 🎁",
        f"Tum sabse special ho ❤️",
        f"Pyar bhara {nice} 😘",
        f"Ek choti si khushi 💝",
    ]

gift_messages = {name: make_messages(name) for name in shop_items}





DATA_FILE = "database.json"

# ---------------- ADD GIF ----------------
async def addgif(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("GIF ko reply karo aur /addgif rose likho")
        return

    msg = update.message.reply_to_message

    file_id = None

    if msg.animation:
        file_id = msg.animation.file_id
    elif msg.document:
        file_id = msg.document.file_id
    else:
        await update.message.reply_text("Ye GIF nahi hai")
        return
        
    if len(context.args) == 0:
        await update.message.reply_text("Example: /addgif rose")
        return

    gift_name = context.args[0].lower()

    if gift_name not in shop_items:
        await update.message.reply_text("Invalid gift name")
        return

    file_id = update.message.reply_to_message.animation.file_id

    # duplicate GIF check
    if file_id in shop_items[gift_name]["gifs"]:
        await update.message.reply_text("⚠️ Ye GIF already add hai")
        return

    # GIF add
    shop_items[gift_name]["gifs"].append(file_id)

    # SAVE DATA
    #..yahape load data add krna he yadi higa toh
    data["shop_items"] = shop_items
    save_data()
    

    total = len(shop_items[gift_name]["gifs"])

    await update.message.reply_text(
        f"✅ GIF added to {gift_name}\nTotal GIFs: {total}"
    )





# ---------------- SHOP COMMAND ----------------
async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    text = "🛒 ITEM SHOP\n━━━━━━━━━━━━━━\n"
    for name, item in shop_items.items():
        text += f"• {item['emoji']} {name.title()} : ₹{item['price']}\n"
    text += "\nReply to a user and use /gift <amount> to send!"
    await update.message.reply_text(text)

# ---------------- GIFT COMMAND ----------------
# ---------------- GIFT COMMAND ----------------
# ---------------- GIFT COMMAND ----------------
async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply karke /gift <amount> likho")
        return

    if len(context.args) == 0:
        await update.message.reply_text("Example: /gift 500")
        return

    try:
        amount = int(context.args[0])
    except:
        await update.message.reply_text("Valid amount likho")
        return

    giver = update.effective_user
    receiver = update.message.reply_to_message.from_user

    gift_name = None
    for name, item in shop_items.items():
        if item["price"] == amount:
            gift_name = name
            break

    if not gift_name:
        await update.message.reply_text("Invalid gift amount")
        return

    if len(shop_items[gift_name]["gifs"]) == 0:
        await update.message.reply_text("Is gift ke GIF abhi add nahi hue")
        return

    giver_data = get_user(giver.id, giver.first_name)
    receiver_data = get_user(receiver.id, receiver.first_name)

    if giver_data["money"] < amount:
        await update.message.reply_text("Paisa kam hai 😢")
        return

    chosen_gif = random.choice(shop_items[gift_name]["gifs"])
    chosen_msg = random.choice(gift_messages[gift_name])

    giver_data["money"] -= amount

    receiver_data["inventory"][gift_name] = receiver_data["inventory"].get(gift_name, 0) + 1

    save_data()
    

    emoji = shop_items[gift_name]["emoji"]

    final_text = (
        f"Oye {receiver.first_name} tereko {giver.first_name} ne ek pyaarisi gift bheja "
        f"{emoji} {gift_name.replace('_',' ').title()} 💖\n\n"
        f"{chosen_msg}"
    )

    await update.message.reply_animation(
        animation=chosen_gif,
        caption=final_text
    )
# ================= ECONOMY COMMAND =================
from telegram import Update
from telegram.ext import ContextTypes
async def economy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    text = (
         "💰 *Nɪᴋɪ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Oᴠᴇʀᴠɪᴇᴡ*\n\n"
       "💬 *Hᴏᴡ Iᴛ Wᴏʀᴋꜱ:*\n"
       "Uꜱᴇ Nɪᴋɪ’ꜱ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Tᴏ Eᴀʀɴ, Mᴀɴᴀɢᴇ, Gɪꜰᴛ, Aɴᴅ Pʀᴏᴛᴇᴄᴛ Vɪʀᴛᴜᴀʟ Mᴏɴᴇʏ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ.\n\n"
       "• /daily — Cʟᴀɪᴍ $1500 Dᴀɪʟʏ Rᴇᴡᴀʀᴅ\n"
       "• /claim — Uɴʟᴏᴄᴋ Gʀᴏᴜᴘ Rᴇᴡᴀʀᴅꜱ Bᴀꜱᴇᴅ Oɴ Mᴇᴍʙᴇʀꜱ\n"
       "• /bal — Cʜᴇᴄᴋ Yᴏᴜʀ Oʀ Aɴᴏᴛʜᴇʀ Uꜱᴇʀ’ꜱ Bᴀʟᴀɴᴄᴇ\n"
       "• /rob (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Rᴏʙ Mᴏɴᴇʏ Fʀᴏᴍ A Uꜱᴇʀ\n"
       "• /kill (ʀᴇᴘʟʏ) — Kɪʟʟ A Uꜱᴇʀ & Eᴀʀɴ $200–$600\n"
       "• /revive — Rᴇᴠɪᴠᴇ Yᴏᴜʀꜱᴇʟꜰ Oʀ A Rᴇᴘʟɪᴇᴅ Uꜱᴇʀ\n"
       "• /protect 1ᴅ|2ᴅ|3ᴅ — Bᴜʏ Pʀᴏᴛᴇᴄᴛɪᴏɴ Fʀᴏᴍ Rᴏʙʙᴇʀʏ\n"
       "• /give (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Tʀᴀɴꜱꜰᴇʀ Mᴏɴᴇʏ\n"
       "• /shop — Sʜᴏᴘ Fᴏʀ Gɪꜰᴛ Iᴛᴇᴍꜱ\n"
       "• /items (ʀᴇᴘʟʏ) — Vɪᴇᴡ Yᴏᴜʀ / Oᴛʜᴇʀꜱ Iɴᴠᴇɴᴛᴏʀʏ\n"
       "• /toprich — Tᴏᴘ 10 Rɪᴄʜᴇꜱᴛ Uꜱᴇʀꜱ\n"
       "• /topkill — Tᴏᴘ 10 Kɪʟʟᴇʀꜱ\n"
       "• /check — Cʜᴇᴄᴋ Pʀᴏᴛᴇᴄᴛɪᴏɴ Sᴛᴀᴛᴜꜱ (Cᴏꜱᴛꜱ $2000)\n"

    )

    # ✅ Send as Markdown for bold formatting
    await update.message.reply_text(text, parse_mode="Markdown")

# =================== REVIVE COMMAND ===================
# =================== REVIVE COMMAND ===================

# =================== REVIVE COMMAND ===================
import time
from telegram import Update
from telegram.ext import ContextTypes

async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    reviver = update.effective_user
    #... yahaoe loaddata
    reviver_data = get_user(reviver.id, reviver.first_name)
    
    now = time.time()

    # ---------------- SELF REVIVE (NO REPLY)
    if not update.message.reply_to_message:
        # Agar khud dead hai
        if reviver_data.get("dead", False):
            if reviver_data.get("money", 0) < 500:
                await update.message.reply_text("😢 500₹ chahiye khudko revive karne ke liye!")
                return

            reviver_data["money"] -= 500
            reviver_data["dead"] = False
            reviver_data["dead_until"] = 0
            save_data()
            

            await update.message.reply_text(
                f"😎 {reviver.first_name} khud revive ho gaya!\n💰 500₹ cut gaya!"
            )
            return

        # Agar alive hoke khudko revive try kare
        if "self_revive_warn" not in reviver_data:
            reviver_data["self_revive_warn"] = 0

        reviver_data["self_revive_warn"] += 1

        if reviver_data["self_revive_warn"] == 1:
            await update.message.reply_text(
                "😂 Tu alive hai bhai! Revive mat kar!"
            )
        elif reviver_data["self_revive_warn"] == 2:
            await update.message.reply_text(
                "⚠️ Last warning! Tu alive hai 😡 Revive mat kar warna paisa katega!"
            )
        else:
            reviver_data["money"] -= 500

            # 🔥 RESET AFTER PENALTY
            reviver_data["self_revive_warn"] = 0

            await update.message.reply_text(
                "💸 Bola tha na! 500₹ cut gaya 😈"
            )

        save_data()
        
        return

    # ---------------- REPLY USER CASE
    target_user = update.message.reply_to_message.from_user
    target_data = get_user(target_user.id, target_user.first_name)
    
    # ---------------- Reviver dead (cannot revive others)
    if reviver_data.get("dead", False):
        await update.message.reply_text(
            "🤣 Tu khud dead hai! Pehle khud revive ho ja!"
        )
        return

    # ---------------- Target alive
    if not target_data.get("dead", False):
        if "revive_attempts" not in reviver_data:
            reviver_data["revive_attempts"] = {}

        attempts = reviver_data["revive_attempts"].get(str(target_user.id), 0)
        attempts += 1
        reviver_data["revive_attempts"][str(target_user.id)] = attempts

        if attempts == 1:
            await update.message.reply_text(
                f"😂 {target_user.first_name} already alive hai! Isko revive mat de!"
            )
        elif attempts == 2:
            await update.message.reply_text(
                f"⚠️ Last warning! Ye user alive hai 😡 Dobara try kiya toh paisa katega!"
            )
        else:
            reviver_data["money"] -= 500

            # 🔥 RESET AFTER PENALTY
            reviver_data["revive_attempts"][str(target_user.id)] = 0

            await update.message.reply_text(
                f"💸 Samjha nahi kya? 500₹ cut gaya 😈"
            )

        save_data()
        
        return

    # ---------------- Target dead (NORMAL REVIVE)
    if target_data.get("dead", False):
        if reviver_data.get("money", 0) < 500:
            await update.message.reply_text("😢 500₹ chahiye revive ke liye!")
            return

        reviver_data["money"] -= 500
        target_data["dead"] = False
        target_data["dead_until"] = 0

        save_data()
        

        await update.message.reply_text(
            f"{reviver.first_name} ne {target_user.first_name} ko revive kiya! 💖\n"
            f"Ab tu jinda hai 😎 Badla le jao!\nProtect lena mat bhulna!"
        )

        # DM target
        try:
            await context.bot.send_message(
                chat_id=target_user.id,
                text=f"{reviver.first_name} ne tujhe revive kiya 😎💖\nProtect lena mat bhulna!"
            )
        except:
            pass

        # DM reviver
        try:
            await context.bot.send_message(
                chat_id=reviver.id,
                text="✅ 500₹ deduct hua revive ke liye!"
            )
        except:
            pass
# =================== HELP / ECONOMY COMMAND ===================
from telegram import Update
from telegram.ext import ContextTypes

async def economy_help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    text = (
        "💰 *NIKI ECONOMY SYSTEM OVERVIEW*\n\n"
        "💬 *How it works:*\n"
        "Use Niki’s economy system to earn, manage, gift, and protect virtual money in your group.\n\n"
        "• /daily — Claim ₹1500 daily reward\n"
        "• /claim — Unlock group rewards based on members\n"
        "• /bal — Check your or another user’s balance\n"
        "• /rob (reply) <amount> — Rob money from a user\n"
        "• /kill (reply) — Kill a user & earn ₹200–₹600\n"
        "• /revive (reply) — Revive yourself or a replied dead user (costs ₹500)\n"
        "• /protect 1d|2d|3d — Buy protection from robbery\n"
        "• /give (reply) <amount> — Transfer money to another user\n"
        "• /shop — View available gift items in shop\n"
        "• /gift <amount> (reply) — Send gift to a user\n"
        "• /items (reply) — View your/others inventory\n"
        "• /toprich — Top 10 richest users\n"
        "• /topkill — Top 10 killers\n"
        "• /check  — Check protection status (costs ₹1000)\n\n"
        "⚠️ If you face any problems, contact my owner 👉 @YTT_BISHAL"
    )
    await update.message.reply_text(text, parse_mode="Markdown")





# =================== /ID COMMAND ===================
from telegram import Update
from telegram.ext import ContextTypes

OWNER_ID = 6175559434  # Owner numeric ID
OWNER_USERNAME = "YTT_BISHAL"  # Owner Telegram username

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    # Check if command is in reply
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    else:
        target_user = update.effective_user

    # Check if target is owner
    if target_user.id == OWNER_ID:
        await update.message.reply_text(
            f"🤔 Abey yar tu mera owner ka id dekhna chahega 🤔 nehi ye thik bat ni 😎\n"
            f"📝 Owner ka id secret hai, mt dekh 👉 @{OWNER_USERNAME}"
        )
        return

    # Group chat id
    chat_id = update.effective_chat.id
    # User numeric id
    user_id = target_user.id
    # Username if available
    username = target_user.username or target_user.first_name

    # Build message
    msg = (
        f"👤 User Name : {username}\n"
        f"🆔 User ID   : {user_id}\n"
        f"💬 Chat ID  : {chat_id}"
    )
    await update.message.reply_text(msg)




# ---------------- CHECK COMMAND FINAL ----------------
import time
from telegram import Update
from telegram.ext import ContextTypes

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    #loaddata

    checker = update.effective_user
    checker_data = get_user(checker.id, checker.first_name)

    cost = 2000

    # ---------------- IF NUMERIC ID USED IN GROUP ----------------
    if context.args:
        if checker_data.get("money", 0) < cost:
            await update.message.reply_text("😢 Paisa kam hai, 2000 chahiye check ke liye")
            return

        # Deduct money
        checker_data["money"] -= cost
        save_data()
        

        await update.message.reply_text(
            "😔 Sorry yahape group me chat id ya numeric id se check nahi kiya ja sakta.\n\n"
            "⚠️ Warning nahi tha but tumhara ₹2000 cut ho gaya 😅\n"
            "Agli baar aisi galti mat karna 👍"
        )
        return

    # ---------------- IF NOT REPLY ----------------
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Reply karke /check likho kisi ka protection check karne ke liye 😌"
        )
        return

    # ---------------- NORMAL REPLY CHECK ----------------
    target = update.message.reply_to_message.from_user
    target_data = get_user(target.id, target.first_name)

    if checker_data.get("money", 0) < cost:
        await update.message.reply_text("😢 Paisa kam hai, 2000 chahiye check ke liye")
        return

    # Deduct money
    checker_data["money"] -= cost
    save_data()
    

    # Calculate protection hours only
    now = time.time()
    protection_until = target_data.get("protection_until", 0)

    if protection_until > now:
        remaining_seconds = int(protection_until - now)
        hours = remaining_seconds // 3600
        protection_text = f"🛡 Active for {hours} hour(s)"
    else:
        protection_text = "❌ No active protection"

    # ----------- SEND DM TO CHECKER -----------
    try:
        await context.bot.send_message(
            chat_id=checker.id,
            text=(
                f"🛡 {target.first_name} ka Protection Status\n\n"
                f"{protection_text}\n\n"
                f"💸 ₹{cost} deduct ho gaya"
            )
        )
    except:
        await update.message.reply_text("⚠️ DM send nahi ho paya")

    # ----------- GROUP MESSAGE -----------
    await update.message.reply_text(
        f"🎉 {target.first_name} ka protection tum check kar liya 👍\n"
        f"DM me check karo 📨"
    )





pending_users = {}  # user_id : sticker_file_id


# ---------------- /own command ----------------
async def own(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    user = update.effective_user

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Sticker pe reply karke /own likho.")
        return

    replied = update.message.reply_to_message

    if not replied.sticker:
        await update.message.reply_text("❌ Sirf sticker pe reply karo.")
        return

    # Save sticker
    pending_users[user.id] = replied.sticker.file_id

    await update.message.reply_text(
        "✅ Sticker mil gaya!\nAb pack name likho aur is message pe reply karo."
    )


# ---------------- Pack Name Handler ----------------
async def pack_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in pending_users:
        return

    if not update.message.reply_to_message:
        return

    # Must reply to bot message
    if update.message.reply_to_message.from_user.id != context.bot.id:
        return

    pack_name = update.message.text.strip()

    await update.message.reply_text(
        f"🎉 {user.first_name}, tumhara pack '{pack_name}' create ho gaya! (Demo)"
    )

    del pending_users[user.id]


# ---------------- Main ----------------



# ---------------- ITEM COMMAND ----------------
async def items(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
   

    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    else:
        target = update.effective_user

    user_data = get_user(target.id, target.first_name)
    inventory = user_data.get("inventory", {})

    if not inventory:
        await update.message.reply_text(
            f"📦 {target.first_name} has no gifts yet!\n\n"
            f"Use /shop to see gifts and /gift to send one."
        )
        return

    text = f"🎁 {target.first_name}'s Gifts:\n\n"

    for gift_name, qty in inventory.items():
        emoji = shop_items[gift_name]["emoji"]
        text += f"{emoji} {gift_name.replace('_',' ').title()} x{qty}\n"

    await update.message.reply_text(text)



# ---------------- BROADCAST ON START ----------------



# ------------------ GIVE COMMAND ------------------


#-------------------AUTO REPLY----------------------
async def auto_niki_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if games.find_one({"_id": str(update.effective_chat.id)}):
        return
        
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower() if update.message.text else ""

    # agar koi "niki" bole
    if "niki" in text:
        await update.message.reply_text(
            "👋 Hello! Mujhe kisi ne yaad kiya?\n"
              "Main Niki  hoon 😎\n"
        )
        return

    # agar kisi ne bot ka message forward kiya
    if update.message.forward_from or update.message.forward_from_chat:
        await update.message.reply_text(
            "📩 Mere message ko forward karke kya bol rahe ho? 😏"
        )

# ------------------ GIVE COMMAND ------------------

# ------------------ GIVE COMMAND ------------------

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    message = update.message
    giver = message.from_user
    #.. loaddata

    # Reply check
    if not message.reply_to_message:
        await message.reply_text(
            "⚠️ Vishal Boss ka hukum ko hum thal nahi sakte, follow karo 👇👇👇\n\n"
            "Use this command by replying to a user and specifying amount.\n"
            "Example: Reply to someone with /give 500"
        )
        return

    receiver = message.reply_to_message.from_user

    if giver.id == receiver.id:
        await message.reply_text("🤡 Khud ko paisa nahi de sakte!")
        return

    # ✅ FIXED AMOUNT READ (IMPORTANT)
    if not context.args:
        await message.reply_text("❌ Amount likho. Example: /give 500")
        return

    try:
        amount = int(context.args[0])
    except:
        await message.reply_text("❌ Invalid amount! Use numbers only.")
        return

    if amount <= 0:
        await message.reply_text("💸 Amount must be greater than 0!")
        return

    giver_data = get_user(giver.id, giver.first_name)
    receiver_data = get_user(receiver.id, receiver.first_name)

    # tax
    tax = int(amount * 0.10)
    total = amount + tax

    if giver_data["money"] < total:
        await message.reply_text(
            f"💸 Paisa kam hai! Tumhe ₹{total} chahiye (10% tax included)."
        )
        return

    # transfer
    giver_data["money"] -= total
    receiver_data["money"] += amount

    save_data()
    

    msg = (
        f"💌 {giver.first_name} ne {receiver.first_name} ke liye paisa bheja ❤️\n\n"
        f"🎉 {receiver.first_name} ne khush ho gaya! 💰 {amount} mila\n\n"
        f"💸 Tax deduct hua: ₹{tax}, Tumhara naya balance: ₹{giver_data['money']}\n\n"
        f"😁 Tum dono ka balance ab update ho gaya!"
    )

    await message.reply_text(msg)

    # DM message
    try:
        await context.bot.send_message(receiver.id, msg)
    except:
        pass

#====================file_id==========≠===============
async def sticker_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.sticker:
        file_id = update.message.sticker.file_id
        await update.message.reply_text(f"Sticker File ID:\n{file_id}")


#---------------------GIFSFILE ID========--------=======



async def gif_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.animation:
        file_id = update.message.animation.file_id
        await update.message.reply_text(f"GIF File ID:\n{file_id}")

#==================COIN GAME=====================

# =================== COIN GAME ===================

# =================== COIN GAME ===================
import random
import asyncio

user_guess = {}

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("COIN RUNNING")  # debug

    message = update.message
    user = message.from_user
    

    # ================= RULES =================
    if not context.args:
        await message.reply_text(
            "🔥 COIN GAME\n\n"
            "➡️ /coin head\n"
            "➡️ /coin tail\n\n"
            "Phir reply karke likho ➜ /coin 100"
        )
        return

    arg = context.args[0].lower()

    # ================= GUESS =================
    if arg in ["head", "tail"]:

        user_guess[user.id] = arg

        await message.reply_text(
            f"🎯 Tumne {arg.upper()} choose kiya\n\n"
            "💰 Ab reply karke likho ➜ /coin 100"
        )
        return

    # ================= BET =================
    elif arg.isdigit():

        # MUST reply to bot
        if not message.reply_to_message or message.reply_to_message.from_user.id != context.bot.id:
            await message.reply_text("❌ Bot ke message ko reply karke bet lagao!")
            return

        if user.id not in user_guess:
            await message.reply_text("❌ Pehle /coin head ya tail likho.")
            return

        guess = user_guess[user.id]
        amount = int(arg)

        if amount < 100:
            await message.reply_text("❌ Minimum bet 100 hai.")
            return

        user_data = get_user(user.id, user.first_name)

        if user_data["money"] < amount:
            await message.reply_text("💸 Tumhare paas paisa nahi hai.")
            return

        # cut bet
        user_data["money"] -= 100
        save_data()
        

        await message.reply_text(f"🎮 {user.first_name} game start!\n🍀 Best of luck!")

        # animation
        flip = await message.reply_text("� Flipping...")
        await asyncio.sleep(1)
        await flip.edit_text("� Flipping... ⏳")
        await asyncio.sleep(1)
        await flip.edit_text("� Flipping... 🔄")
        await asyncio.sleep(1)

        # result
        result = random.choice(["head", "tail"])
        await flip.edit_text(f"� RESULT ➜ {result.upper()}")

        # win / loss
        if guess == result:
            win = random.randint(100, 1000)
            user_data["money"] += win
            save_data()
            

            await message.reply_text(f"🎉 WIN! ₹{win} mila 😎")
        else:
            await message.reply_text("💔 LOSS! ₹100 gaya 😢")

        await message.reply_text("🔁 Fir se try karo!")

        # clear guess
        del user_guess[user.id]

        return

    # ================= INVALID =================
    else:
        await message.reply_text("❌ Sirf head, tail ya amount likho.")

# ================= NUMBER GUESS GAME =================
import random

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    user = message.from_user
    

    if not context.args:
        await message.reply_text(
            "🎯 NUMBER GUESS GAME\n\n"
            "1 se 10 ke beech number guess karo\n\n"
            "➡️ Example: /guess 5"
        )
        return

    try:
        user_guess = int(context.args[0])
    except:
        await message.reply_text("❌ Sahi number likho (1-10)")
        return

    if user_guess < 1 or user_guess > 10:
        await message.reply_text("❌ Number 1 se 10 ke beech hona chahiye")
        return

    bot_number = random.randint(1, 10)

    user_data = get_user(user.id, user.first_name)

    # result
    if user_guess == bot_number:
        win = random.randint(100, 500)
        user_data["money"] += win
        save_data()
        

        await message.reply_text(
            f"🎉 Sahi pakda!\n\n"
            f"🤖 Bot number: {bot_number}\n"
            f"💰 Tum jeete ₹{win}"
        )
    else:
        loss = 50
        user_data["money"] -= loss
        save_data()
        

        await message.reply_text(
            f"💔 Galat guess\n\n"
            f"🤖 Bot number: {bot_number}\n"
            f"❌ ₹{loss} loss"
        )


# =================== DICE GAME ===================
import random
import asyncio

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    message = update.message
    user = message.from_user
    

    # ================= RULES =================
    if not context.args:
        await message.reply_text(
            "🎲 DICE GAME\n\n"
            "1 se 6 ke beech number choose karo\n\n"
            "➡️ Example: /dice 4\n\n"
            "🎯 Sahi guess = paisa jeetoge\n"
            "❌ Galat = ₹100 loss"
        )
        return

    # ================= INPUT =================
    try:
        user_guess = int(context.args[0])
    except:
        await message.reply_text("❌ Number likho (1-6)")
        return

    if user_guess < 1 or user_guess > 6:
        await message.reply_text("❌ Number 1 se 6 ke beech hona chahiye")
        return

    user_data = get_user(user.id, user.first_name)

    # ================= START =================
    await message.reply_text(f"🎮 {user.first_name} game start!\n🍀 Best of luck!")

    # ================= ANIMATION =================
    flip = await message.reply_text("🎲 Rolling...")
    await asyncio.sleep(1)
    await flip.edit_text("🎲 Rolling... ⏳")
    await asyncio.sleep(1)
    await flip.edit_text("🎲 Rolling... 🔄")
    await asyncio.sleep(1)

    # ================= RESULT =================
    bot_roll = random.randint(1, 6)

    await flip.edit_text(f"🎲 RESULT ➜ {bot_roll}")

    # ================= WIN / LOSS =================

    # ================= WIN / LOSS =================
    try:
        if user_guess == bot_roll:
            win = random.randint(200, 800)
            user_data["money"] += win

            await message.reply_text(
                f"🎉 WIN! ₹{win} mila 😎\n"
                f"💰 Balance: ₹{user_data['money']}"
            )

        else:
            loss = 100
            user_data["money"] -= loss

            if user_data["money"] < 0:
                user_data["money"] = 0

            await message.reply_text(
                f"💔 LOSS! ₹{loss} gaya 😢\n"
                f"💰 Balance: ₹{user_data['money']}"
            )

        save_data()
        

    except Exception as e:
        print("ERROR:", e)
        await message.reply_text("💝BETTER LUCK NEXT TIME PHIRSE TRY KARONE 😁❤️")

# =================== MINES GAME FINAL ===================
# =================== MINES GAME FINAL (WORKING) ===================
# =================== MINES GAME FINAL ===================


#====================AUTO FORWARD MSG ONLY OWNER======================

# =================== AUTO SAVE USERS & GROUPS ===================
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

# =================== START / TRACK CHAT ===================
async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global data  # ensure your global data variable is defined

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type

    # === GROUPS SAVE ===
    if chat_type in ["group", "supergroup"]:
        if "groups" not in data:
            data["groups"] = []
        if chat_id not in data["groups"]:
            data["groups"].append(chat_id)
            save_data()
            # auto save groups
            print(f"Group saved: {chat_id}")

    # === USERS SAVE ===
    if chat_type == "private":
        if "users" not in data:
            data["users"] = []
        if user_id not in data["users"]:
            data["users"].append(user_id)
            save_data() 
            # auto save users
            print(f"User saved: {user_id}")

# =================== FORWARD COMMAND /fw ===================
async def forward_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    OWNER_USERNAME = "@YTT_BISHAL"  # sirf ye user use kar sake

    # check if command from owner
    if update.effective_user.username != OWNER_USERNAME.replace("@", ""):
        return await update.message.reply_text("⚠️ Only owner can use this command!")

    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /fw Your message here")

    msg_text = " ".join(context.args)

    # combine users + groups
    recipients = data.get("users", []) + data.get("groups", [])
    sent_count = 0
    failed_count = 0

    for chat_id in recipients:
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg_text)
            sent_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to send to {chat_id}: {e}")

    await update.message.reply_text(f"✅ Sent: {sent_count}\n❌ Failed: {failed_count}")


#=====================ADD BALANCE=====================
async def addbal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke use karo")
        return

    try:
        target = update.message.reply_to_message.from_user
        amount = int(context.args[0])

        user = get_user(target.id, target.first_name)
        user["money"] += amount

        save_data()
        

        await update.message.reply_text(f"💰 {target.first_name} ko ₹{amount} add hua")

    except:
        await update.message.reply_text("❌ Use: /addbal 100000")

#====================SET BALANCE ======================
async def setbal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke use karo")
        return

    try:
        target = update.message.reply_to_message.from_user
        amount = int(context.args[0])

        user = get_user(target.id, target.first_name)
        user["money"] = amount

        save_data()
        

        await update.message.reply_text(f"👑 {target.first_name} ka balance set: ₹{amount}")

    except:
        await update.message.reply_text("❌ Use: /setbal 1000000")

#======================REMOVE BALANCE =================
async def removebal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke use karo")
        return

    try:
        target = update.message.reply_to_message.from_user
        amount = int(context.args[0])

        user = get_user(target.id, target.first_name)
        user["money"] -= amount

        if user["money"] < 0:
            user["money"] = 0

        save_data()
        

        await update.message.reply_text(f"💸 {target.first_name} se ₹{amount} remove hua")

    except:
        await update.message.reply_text("❌ Use: /removebal 100000")

#=====================SEND/STATS/BOARD CAST =======================
from pymongo import MongoClient
import asyncio

# ================= CONFIG =================
BOT_TOKEN = "8614646410:AAEDw9e9dJLxeElsixxCfolh2yrn8pBjxD4"
OWNER_ID = 6175559434
BOT_USERNAME = "iim_Nikibot"
MONGO_URL = "mongodb+srv://vishal:VISHAL123@vishal07.espy0qo.mongodb.net/?appName=Vishal07"

client = MongoClient(MONGO_URL)

db_broadcast = client["niki_bot"]
chats_col = db_broadcast["chats"]   # ⚡ 14 members yahi hai

# ================= SAVE USERS / GROUPS =================

# ================= STATS =================
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    total = col.count_documents({})
    users = col.count_documents({"type": "private"})
    groups = col.count_documents({"type": {"$in": ["group", "supergroup"]}})

    await update.message.reply_text(
        f"📊 Stats:\n👤 Users: {users}\n👥 Groups: {groups}\n📦 Total: {total}"
    )

# ================= BROADCAST =================
async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not update.message.reply_to_message and not context.args:
        await update.message.reply_text("❌ Reply or use /send text")
        return

    silent = False
    if context.args and context.args[0] == "-s":
        silent = True
        context.args.pop(0)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌸 Start Me", url=f"https://t.me/{BOT_USERNAME}")]
    ])

    total = 0
    failed = 0

    for user in col.find():
        try:
            if update.message.reply_to_message:
                msg = await update.message.reply_to_message.copy(
                    chat_id=user["chat_id"],
                    reply_markup=keyboard,
                    disable_notification=silent
                )
            else:
                text = " ".join(context.args)
                msg = await context.bot.send_message(
                    chat_id=user["chat_id"],
                    text=text,
                    reply_markup=keyboard,
                    disable_notification=silent
                )

            # 👉 Auto pin in groups
            if user["type"] in ["group", "supergroup"]:
                try:
                    await context.bot.pin_chat_message(
                        user["chat_id"],
                        msg.message_id
                    )
                except:
                    pass

            total += 1
            await asyncio.sleep(0.05)  # anti-ban delay

        except:
            failed += 1

    await update.message.reply_text(
        f"✅ Done!\n✔ Sent: {total}\n❌ Failed: {failed}"
    )
#=============================duelcommand======================

# ================================ START =================

from telegram import *
from telegram.ext import *
import asyncio
import random

BOT_TOKEN = "8614646410:AAEDw9e9dJLxeElsixxCfolh2yrn8pBjxD4"

duels = {}
duel_tasks = {}

# ================= DUEL =================



# ================= DUEL =================
async def duel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    user1 = update.effective_user

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "🎮 𝗗ᴜᴇʟ 𝗚ᴀᴍᴇ 𝗚ᴜɪᴅᴇ\n\n"
            "⚔️ Kᴀɪꜱᴇ ᴋʜᴇʟᴛᴇ ʜᴀɪ:\n\n"
            "1️⃣ /duel ᴋᴏɪ ᴜꜱᴇʀ ᴘᴇ ʀᴇᴘʟʏ ᴋᴀʀᴏ\n"
            "2️⃣ Oᴘᴘᴏɴᴇɴᴛ /accept ᴋᴀʀᴇ\n"
            "3️⃣ Dᴏɴᴏ ᴘʟᴀʏᴇʀ ʟᴜᴄᴋʏ ɴᴜᴍʙᴇʀ ᴄʜᴏᴏꜱᴇ\n"
            "4️⃣ Pʟᴀʏᴇʀ1 ʙᴇᴛ ꜱᴇᴛ ᴋᴀʀᴛᴀ ʜᴀɪ 💰\n"
            "5️⃣ Pʟᴀʏᴇʀ2 ᴜꜱɪ ʙᴇᴛ ᴀᴄᴄᴇᴘᴛ ᴋᴀʀᴛᴀ ʜᴀɪ\n\n"
            "🎲 Fɪɴᴀʟ:\n"
            "Jɪꜱᴋᴀ Dɪᴄᴇ ʙᴀᴅᴀ → Wɪɴɴᴇʀ 🏆\n\n"
            "💰 Wɪɴɴᴇʀ ꜱᴀʀᴀ ᴍᴏɴᴇʏ ʟᴇ ᴊᴀᴛᴀ ʜᴀɪ 😈\n\n"
            "🔥 Aʙ ʀᴇᴘʟʏ ᴋᴀʀᴏ ᴀᴜʀ /duel ᴅᴀʟᴏ!"
        )
        return

    user2 = update.message.reply_to_message.from_user

    duels[user1.id] = {
        "p1": user1.id,
        "p1_name": user1.first_name,
        "p2": user2.id,
        "p2_name": user2.first_name,
        "chat": update.effective_chat.id,
        "p1_done": False,
        "p2_done": False,
        "bet": None
    }

    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚔️ Accept Duel", callback_data=f"duel_acc_{user2.id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"duel_rej_{user2.id}")
        ]
    ])

    await update.message.reply_text(
        f"⚔️ {user1.first_name} ɴᴇ {user2.first_name} ᴋᴏ ᴄʜᴀʟʟᴇɴɢᴇ ᴋɪʏᴀ!",
        reply_markup=kb
    )

    async def timeout():
        await asyncio.sleep(15)

        if user1.id in duels:
            await context.bot.send_message(
                update.effective_chat.id,
                f"⏳ {user2.first_name} accept karo duel!"
            )

        await asyncio.sleep(15)

        if user1.id in duels:
            del duels[user1.id]
            await context.bot.send_message(
                update.effective_chat.id,
                "❌ Duel cancel ho gaya (no response)"
            )

    duel_tasks[user1.id] = asyncio.create_task(timeout())


# ================= ACCEPT =================
async def accept_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id

    for key, d in duels.items():
        if d["p2"] == uid:

            if key in duel_tasks:
                duel_tasks[key].cancel()

            await query.edit_message_text(
                f"🔥 Dᴜᴇʟ Aᴄᴄᴇᴘᴛᴇᴅ!\n⏳ {d['p1_name']} ᴍᴏᴠᴇ..."
            )

            await send_number_choice(context, d["p1"])
            return

    await query.answer("Tum is duel ke player nahi ho!", show_alert=True)


# ================= CANCEL =================
async def cancel_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id

    for key, d in duels.items():
        if d["p2"] == uid:

            if key in duel_tasks:
                duel_tasks[key].cancel()

            del duels[key]

            await query.edit_message_text("❌ Duel cancel ho gaya")
            return

    await query.answer("Tum cancel nahi kar sakte!", show_alert=True)


# ================= NUMBER =================
async def send_number_choice(context, uid):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(str(i), callback_data=f"num_{uid}_{i}") for i in range(1, 4)],
        [InlineKeyboardButton(str(i), callback_data=f"num_{uid}_{i}") for i in range(4, 7)]
    ])

    await context.bot.send_message(
        uid,
        "🎲 𝗖ʜᴏᴏꜱᴇ ʏᴏᴜʀ ʟᴜᴄᴋʏ ɴᴜᴍʙᴇʀ 😈",
        reply_markup=kb
    )


# ================= BET =================
async def send_bet_choice(context, uid):
    bets = [500, 700, 1000, 2000, 5000, 10000]

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"💰 {b}", callback_data=f"bet_{uid}_{b}")]
        for b in bets
    ])

    await context.bot.send_message(
        uid,
        "💸 𝗖ʜᴏᴏꜱᴇ ʏᴏᴜʀ ʙᴇᴛ 💰",
        reply_markup=kb
    )


# ================= BUTTON =================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    uid_clicked = query.from_user.id

    for key, d in duels.items():

        # 👉 sirf duel ke players hi interact kare
        if uid_clicked not in [d["p1"], d["p2"]]:
            continue

        # ================= NUMBER =================
        if data[0] == "num":

            uid = int(data[1])
            num = int(data[2])

            if d["p1"] == uid and not d["p1_done"]:
                d["p1_num"] = num
                d["p1_done"] = True

                await query.edit_message_text(
                    f"✅ {d['p1_name']} Nᴜᴍʙᴇʀ Lᴏᴄᴋᴇᴅ 🔒"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"🎯 {d['p1_name']} ne number choose kiya!"
                )

                await send_number_choice(context, d["p2"])
                return

            if d["p2"] == uid and not d["p2_done"]:
                d["p2_num"] = num
                d["p2_done"] = True

                await query.edit_message_text(
                    f"✅ {d['p2_name']} Nᴜᴍʙᴇʀ Lᴏᴄᴋᴇᴅ 🔒"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"🎯 {d['p2_name']} ready!"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"🔥 {d['p1_name']} vs {d['p2_name']} ready!"
                )

                await send_bet_choice(context, d["p1"])
                return

        # ================= BET =================
        if data[0] == "bet":

            uid = int(data[1])
            bet = int(data[2])

            # 👉 wrong user click ignore
            if uid_clicked != uid:
                continue

            # ================= P1 BET =================
            if d["p1"] == uid_clicked:

                u1 = data_store[str(d["p1"])]

                if u1["money"] < bet:
                    await query.answer("❌ Paise kam hai", show_alert=True)
                    return

                d["bet"] = bet

                # 💸 P1 paisa cut
                u1["money"] -= bet
                save_data()
                

                await query.edit_message_text(
                    f"💰 {d['p1_name']} ne bet lock kiya: {bet}"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"💰 {d['p1_name']} ne {bet} bet lagaya!\n⏳ {d['p2_name']} /accept karega..."
                )

                # 📩 P2 DM
                await context.bot.send_message(
                    d["p2"],
                    f"💰 {d['p1_name']} ne {bet} bet lagaya hai!\n\n👉 Accept karne ke liye /accept likho 😈"
                )

                # ⏳ TIMER SYSTEM
                async def bet_timeout():
                    await asyncio.sleep(20)

                    if key in duels:
                        await context.bot.send_message(
                            d["chat"],
                            f"⏳ {d['p2_name']} jaldi karo! /accept karo (20 sec left)"
                        )

                    await asyncio.sleep(20)

                    if key in duels:
                        # 💸 refund P1
                        u1["money"] += bet
                        save_data()
                        

                        await context.bot.send_message(
                            d["chat"],
                            "❌ Duel cancel ho gaya (no accept)\n💰 P1 ka paisa wapas"
                        )

                        duels.pop(key, None)

                asyncio.create_task(bet_timeout())

                return

#===================ACCEPT BET===================
async def accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    for key, d in duels.items():

        if user_id != d["p2"]:
            continue

        if not d.get("bet"):
            await update.message.reply_text("❌ Bet abhi set nahi hua")
            return

        u1 = data_store[str(d["p1"])]
        u2 = data_store[str(d["p2"])]

        # 💰 money check
        if u2["money"] < d["bet"]:
            await update.message.reply_text("❌ Tumhare paas paise kam hai")
            return

        # 💸 P2 paisa cut
        u2["money"] -= d["bet"]

        save_data()
        

        # 📩 DM to both
        await context.bot.send_message(
            d["p1"],
            "🔥 Bet accepted!\n👉 Group me game start ho gaya"
        )

        await context.bot.send_message(
            d["p2"],
            "🔥 Tumne bet accept kiya!\n👉 Group check karo"
        )

        # 📢 Group msg
        await context.bot.send_message(
            d["chat"],
            f"🔥 Duel Start!\n💰 Bet: {d['bet']}\n🎮 Game begins now!"
        )

        await start_duel(context, d)

        duels.pop(key, None)
        return

    await update.message.reply_text("❌ Koi active bet nahi mila")
# ================= DUEL ENGINE =================
async def start_duel(context, d):
    chat = d["chat"]

    await context.bot.send_message(chat, f"🎲 {d['p1_name']} ka dice")
    msg1 = await context.bot.send_dice(chat)

    await asyncio.sleep(3)

    await context.bot.send_message(chat, f"🎲 {d['p2_name']} ka dice")
    msg2 = await context.bot.send_dice(chat)

    r1 = msg1.dice.value
    r2 = msg2.dice.value

    total = d["bet"] * 2

    u1 = data_store[str(d["p1"])]
    u2 = data_store[str(d["p2"])]

    if r1 > r2:
        u1["money"] += total
        winner = d["p1_name"]

    elif r2 > r1:
        u2["money"] += total
        winner = d["p2_name"]

    else:
        u1["money"] += d["bet"]
        u2["money"] += d["bet"]
        winner = "Draw"

    save_data()
    

    await context.bot.send_message(
        chat,
        f"🎲 𝗥ᴇꜱᴜʟᴛ\n\n"
        f"👤 {d['p1_name']}: {r1}\n"
        f"👤 {d['p2_name']}: {r2}\n\n"
        f"🏆 Wɪɴɴᴇʀ: 👑 {winner}\n"
        f"💰 Tᴏᴛᴀʟ: {total}"
    )    
    
#=========================ROMANTIC===============================



# ================= DB =================
# ================= DB =================
MONGO_URL = "mongodb+srv://vishal:VISHAL123@vishal07.espy0qo.mongodb.net/?appName=Vishal07"

client = MongoClient(MONGO_URL)


db = client["botdb"]

marriage_col = db["marriages"]
gif_col = db["gifs"]   # 💋 kiss + hug yahi se aayega
# ================= LOAD GIF =================
def get_gifs(command):
    data = gif_col.find_one({"cmd": command})   # ✅ FIX
    if data:
        return data.get("gifs", [])
    return []

# ================= SAVE GIF =================
def save_gif(cmd, gif):
    gif_col.update_one(   # ✅ FIX
        {"cmd": cmd},
        {"$addToSet": {"gifs": gif}},
        upsert=True
)

# ================= /savegif COMMAND =================
async def savegif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ GIF pe reply karke use karo")
        return

    if len(context.args) == 0:
        await update.message.reply_text("❌ Use: /savegif kiss")
        return

    cmd = context.args[0].lower()
    msg = update.message.reply_to_message

    gif = None

    # GIF / Animation detect
    if msg.animation:
        gif = msg.animation.file_id
    elif msg.document and msg.document.mime_type == "video/mp4":
        gif = msg.document.file_id

    if not gif:
        await update.message.reply_text("❌ Ye GIF nahi hai")
        return

    save_gif(cmd, gif)
    await update.message.reply_text(f"✅ GIF saved in /{cmd}")

# ================= COMMON FUNCTION =================
async def send_action(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd, text_template):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke use karo")
        return

    user1 = update.message.from_user.first_name
    user2 = update.message.reply_to_message.from_user.first_name

    gifs = get_gifs(cmd)
    if not gifs:
        await update.message.reply_text("❌ GIF nahi mila")
        return

    gif = random.choice(gifs) if gifs else None

    if not gif:
        await update.message.reply_text("❌ GIF nahi mila")
        return

    msg = text_template.format(u1=user1, u2=user2)

    await update.message.reply_animation(animation=gif, caption=msg)

# ================= COMMANDS =================

async def kiss(update, context):
    await send_action(update, context, "kiss",
    "😘 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐊𝐢𝐬𝐬 𝐝𝐢𝐲𝐚 💋")

async def hug(update, context):
    await send_action(update, context, "hug",
    "🤗 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐇𝐮𝐠 𝐤𝐢𝐲𝐚 ❤️")

async def slap(update, context):
    await send_action(update, context, "slap",
    "😂 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐒𝐥𝐚𝐩 𝐦𝐚𝐫𝐚 👋")

async def kick(update, context):
    await send_action(update, context, "kick",
    "😆 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐊𝐢𝐜𝐤 𝐦𝐚𝐫𝐚 🦵")

async def pat(update, context):
    await send_action(update, context, "pat",
    "🥰 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐏𝐚𝐭 𝐤𝐢𝐲𝐚 🫳")

async def punch(update, context):
    await send_action(update, context, "punch",
    "👊 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐏𝐮𝐧𝐜𝐡 𝐦𝐚𝐫𝐚 💥")

async def bite(update, context):
    await send_action(update, context, "bite",
    "😋 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐁𝐢𝐭𝐞 𝐤𝐢𝐲𝐚 🦷")

async def cuddle(update, context):
    await send_action(update, context, "cuddle",
    "💞 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐂𝐮𝐝𝐝𝐥𝐞 𝐤𝐢𝐲𝐚 🤍")

async def poke(update, context):
    await send_action(update, context, "poke",
    "👉 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐏𝐨𝐤𝐞 𝐤𝐢𝐲𝐚 😜")

async def tickle(update, context):
    await send_action(update, context, "tickle",
    "🤣 {u1} 𝐍𝐞 {u2} 𝐊𝐨 𝐓𝐢𝐜𝐤𝐥𝐞 𝐤𝐢𝐲𝐚 😂")



# ================= SPECIAL USERS =================
SPECIAL_USERS = [
    "YTT_BISHAL",
    "ll_Sassy_Queen_ll",
    "ll_Vishal_Heart_ll"   # <-- yaha apna 3rd username dal dena (without @)
]

# ================= LOVE COMMAND =================
async def love(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke /love use karo!")
        return

    user1 = update.effective_user
    user2 = update.message.reply_to_message.from_user

    # Username (without @)
    username1 = user1.username if user1.username else str(user1.id)
    username2 = user2.username if user2.username else str(user2.id)

    # Check if both are in special list
    if username1 in SPECIAL_USERS and username2 in SPECIAL_USERS:
        love_percent = 100
    else:
        love_percent = random.randint(1, 100)

    # Clickable name (tg://user?id=)
    name1 = f"<a href='tg://user?id={user1.id}'>{user1.first_name}</a>"
    name2 = f"<a href='tg://user?id={user2.id}'>{user2.first_name}</a>"

    # Stylish format (tumhara wala)
    text = f"""
❤️ Lᴏᴠᴇ Mᴇᴛᴇʀ Rᴇᴘᴏʀᴛ ❤️

{name1} ❤️ {name2}

Lᴏᴠᴇ Cᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ: {love_percent}% ❤️
"""

    await update.message.reply_text(text, parse_mode="HTML")

# ================= MONGO =================
MONGO_URL = "mongodb+srv://vishal:VISHAL123@vishal07.espy0qo.mongodb.net/?appName=Vishal07"
client = MongoClient(MONGO_URL)

db = client["couple_db"]
couple_col = db["groups"]





# ================= SPECIAL USERS (USERNAME YA ID) =================
SPECIAL_USERS = [
    "YTT_BISHAL",   # username without @
    "ll_Sassy_Queen_ll",
    "ll_Vishal_Heart_ll",
    "user4",
    "user5"
]

# ================= COOLDOWN =================
COOLDOWN = 300  # 5 min


# ================= SHAYARI =================
SHAYARI_LIST = [
    "Teri muskaan me kuch baat hai 💖",
    "Nazron se shuru hui kahani 💞",
    "Tum dono ek dusre ke liye bane ho 💕",
    "Mohabbat ki hawa chal rahi hai 💘",
    "Tere bina adhura tha sab 💓",
    "Do dil jab milte hain 💖",
    "Kuch toh jaadu hai tum dono ke beech ✨",
    "Dil se dil ka connection 💞",
    "Jodi ho toh tum dono jaisi 💕",
    "Rab ne banayi hogi tumhari jodi 💘"
]


# ================= DATA FUNCTIONS =================
def get_data(chat_id):
    chat_id = str(chat_id)

    data = couple_col.find_one({"_id": chat_id})
    if not data:
        data = {
            "_id": chat_id,
            "count": 0,
            "last_used": 0,
            "photo": None,
            "shayari_index": 0,
            "history": [],
            "leaderboard": {}
        }
        couple_col.insert_one(data)

    return data


def update_data(chat_id, data):
    chat_id = str(chat_id)

    data.pop("_id", None)  # ❗ VERY IMPORTANT
    couple_col.update_one({"_id": chat_id}, {"$set": data})

# ================= SET PHOTO =================
async def setcouplepic(update, context):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("❌ Photo pe reply karo!")
        return

    chat_id = update.effective_chat.id
    photo_id = update.message.reply_to_message.photo[-1].file_id

    data = get_data(chat_id)

    # ✅ already saved check
    if data.get("photo"):
        await update.message.reply_text("⚠️ Couple photo already saved hai!")
        return

    data["photo"] = photo_id

    update_data(chat_id, data)

    await update.message.reply_text("✅ Couple photo permanently saved 💖")

# ================= COUPLE =================
async def couple(update, context):
    if not update.message:
        return

    chat = update.effective_chat
    if chat.type == "private":
        await update.message.reply_text("❌ Yeh command sirf group me kaam karega")
        return

    chat_id = chat.id
    user = update.effective_user
    username = user.username or ""

    data = get_data(chat_id)

    # ===== COOLDOWN =====
    if username not in SPECIAL_USERS:
        if time.time() - data.get("last_used", 0) < COOLDOWN:
            await update.message.reply_text("⏳ Try after 5 mins")
            return

    data["last_used"] = time.time()

    # ===== GET MEMBERS =====
    special_members = []
    normal_members = []

    try:
        admins = await context.bot.get_chat_administrators(chat_id)

        for admin in admins:
            u = admin.user
            if u.is_bot:
                continue

            uname = u.username or ""

            if uname in SPECIAL_USERS:
                special_members.append(u)
            else:
                normal_members.append(u)

    except:
        pass

    # 👉 current user add
    if not user.is_bot:
        if username in SPECIAL_USERS:
            special_members.append(user)
        else:
            normal_members.append(user)

    # 👉 remove duplicates
    special_members = list({m.id: m for m in special_members}.values())
    normal_members = list({m.id: m for m in normal_members}.values())

    # ===== LOGIC =====

    # 🔥 SPECIAL USER COMMAND
    if username in SPECIAL_USERS:

        if len(special_members) >= 2:
            user1, user2 = random.sample(special_members, 2)

        else:
            if len(normal_members) < 2:
                await update.message.reply_text("❌ Not enough users")
                return

            user1, user2 = random.sample(normal_members, 2)

    # 🔥 NORMAL USER COMMAND
    else:
        data["count"] = data.get("count", 0) + 1

        # 👉 4th turn special
        if data["count"] == 4:

            if len(special_members) >= 2:
                user1, user2 = random.sample(special_members, 2)
            else:
                if len(normal_members) < 2:
                    await update.message.reply_text("❌ Not enough users")
                    return

                user1, user2 = random.sample(normal_members, 2)

            data["count"] = 0

        else:
            if len(normal_members) < 2:
                await update.message.reply_text("❌ Not enough users")
                return

            user1, user2 = random.sample(normal_members, 2)

    # ===== SHAYARI =====
    shayari_index = data.get("shayari_index", 0)
    shayari = SHAYARI_LIST[shayari_index]
    data["shayari_index"] = (shayari_index + 1) % len(SHAYARI_LIST)

    # ===== SAVE HISTORY =====
    data.setdefault("history", [])
    data.setdefault("leaderboard", {})

    data["history"].append((user1.id, user2.id, user1.first_name, user2.first_name))
    data["history"] = data["history"][-10:]

    key = f"{min(user1.id,user2.id)}_{max(user1.id,user2.id)}"
    data["leaderboard"][key] = data["leaderboard"].get(key, 0) + 1

    update_data(chat_id, data)

    # ===== TEXT =====
    name1 = f"<a href='tg://user?id={user1.id}'>{user1.first_name}</a>"
    name2 = f"<a href='tg://user?id={user2.id}'>{user2.first_name}</a>"

    caption = f"""
💞 Tᴏᴅᴀʏ's Sᴘᴇᴄɪᴀʟ Cᴏᴜᴘʟᴇ 💞

{name1} ❤️ {name2}

✨ "{shayari}"

💖 Niki says: Tum dono ki jodi hamesha bani rahe 💕
"""

    # ===== SEND =====
    if data.get("photo"):
        msg = await context.bot.send_photo(
            chat_id=chat_id,
            photo=data["photo"],
            caption=caption,
            parse_mode="HTML"
        )
    else:
        msg = await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode="HTML"
        )

    # ===== AUTO PIN =====
    try:
        await context.bot.pin_chat_message(chat_id, msg.message_id)
    except:
        pass

# ================= HISTORY =================
async def couplehistory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_data(update.effective_chat.id)

    if not data["history"]:
        await update.message.reply_text("No history")
        return

    text = "💖 Couple History\n\n"
    for u1,u2,n1,n2 in reversed(data["history"]):
        text += f"<a href='tg://user?id={u1}'>{n1}</a> ❤️ <a href='tg://user?id={u2}'>{n2}</a>\n"

    await update.message.reply_text(text, parse_mode="HTML")

# ================= LEADERBOARD =================
async def coupleleaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_data(update.effective_chat.id)

    if not data["leaderboard"]:
        await update.message.reply_text("No data")
        return

    sorted_pairs = sorted(data["leaderboard"].items(), key=lambda x:x[1], reverse=True)[:10]

    text = "🏆 Top Couples\n\n"
    for i,(pair,count) in enumerate(sorted_pairs,1):
        u1,u2 = pair.split("_")
        text += f"{i}. <a href='tg://user?id={u1}'>User</a> ❤️ <a href='tg://user?id={u2}'>User</a> ➤ {count}\n"

    await update.message.reply_text(text, parse_mode="HTML")


#=================≠==========propes======================
SPECIAL_USER = "YTT_BISHAL"
MAX_SPECIAL_MARRIAGE = 3
#==========================❤️❤️❤️=========================
MONGO_URL = "mongodb+srv://vishal:VISHAL123@vishal07.espy0qo.mongodb.net/?appName=Vishal07"

client = MongoClient(MONGO_URL)
db = client["botdb"]

client = MongoClient(MONGO_URL)
db = client["botdb"]

marriage_col = db["marriages"]
gif_col = db["gifs"]   # 💋 kiss + hug yahi se aayega
# ================= GLOBAL =================
pending_proposals = {}

# ================= HELP =================
def link_user(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

def get_marriages(uid):
    return list(marriage_col.find({"$or":[{"user1":uid},{"user2":uid}]}))

def is_married(uid):
    return len(get_marriages(uid)) > 0

def get_gifs(cmd):
    data = gif_col.find_one({"cmd": cmd})
    return data.get("gifs", []) if data else []

def get_random_gif(cmd):
    gifs = get_gifs(cmd)
    return random.choice(gifs) if gifs else None

# ================= ADD GIF =================
async def addgifs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.animation:
        await update.message.reply_text("❌ GIF pe reply karo")
        return

    gif_col.insert_one({"gif": update.message.reply_to_message.animation.file_id})
    await update.message.reply_text("💖 Romantic GIF saved successfully")

# ================= PROPOSE =================
async def propose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user1 = update.effective_user

    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke propose karo 💌")
        return

    user2 = update.message.reply_to_message.from_user

    if user1.id == user2.id:
        await update.message.reply_text("💀 Khud se shaadi? 😂")
        return

    key = f"{user1.id}_{user2.id}"

    if key in pending_proposals:
        await update.message.reply_text("⏳ Proposal already pending hai")
        return
# ================= SPECIAL USER CHECK =================
    m1 = get_marriages(user1.id)

    if user1.username != SPECIAL_USER:
        if m1:
            text = (
                "💞━━━━━━━💞\n"
                "💍 Already Taken 💍\n"
                "💞━━━━━━━💞\n\n"
                "❤️ Tum already committed ho:\n\n"
            )
            for x in m1:
                u1 = await context.bot.get_chat(x['user1'])
                u2 = await context.bot.get_chat(x['user2'])
                text += f"💖 {link_user(u1)} Weds {link_user(u2)}\n"

            await update.message.reply_text(text, parse_mode="HTML")
            return
    else:
        if len(m1) >= MAX_SPECIAL_MARRIAGE:
            await update.message.reply_text("💀 Tum already 3 marriages kar chuke ho!")
            return
        
    if is_married(user2.id):
        m = get_marriages(user2.id)
        text = (
            "💞━━━━━━━💞\n"
            "💍 Already Committed 💍\n"
            "💞━━━━━━━💞\n\n"
        )
        for x in m:
            u1 = await context.bot.get_chat(x['user1'])
            u2 = await context.bot.get_chat(x['user2'])
            text += f"💖 {link_user(u1)} Weds {link_user(u2)}\n"

        await update.message.reply_text(text, parse_mode="HTML")
        return

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💚 Accept", callback_data=f"marry_acc_{user1.id}_{user2.id}"),
            InlineKeyboardButton("💔 Reject", callback_data=f"marry_rej_{user1.id}_{user2.id}")
        ]
    ])

    msg = await update.message.reply_text(
        f"💌 {link_user(user1)} ne {link_user(user2)} ko propose kiya hai!\n\n💖 Kya tum accept karte ho?",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    pending_proposals[key] = msg.message_id

    await asyncio.sleep(30)

    if key in pending_proposals:
        del pending_proposals[key]
        try:
            await msg.edit_text("💔 Time over... Proposal reject ho gaya")
        except:
            pass

# ================= ACCEPT =================
async def accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, _, u1, u2 = q.data.split("_")
    u1, u2 = int(u1), int(u2)

    key = f"{u1}_{u2}"

    if key not in pending_proposals:
        await q.answer("❌ Proposal expire ho gaya!", show_alert=True)
        return

    if q.from_user.id != u2:
        await q.answer("❌ Ye tumhara proposal nahi hai!", show_alert=True)
        return

    del pending_proposals[key]

    marriage_col.insert_one({"user1":u1,"user2":u2})

    text = (
        "💞━━━━━━━💞\n"
        "💍 M A R R I A G E 💍\n"
        "💞━━━━━━━💞\n\n"
        f"💖 <a href='tg://user?id={u1}'>User</a> Weds <a href='tg://user?id={u2}'>User</a> 💖\n\n"
        "💫 Dil mil gaye...\n"
        "💫 Rishta ban gaya...\n"
        "🥳 Mubarak hooooo 🎉"
    )

    gif = get_random_gif()

    # ================= DP ADD =================
    p1 = await context.bot.get_user_profile_photos(u1)
    p2 = await context.bot.get_user_profile_photos(u2)

    photo = None

    if p1.total_count > 0:
        photo = p1.photos[0][-1].file_id
    elif p2.total_count > 0:
        photo = p2.photos[0][-1].file_id

    if gif:
        await q.message.reply_animation(gif, caption=text, parse_mode="HTML")
        await q.message.delete()
    elif photo:
        await q.message.reply_photo(photo, caption=text, parse_mode="HTML")
        await q.message.delete()
    else:
        await q.edit_message_text(text, parse_mode="HTML")

# ================= REJECT =================
async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    _, _, u1, u2 = q.data.split("_")
    key = f"{u1}_{u2}"

    if key not in pending_proposals:
        await q.answer("❌ Already expired", show_alert=True)
        return

    if q.from_user.id != int(u2):
        await q.answer("❌ Ye tumhara proposal nahi hai!", show_alert=True)
        return

    del pending_proposals[key]

    await q.edit_message_text("💔 Proposal reject ho gaya...")

# ================= PARTNER =================
async def partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    m = get_marriages(uid)

    if not m:
        await update.message.reply_text("❌ Tum single ho 😅")
        return

    text = "💑 Tumhara relation:\n\n"

    for x in m:
        u1 = await context.bot.get_chat(x['user1'])
        u2 = await context.bot.get_chat(x['user2'])
        text += f"💖 {link_user(u1)} Weds {link_user(u2)}\n"

    await update.message.reply_text(text, parse_mode="HTML")

# ================= PROFILE =================
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id

    m = get_marriages(uid)

    text = (
        "👤━━━━━━━👤\n"
        "💖 USER PROFILE 💖\n"
        "👤━━━━━━━👤\n\n"
        f"👑 Name: {link_user(user)}\n"
        f"🆔 ID: <code>{uid}</code>\n\n"
    )

    if not m:
        text += "💔 Status: Single 😅"
    else:
        text += "💍 Status: Married\n\n💑 Partner:\n"
        for x in m:
            u1 = await context.bot.get_chat(x['user1'])
            u2 = await context.bot.get_chat(x['user2'])
            text += f"💖 {link_user(u1)} Weds {link_user(u2)}\n"

    await update.message.reply_text(text, parse_mode="HTML")

# ================= HISTORY =================
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = list(marriage_col.find())

    if not data:
        await update.message.reply_text("📜 No marriages yet")
        return

    text = "📜 Marriage History:\n\n"

    for x in data:
        u1 = await context.bot.get_chat(x['user1'])
        u2 = await context.bot.get_chat(x['user2'])
        text += f"💖 {link_user(u1)} Weds {link_user(u2)}\n"

    await update.message.reply_text(text, parse_mode="HTML")

# ================= DIVORCE =================
async def divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    m = get_marriages(uid)

    if not m:
        await update.message.reply_text("❌ Tum married hi nahi ho")
        return

    marriage_col.delete_many({"$or":[{"user1":uid},{"user2":uid}]})
    await update.message.reply_text("💔 Divorce ho gaya...\nAb tum free ho 😌")
    
#====================LOOKRATE=======================


# 👉 YAHAPE APNE 5 VIP USERNAME DAL (without @)
SPECIAL_USERS = [
    "YTT_BISHAL",
    "iim_Nikibot",
    "ll_Vishal_Heart_ll",
    "ll_Sassy_Queen_ll",
    "ll_Evil_ll"
]

# ================= LOOK COMMAND =================
async def look(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke /look use karo")
        return

    user = update.message.reply_to_message.from_user
    name = user.first_name
    user_id = user.id
    username = user.username.lower() if user.username else ""

    # 👉 FIXED VIP CHECK (case-insensitive)
    if username in [u.lower() for u in SPECIAL_USERS]:
        rating = "∞"
        emoji = "😍🔥👑"
        status = "✨ 𝙑𝙄𝙋 𝙎𝙔𝙎𝙏𝙀𝙈 𝘼𝘾𝙏𝙄𝙑𝙀"
    else:
        percent = random.randint(1, 100)
        rating = f"{percent}%"

        if percent >= 90:
            emoji = "😍🔥"
        elif percent >= 70:
            emoji = "😎✨"
        elif percent >= 50:
            emoji = "🙂"
        else:
            emoji = "😐💔"

        status = "✨ 𝙉𝙊𝙍𝙈𝘼𝙇 𝙐𝙎𝙀𝙍"

    # 👉 FANCY TEXT OUTPUT (same as yours)
    text = f"""
ꙮ๊ 『🇻⃪͢𝗜𝗣』𝙇𝙊𝙊𝙆 𝙍𝘼𝙏𝙄𝙉𝙂 𝙎𝙔𝙎𝙏𝙀𝙈 🦅✨

👤 <a href="tg://user?id={user_id}">{name}</a>
💖 𝙇𝙊𝙊𝙆 𝙍𝘼𝙏𝙄𝙉𝙂 𝙄𝙎: {rating} {emoji}

{status}
"""

    await update.message.reply_text(text, parse_mode="HTML")


    #=============BRAIN==================
    
# ================= SPECIAL USERS =================
SPECIAL_USERS = [
    6175559434,
    8798985968,
    8336495718,
    8798985968,
    8667537253,
    444444444
]

# ================= EMOJI SYSTEM =================
def get_iq_emoji(iq):
    if iq <= 20:
        return "🤡"
    elif iq <= 40:
        return "😵"
    elif iq <= 60:
        return "😎"
    elif iq <= 80:
        return "🔥"
    elif iq <= 99:
        return "🧠"
    else:
        return "🚀"

# ================= CLICKABLE NAME =================
def mention(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

# ================= PROGRESS BAR =================
def progress_bar(percent):
    total = 10
    filled = int(percent / 10)
    empty = total - filled
    return "█" * filled + "░" * empty

# ================= BRAIN COMMAND =================
async def brain(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ❌ MUST REPLY
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply karke use karo /brain")
        return

    target = update.message.reply_to_message.from_user
    name = mention(target)
    user_id = target.id

    msg = await update.message.reply_text("🧠 Initializing Brain Scan...")
    
    # ================= SPECIAL USER =================
    if user_id in SPECIAL_USERS:

        # 🔥 FULL ANIMATION (0 → 100)
        for i in range(0, 101, 10):
            bar = progress_bar(i)
            try:
                await msg.edit_text(f"⚡ OVERRIDE SCAN...\n\n[{bar}] {i}%")
                await asyncio.sleep(0.2)
            except:
                pass

        # 🔥 FINAL RESULT (INFINITY)
        text = f"""
<pre>
╔═══━━━─── • ───━━━═══╗
     ⚡ SYSTEM OVERRIDE ⚡
╚═══━━━─── • ───━━━═══╝

🎯 TARGET : {name}

🧬 IQ LEVEL : ∞ ♾️
🧠 STATUS : GOD MODE ☠️
💻 ACCESS : VIP ROOT

[██████████] ∞%

╔═━━━─── • ───━━━═╗
   ☠️ NO LIMIT SYSTEM ☠️
╚═━━━─── • ───━━━═╝
</pre>
"""
        await msg.edit_text(text, parse_mode="HTML")
        return

    # ================= NORMAL USER =================
    iq = random.randint(1, 100)
    emoji = get_iq_emoji(iq)

    # 🔥 ANIMATION (0 → IQ)
    for i in range(0, iq + 1, 10):
        bar = progress_bar(i)
        try:
            await msg.edit_text(f"🧠 Scanning Brain...\n\n[{bar}] {i}%")
            await asyncio.sleep(0.2)
        except:
            pass

    # 🔥 FINAL BAR EXACT IQ
    final_bar = progress_bar(iq)

    text = f"""
<pre>
╔═══━━━─── • ───━━━═══╗
        🧠 BRAIN SCAN
╚═══━━━─── • ───━━━═══╝

🎯 TARGET : {name}

🧬 IQ LEVEL : {iq}% {emoji}
🧠 STATUS : ANALYZED
💻 ACCESS : USER MODE

[{final_bar}] {iq}%

╔═━━━─── • ───━━━═╗
   🔍 SYSTEM REPORT
╚═━━━─── • ───━━━═╝
</pre>
"""

    await msg.edit_text(text, ENTRY_mode="HTML")


#==============WELCOME MSG===============


# ================= VIP USERS =================
VIP_USERS = [6175559434]

# ================= QUEUE =================
welcome_queue = deque()
active_workers = 0
MAX_WORKERS = 3

# ================= BUTTON =================
def get_start_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 Start Game", url="https://t.me/iim_Nikibot?start=start")]
    ])

# ================= SMART WELCOME =================
async def run_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE, member):

    user_id = member.id
    name = member.first_name
    username = f"@{member.username}" if member.username else "No Username"
    group_name = update.effective_chat.title
    mention = f"<a href='tg://user?id={user_id}'>{name}</a>"

    final_text = f"""
╭━━━〔 💖 WELCOME TO GROUP 💖 〕━━━╮

👤 Name: {mention}
🆔 ID: <code>{user_id}</code>
🔰 Username: {username}

━━━━━━━━━━━━━━━━━━━
🎮 PLAYER ENTRY SUCCESS
━━━━━━━━━━━━━━━━━━━

🏷️ Group: <b>{group_name}</b>

━━━━━━━━━━━━━━━━━━━
💻 SYSTEM STATUS:
██████████ 100% ✅

🔓 Access Granted!
━━━━━━━━━━━━━━━━━━━

🤖 <b>Niki Says:</b>
"Welcome baby 😘 enjoy & play 💕"
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
"""

    try:
        photos = await context.bot.get_user_profile_photos(user_id)

        if photos.total_count > 0:
            photo = photos.photos[0][-1].file_id

            await update.effective_chat.send_photo(
                photo=photo,
                caption=final_text,
                parse_mode="HTML",
                reply_markup=get_start_button()
            )
        else:
            await update.effective_chat.send_message(
                final_text,
                parse_mode="HTML",
                reply_markup=get_start_button()
            )
    except:
        await update.effective_chat.send_message(final_text, parse_mode="HTML")


# 🔹 NEW MEMBER JOIN (normal join)
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await run_welcome(update, context, member)


# 🔹 MEMBER APPROVE / REQUEST ACCEPT
async def member_update_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member:
        cm = update.chat_member
        if cm.new_chat_member.status == "member":
            await run_welcome(update, context, cm.new_chat_member.user)

async def member_update_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.chat_member:
        cm = update.chat_member

        old_status = cm.old_chat_member.status
        new_status = cm.new_chat_member.status

        if old_status in ["left", "kicked"] and new_status == "member":
            await run_welcome(update, context, cm.new_chat_member.user)

# ================= MAGIC =================
async def magic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    mention = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"

    msg = await update.message.reply_text("💻 Initializing hack...")

    steps = [
        "🔍 Scanning system...",
        "💣 Breaking firewall...",
        "📡 Accessing root...",
        "💰 Opening vault..."
    ]

    for step in steps:
        try:
            await asyncio.sleep(1.5)
            await msg.edit_text(f"💻 {step}")
        except:
            pass  # 🔥 anti-freeze

    # 🔥 USER DATA FIX
    u = get_user(user_id)

    if not u:
        u = {}

    if "money" not in u:
        u["money"] = 0

    if "magic_used" not in u:
        u["magic_used"] = False

    # ❌ SAME DESIGN (WITH BAR)
    if u["magic_used"]:
        await msg.edit_text(f"""
╭━━━〔 ❌ ACCESS DENIED 〕━━━╮

👤 {mention}
🛑 Reward already claimed!

💖 Niki Says:
"Ek hi chance milta hai 😏"

╰━━━━━━━━━━━━━━━━━━━━╯
""", parse_mode="HTML")
        return

    # 💰 REWARD
    reward = random.randint(10000, 20000)

    u["magic_used"] = True
    u["money"] += reward

    save_data()
    

    # ✅ FINAL (SAME BAR STYLE)
    try:
        await msg.edit_text(f"""
╭━━━〔 💰 HACK SUCCESSFUL 〕━━━╮

👤 {mention}
💰 Reward: <b>{reward}</b> coins
🏦 Total Balance: <b>{u['money']}</b> coins

💖 Niki Says:
"Wow 😍 tum lucky nikle!"

╰━━━━━━━━━━━━━━━━━━━━╯
""", parse_mode="HTML")
    except:
        pass

# ================= DART SOLO =================
async def dart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return
    
    user = update.effective_user
    user_id = user.id

    # 🔥 STRONG ARG PARSE (FIXED)
    text = update.message.text.strip().split()

    if len(text) > 1:
        bet_arg = text[1]
    else:
        bet_arg = None

    mention = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"

    # ❌ No bet
    if not bet_arg:
        await update.message.reply_text("❌ Use: /dart <amount>\nExample: /dart 1000")
        return

    try:
        bet = int(bet_arg)
    except:
        await update.message.reply_text("❌ Invalid amount")
        return

    # ❌ MIN BET CHECK
    if bet < 100:
        await update.message.reply_text("❌ Minimum bet 100 hai")
        return

    # 💾 SAFE USER SYSTEM
    user_id_str = str(user_id)

    if user_id_str not in data:
        data[user_id_str] = {"money": 0}

    u = data[user_id_str]

    if "money" not in u:
        u["money"] = 0

    # ❌ Not enough money
    if u["money"] < bet:
        await update.message.reply_text("❌ Paise kam hai")
        return

    # 💸 Deduct bet
    u["money"] -= bet
    save_data()
    

    # ================= HACKER LOADING =================
    msg = await update.message.reply_text("⚠️ Initializing dark protocol...")

    steps = [
        "🧠 Syncing neural aim...",
        "💻 Injecting target system...",
        "📡 Tracking wind velocity...",
        "🔓 Breaking aim firewall...",
        "⚡ Calibrating shot precision...",
        "🛰️ Locking final coordinates..."
    ]

    for step in steps:
        try:
            await asyncio.sleep(1)
            await msg.edit_text(f"⚠️ {step}")
        except:
            pass

    # ================= LOADING BAR =================
    for i in range(0, 101, 10):
        bar = "█" * (i // 10) + "▒" * (10 - (i // 10))
        glitch = ["", "⚡", "☠️", "✖️", "⚠️"]

        try:
            await msg.edit_text(f"""
💻 SYSTEM BREACH IN PROGRESS...

{bar} {i}% {glitch[i % len(glitch)]}
""")
        except:
            pass

        await asyncio.sleep(0.8)

    # ================= PREMIUM SCREEN =================
    await msg.edit_text(f"""
╭━━━〔 ☠️ DARK SYSTEM ☠️ 〕━━━╮

👤 {mention}

💀 Dart Solo Challenge Initialized
🔓 Access Level: ELITE
⚡ Mode: HACKED PRECISION

━━━━━━━━━━━━━━━━━━━
🔥 TARGET LOCK COMPLETE
━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    await asyncio.sleep(3)

    # ================= REAL DART =================
    dart_msg = await update.message.reply_dice(emoji="🎯")
    value = dart_msg.dice.value

    await asyncio.sleep(2)

    # ================= RESULT =================
    if value <= 3:
        result = f"""
╭━━━〔 ❌ SYSTEM FAILED 〕━━━╮

👤 {mention}
🎯 Score: {value}

💸 Lost: {bet}

💔 Niki Says:
"System hack fail ho gaya 😢"
╰━━━━━━━━━━━━━━━━━━━━╯
"""

    elif value == 6:
        win = bet * 3
        u["money"] += win
        save_data()
        

        result = f"""
╭━━━〔 💎 ROOT ACCESS GAINED 〕━━━╮

👤 {mention}
🎯 PERFECT HIT: {value}

💰 Won: {win} (3X)

🔥 Niki Says:
"OMG 😳 FULL CONTROL MIL GAYA!"
╰━━━━━━━━━━━━━━━━━━━━╯
"""

    else:
        win = bet * 2
        u["money"] += win
        save_data()
        

        result = f"""
╭━━━〔 💰 HACK SUCCESS 〕━━━╮

👤 {mention}
🎯 Score: {value}

💰 Won: {win}

💖 Niki Says:
"Nice hack 😘"
╰━━━━━━━━━━━━━━━━━━━━╯
"""

    await update.message.reply_text(result, parse_mode="HTML")

# ================= TRANSLATE COMMAND =================
async def tr(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    # ❌ must reply to a message
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Reply to a message and type /tr")
        return

    text = update.message.reply_to_message.text

    if not text:
        await update.message.reply_text("❌ Only text messages can be translated")
        return

    try:
        # 🌐 Translators
        en = GoogleTranslator(source='auto', target='en').translate(text)
        hi = GoogleTranslator(source='auto', target='hi').translate(text)
        or_ = GoogleTranslator(source='auto', target='or').translate(text)

        result = f"""
🌐 𝗧𝗥𝗔𝗡𝗦𝗟𝗔𝗧𝗜𝗢𝗡

🇬🇧 English:
{en}

🇮🇳 Hindi:
{hi}

🟠 Odia:
{or_}
"""

        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text("❌ Translation failed. Try again later.")


# ================= CONFIG =================

OWNER_ID = 6175559434
OWNER_USERNAME = "YTT_BISHAL"# 👉 apna Telegram user ID daal

# ================= STORAGE =================
BOT_STATUS = {}  # {chat_id: True/False}


# ================= ADMIN / OWNER CHECK =================
async def is_admin_or_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat = update.effective_chat

    # 👑 Owner always allowed
    if user_id == OWNER_ID:
        return True

    member = await context.bot.get_chat_member(chat.id, user_id)
    return member.status in ["administrator", "creator"]


# ================= CLOSE COMMAND =================
async def close_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # ❌ only group
    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Ye command sirf group me use hota hai!")

    # 🔐 check
    if not await is_admin_or_owner(update, context):
        return await update.message.reply_text("❌ Sirf admin ya owner hi bot band kar sakta hai!")

    BOT_STATUS[chat.id] = False

    await update.message.reply_text("🔒 Niki Bot ab is group me OFF ho gaya 💔")


# ================= OPEN COMMAND =================
async def open_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Ye command sirf group me use hota hai!")

    if not await is_admin_or_owner(update, context):
        return await update.message.reply_text("❌ Sirf admin ya owner hi bot ON kar sakta hai!")

    BOT_STATUS[chat.id] = True

    await update.message.reply_text("🔓 Niki Bot ab is group me ON ho gaya 🎮✨")


# ================= BLOCK SYSTEM =================
async def block_system(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    # ❌ only group
    if chat.type not in ["group", "supergroup"]:
        return

    status = BOT_STATUS.get(chat.id, True)

    if status:
        return  # bot ON

    user_id = update.effective_user.id

    # 👑 OWNER bypass
    if user_id == OWNER_ID:
        return

    # 👑 ADMIN bypass
    member = await context.bot.get_chat_member(chat.id, user_id)
    if member.status in ["administrator", "creator"]:
        return

    # ❌ block all commands
    if update.message and update.message.text and update.message.text.startswith("/"):
        await update.message.reply_text(
            "🚫 Niki Bot abhi OFF hai 💔\nAdmin ya owner se bolo open kare..."
        )
        return

        
#====================CHEACK BOT ACTIVE================
async def check_bot_active(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user_id = update.effective_user.id

    if chat.type not in ["group", "supergroup"]:
        return True

    status = BOT_STATUS.get(chat.id, True)

    if status:
        return True

    if user_id == OWNER_ID:
        return True

    member = await context.bot.get_chat_member(chat.id, user_id)
    if member.status in ["administrator", "creator"]:
        return True

    await update.message.reply_text("🚫 Bot OFF hai yaha 💔")
    return False

# ================= ADD FILTER =================
async def filter_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to a message/sticker")

    if len(context.args) == 0:
        return await update.message.reply_text("❌ Use: /filter name")

    name = context.args[0].lower()
    reply = update.message.reply_to_message
    chat_id = update.effective_chat.id

    data = {"type": None, "content": None}

    if reply.text:
        data["type"] = "text"
        data["content"] = reply.text

    elif reply.sticker:
        data["type"] = "sticker"
        data["content"] = reply.sticker.file_id

    elif reply.photo:
        data["type"] = "photo"
        data["content"] = reply.photo[-1].file_id
        data["caption"] = reply.caption

    else:
        return await update.message.reply_text("❌ Unsupported type")

    filters_col.update_one(
        {"chat_id": chat_id, "name": name},
        {"$set": data},
        upsert=True
    )

    await update.message.reply_text(f"✅ Filter '{name}' saved!")


# ================= DELETE FILTER =================
async def dfilter_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        return await update.message.reply_text("❌ Use: /dfilter name")

    name = context.args[0].lower()
    chat_id = update.effective_chat.id

    result = filters_col.delete_one({"chat_id": chat_id, "name": name})

    if result.deleted_count:
        await update.message.reply_text(f"🗑️ Filter '{name}' deleted!")
    else:
        await update.message.reply_text("❌ Filter not found")


# ================= AUTO FILTER CHECK =================
async def filter_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    chat_id = update.effective_chat.id
    

    if games.find_one({"_id": chat_id}):
        return
    try:
        filters_data = list(filters_col.find({"chat_id": chat_id}))
    except Exception as e:
        print("Filter Error:", e)
        return

    for f in filters_data:
        # 🔥 exact word match (no fake trigger)
        if re.search(rf"\b{re.escape(f['name'])}\b", text):

            try:
                if f["type"] == "text":
                    await update.message.reply_text(f["content"])

                elif f["type"] == "sticker":
                    await update.message.reply_sticker(f["content"])

                elif f["type"] == "photo":
                    await update.message.reply_photo(
                        photo=f["content"],
                        caption=f.get("caption") or ""
                    )
            except Exception as e:
                print("Send Error:", e)

            break  # ek hi filter chalega    

# ================= MODERATION SYSTEM =================



OWNER_USERNAME = "YTT_BISHAL"   # without @


# ================= ADMIN CHECK =================
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]




# ================= TIME PARSER =================
def parse_time(time_str):
    match = re.match(r"(\d+)([smhd])", time_str)
    if not match:
        return None

    value, unit = match.groups()
    value = int(value)

    if unit == "s":
        return timedelta(seconds=value)
    elif unit == "m":
        return timedelta(minutes=value)
    elif unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)


# ================= BAN =================
async def ban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin only command")

    user = get_user(update, context)
    if not user:
        return await update.message.reply_text("❌ User not found")

    if is_owner(user):
        return await update.message.reply_text("❌ Owner ko ban nahi kar sakte 😎")

    try:
        await update.effective_chat.ban_member(user.id)
        await update.message.reply_text(f"🔨 {user.first_name} banned!")
    except:
        await update.message.reply_text("❌ Ban failed")


# ================= UNBAN =================
async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin only command")

    user = get_user(update, context)
    if not user:
        return await update.message.reply_text("❌ User not found")

    try:
        await update.effective_chat.unban_member(user.id)
        await update.message.reply_text(f"✅ {user.first_name} unbanned!")
    except:
        await update.message.reply_text("❌ Unban failed")


# ================= MUTE =================
async def mute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin only command")

    user = get_user(update, context)
    if not user:
        return await update.message.reply_text("❌ User not found")

    if is_owner(user):
        return await update.message.reply_text("❌ Owner ko mute nahi kar sakte 😎")

    try:
        await update.effective_chat.restrict_member(
            user.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(f"🔇 {user.first_name} muted!")
    except:
        await update.message.reply_text("❌ Mute failed")


# ================= UNMUTE =================
async def unmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin only command")

    user = get_user(update, context)
    if not user:
        return await update.message.reply_text("❌ User not found")

    try:
        await update.effective_chat.restrict_member(
            user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await update.message.reply_text(f"🔊 {user.first_name} unmuted!")
    except:
        await update.message.reply_text("❌ Unmute failed")


# ================= TIMED MUTE =================
async def tmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin only command")

    if len(context.args) < 1:
        return await update.message.reply_text("❌ Use: /tmute 10m")

    duration = parse_time(context.args[0])
    if not duration:
        return await update.message.reply_text("❌ Invalid time")

    user = get_user(update, context)
    if not user:
        return await update.message.reply_text("❌ User not found")

    if is_owner(user):
        return await update.message.reply_text("❌ Owner ko mute nahi kar sakte 😎")

    until_time = datetime.utcnow() + duration

    try:
        await update.effective_chat.restrict_member(
            user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_time
        )
        await update.message.reply_text(f"⏳ {user.first_name} muted for {context.args[0]}")
    except:
        await update.message.reply_text("❌ Timed mute failed")


# ================= TIMED BAN =================
async def tban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("❌ Admin only command")

    if len(context.args) < 1:
        return await update.message.reply_text("❌ Use: /tban 10m")

    duration = parse_time(context.args[0])
    if not duration:
        return await update.message.reply_text("❌ Invalid time")

    user = get_user(update, context)
    if not user:
        return await update.message.reply_text("❌ User not found")

    if is_owner(user):
        return await update.message.reply_text("❌ Owner ko ban nahi kar sakte 😎")

    until_time = datetime.utcnow() + duration

    try:
        await update.effective_chat.ban_member(user.id, until_date=until_time)
        await update.message.reply_text(f"⛔ {user.first_name} banned for {context.args[0]}")
    except:
        await update.message.reply_text("❌ Timed ban failed")    

 

# ================= USERINFO =================
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
import asyncio

async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user

    user_data = get_user(user.id, user.first_name)

    name = user.first_name
    username = f"@{user.username}" if user.username else "No Username"
    mention = f"<a href='tg://user?id={user.id}'>{name}</a>"

    # 🏆 RANK
    users_only = {
        uid: u for uid, u in data.items()
        if isinstance(u, dict) and "money" in u
    }

    sorted_users = sorted(users_only.items(), key=lambda x: x[1]["money"], reverse=True)
    rank = next((i+1 for i,(uid,u) in enumerate(sorted_users) if uid==str(user.id)), "N/A")

    # 👑 OWNER CHECK
    is_owner = user.username and user.username.lower() == "YTT_BISHAL"

    # 🔥 DISPLAY FIX (ONLY HERE CHANGE)
    balance_text = "∞" if is_owner else f"₹{user_data.get('money',0)}"
    rank_text = "∞" if is_owner else rank

    # ================= OWNER =================
    if is_owner:

        msg = await update.message.reply_text("⚡ Initializing NIKI CORE...")

        for i in range(0, 101, 10):
            bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
            try:
                await msg.edit_text(f"""
<pre>
⚡ SYSTEM BOOTING...

[{bar}] {i}%

🔓 Accessing Owner Core...
</pre>
""", parse_mode="HTML")
                await asyncio.sleep(0.3)
            except:
                pass

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎮 GAME", callback_data="game_panel"),
                InlineKeyboardButton("💖 LOVE", callback_data="romantic_panel")
            ],
            [
                InlineKeyboardButton("🛡️ ADMIN", callback_data="admin_panel"),
                InlineKeyboardButton("⚡ POWER", callback_data="power_panel")
            ],
            [
                InlineKeyboardButton("📊 STATS", callback_data="stats_panel"),
                InlineKeyboardButton("💞 PARTNER", callback_data="partner_panel")
            ]
        ])

        text = f"""  
<pre>  
╔════════════════════════════════════════════╗  
   🌈 N E O N   R G B   C O R E   S Y S T E M 🌈  
╠════════════════════════════════════════════╣  
   ⚡ 𝐑𝟎𝟎𝐓 𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄𝐃 ⚡  
   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%  
╚════════════════════════════════════════════╝  
</pre>  

💀 <b>⟦ 𝐒𝐘𝐒𝐓𝐄𝐌 𝐁𝐑𝐄𝐀𝐂𝐇 𝐒𝐔𝐂𝐂𝐄𝐒𝐒 ⟧</b> 💀    
🔥 <b>⟦ 𝐍𝐈𝐊𝐈 𝐂𝐎𝐑𝐄 𝐅𝐔𝐋𝐋𝐘 𝐔𝐍𝐋𝐎𝐂𝐊𝐄𝐃 ⟧</b> 🔥    

<pre>  
[ SYSTEM LOGS ]  
> Injecting Owner Privileges...  
> Bypassing Security Layer...  
> Accessing Core Memory...  
> Finalizing Control...  
</pre>  

🌈✨🌈 <b>𝐎ᴡɴᴇʀ 𝐆ᴏ𝐝 𝐌𝐨𝐝𝐞 𝐀𝐜𝐭𝐢𝐯𝐞</b> 🌈✨🌈    
👑 <b>{mention}</b>  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

🔴 ➤ <b>𝐈𝐃        :</b> <code>{user.id}</code>    
🟢 ➤ <b>𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄  :</b> {username}    
🔵 ➤ <b>𝐒𝐓𝐀𝐓𝐔𝐒    :</b> ⚡ 𝐒𝐔𝐏𝐑𝐄𝐌𝐄 𝐎𝐖𝐍𝐄𝐑    
  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

🟣 ➤ <b>𝐁𝐑𝐀𝐈𝐍     :</b> ∞ 𝐆𝐎𝐃 𝐋𝐄𝐕𝐄𝐋    
🟡 ➤ <b>𝐏𝐎𝐖𝐄𝐑     :</b> ∞ 𝐂𝐎𝐍𝐓𝐑𝐎𝐋    
🟠 ➤ <b>𝐀𝐂𝐂𝐄𝐒𝐒    :</b> 𝐑𝐎𝐎𝐓 𝐀𝐂𝐂𝐄𝐒𝐒    

━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💰 ➤ <b>𝐁𝐀𝐋𝐀𝐍𝐂𝐄  :</b> {balance_text}  
🏆 ➤ <b>𝐑𝐀𝐍𝐊     :</b> {rank_text}  
⚔ ➤ <b>𝐊𝐈𝐋𝐋𝐒    :</b> {user_data.get("kills",0)}  
❤️ ➤ <b>𝐒𝐓𝐀𝐓𝐔𝐒   :</b> {"Alive ❤️" if not user_data.get("dead", False) else "Dead ☠️"}  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💎 <b>➤ 𝐂𝐎𝐑𝐄 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 :</b>    
🌈 "System tera slave hai 😈    
💖 NIKI tera heart hai    
🔥 Commands tere hukum me hai    
👑 Tu hi asli creator hai"  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💎 <b>➤ 𝐂𝐎𝐑𝐄 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 :</b>    
🌈 "System tera slave hai 😈    
💖 NIKI tera heart hai    
🔥 Commands tere hukum me hai    
👑 Tu hi asli creator hai"  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💌 <b>➤ 𝐍𝐈𝐊𝐈 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 :</b>    
"💖 Mere pyare baby Ritvi…    
Tu Vishal ki duniya hai 😘    
Aur Vishal… tu mera king 👑    
Main NIKI hoon… tum dono ki 💕    
Forever saath rahoge tum dono 🌹"  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
⚠️ <b>➤ 𝐅𝐈𝐑𝐄𝐖𝐀𝐋𝐋 :</b>    
🚫 Unauthorized = BAN ⚡    
💀 Intruder = TERMINATED    

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  

<pre>  
╔══════════════════════════════╗  
        👑 𝐕ɪꜱʜᴀʟ 👑  
╠══════════════════════════════╣  
   ❤️ LOVE STATUS: IMMORTAL ❤️  
╚══════════════════════════════╝  
</pre>  

💖 <b>𝐕ɪꜱʜ𝐀𝐋 ❤️ 𝐑𝐈𝐓𝐕𝐈</b> 💖    
🌹 <i>𝐈ɴꜰɪɴɪᴛ𝐞 𝐋𝐨𝐯𝐞 • 𝐍𝐞𝐨𝐧 𝐁𝐨𝐧𝐝 • 𝐅𝐨𝐫𝐞𝐯𝐞𝐫 ♾️</i>  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
🔥 <b>⟦ 𝐍𝐈𝐊𝐈 𝐂𝐎𝐑𝐄 : 𝐎𝐍𝐋𝐈𝐍𝐄 ⟧</b>    
🚀 <b>⟦ 𝐌𝐎𝐃𝐄 : 𝐆𝐎𝐃 𝐌𝐎𝐃𝐄 ⟧</b>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━  
"""  


        await msg.edit_text(text, parse_mode="HTML", reply_markup=buttons)

    # ================= NORMAL USER =================
    else:
        await update.message.reply_text(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇺 🇸 🇪 🇷  ☠️ 🇮 🇳 🇫 🇴 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name: {mention}
🆔 ID: <code>{user.id}</code>
🔰 Username: {username}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: {balance_text}
🏆 Rank: {rank_text}
⚔ Kills: {user_data.get("kills",0)}
❤️ Status: {"Alive ❤️" if not user_data.get("dead", False) else "Dead ☠️"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")


# ================= BUTTON LOGIC =================
async def userinfo_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # 🎮 GAME + ECONOMY
    if data == "game_panel":
        text = """✨🌸 ╔═══〔 💖 𝗡𝗜𝗞𝗜 𝗕𝗢𝗧 𝗠𝗘𝗚𝗔 𝗨𝗣𝗗𝗔𝗧𝗘 💖 〕═══╗ 🌸✨

🥀 Hey meri cute family 😘  
💫 Niki ab aur bhi smart + powerful ho gayi hai 💕

━━━━━━━━━━━━━━━━━━━━━━━
🎮 ⚡ 𝗚𝗔𝗠𝗘 & 𝗙𝗨𝗡 𝗭𝗢𝗡𝗘 ⚡

⚔️ /kill  ➤ attack karo 😈  
💰 /rob   ➤ paisa loot lo 😏  
🎯 /dart  ➤ luck try karo  
🧠 /brain ➤ IQ check 😎  

🎮 Full fun mode ON 🔥

━━━━━━━━━━━━━━━━━━━━━━━
💸 💎 𝗘𝗖𝗢𝗡𝗢𝗠𝗬 𝗦𝗬𝗦𝗧𝗘𝗠 💎

💰 /balance ➤ paisa check  
🎁 /daily   ➤ daily reward  
🎁 /claim   ➤ bonus claim  
❤️ /revive  ➤ revive ho jao  

━━━━━━━━━━━━━━━━━━━━━━━
🤖💖 𝗡𝗜𝗞𝗜 𝗦𝗔𝗬𝗦:

"Main sirf bot nahi…  
thodi cute, thodi crazy,  
aur thodi tumhari hoon 😘💕  

active raho na baby 😏✨"

╚═══════════════════════════════╝ 💫"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # 💖 ROMANTIC
    elif data == "romantic_panel":
        text = """💍 💖 𝗟𝗢𝗩𝗘 & 𝗥𝗢𝗠𝗔𝗡𝗧𝗜𝗖 💖

😘 /kiss     ➤ pyaar bhara kiss 😘  
🤗 /hug      ➤ tight warm hug 🤗  
👋 /slap     ➤ naughty slap 😜  
👊 /punch    ➤ funny punch 😂  
🦶 /kick     ➤ cute kick 😏  
🥰 /cuddle   ➤ close cuddle 💞  
😜 /tickle   ➤ hasi wali tickle 😆  
💘 /love     ➤ love express 💖  

━━━━━━━━━━━━━━━━━━━━━━━
💌 💕 𝗥𝗢𝗠𝗔𝗡𝗧𝗜𝗖 𝗙𝗘𝗘𝗟𝗜𝗡𝗚 💕

"Thoda pyaar, thoda masti 😘  
Niki ke saath full romance 💞"

💖 Pyaar full ON 😍🔥"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # 🛡️ ADMIN
    elif data == "admin_panel":
        text = """🛡️ 🔥 𝗔𝗗𝗠𝗜𝗡 𝗣𝗢𝗪𝗘𝗥 🔥

🔨 /ban ➤ ban karo  
🔓 /unban ➤ wapas lao  
🔇 /mute ➤ chup karao  
🔊 /unmute ➤ awaaz wapas  

⏳ /tmute 2h ➤ temp mute  
⛔ /tban 1d ➤ temp ban  

👑 Only admins use kare!"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # ⚡ POWER
    elif data == "power_panel":
        text = """⚡⚡ 𝗣𝗢𝗪𝗘𝗥 𝗖𝗢𝗥𝗘 ⚡⚡

🧠 Brain : ∞  
🔥 Power : ∞  
🚀 Mode  : GOD MODE  

💀 System control tumhare haath me 😈"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # 📊 STATS
    elif data == "stats_panel":
        text = """📊 🌈 𝗦𝗧𝗔𝗧𝗦 𝗣𝗔𝗡𝗘𝗟 🌈

🧠 Brain : ∞  
😍 Look  : ∞  
💪 Power : ∞  

🔥 Perfect Profile 😎"""
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # 💘 LOVE
    elif data == "love_panel":
        text = """💖 💞 𝗟𝗢𝗩𝗘 𝗖𝗢𝗥𝗘 💞 💖

👑 Vishal ❤️ Ritvi  
🌹 Infinite Love ♾️  
💫 Perfect Couple  

🥀 "Ek dusre ke liye bane ho 💕" """
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # 👫 PARTNER
    elif data == "partner_panel":
        text = """💖✨ 𝗩𝗜𝗦𝗛𝗔𝗟 ❤️ 𝗥𝗜𝗧𝗩𝗜 ✨💖

🌹 "Tum dono ek kahani ho,  
jisme pyaar kabhi khatam nahi hota 💕  

Ritvi tum uski smile ho 😘  
Aur Vishal tum uska world 👑  

Forever saath rahoge tum dono 💞" """
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="back_main")]])
        await query.message.edit_text(text, reply_markup=buttons)

    # 🔙 BACK BUTTON
    elif data == "back_main":
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎮 GAME", callback_data="game_panel"),
                InlineKeyboardButton("💖 LOVE", callback_data="romantic_panel")
            ],
            [
                InlineKeyboardButton("🛡️ ADMIN", callback_data="admin_panel"),
                InlineKeyboardButton("⚡ POWER", callback_data="power_panel")
            ],
            [
                InlineKeyboardButton("📊 STATS", callback_data="stats_panel"),
                InlineKeyboardButton("💞 PARTNER", callback_data="partner_panel")
            ]
        ])
        await query.message.edit_text("🔙 Back to menu", reply_markup=buttons)




#=======================CARD GAME =====================
import random
import asyncio
import time

card_games = {}

cards = {
"a": (1, 13),
"b": (1, 13),
"c": (1, 13),
"d": (1, 13)
}

#================ AUTO SYSTEM =================

async def auto_monitor():
    while True:
        await asyncio.sleep(5)

        for chat_id in list(card_games.keys()):
            game = card_games.get(chat_id)
            if not game:
                continue

            # 🟢 1 MIN AUTO START
            if not game.get("started") and time.time() - game["start_time"] > 60:
                if len(game["players"]) < 2:
                    starter = game["players"][0]

                    user_data = get_user(starter.id, starter.first_name)
                    user_data["money"] += game["bet"]
                    save_data()

                    await bot.send_message(chat_id, f"""  
❌ 𝐍ᴏ 𝐏ʟᴀʏᴇʀ  

💸 𝐁ᴇ𝐭 𝐑𝐞𝐟𝐮𝐧𝐝𝐞𝐝 → ₹{game['bet']}  
👤 {starter.mention_html()}  
""", parse_mode="HTML")

                    del card_games[chat_id]
                    continue

                game["started"] = True
                await start_match(chat_id)

            # 🤖 AUTO PLAY (20 sec idle)
            if game.get("started") and time.time() - game["last_action"] > 20:
                await auto_play(chat_id)




#================ START GAME =================

async def card(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id in card_games:
        return await update.message.reply_text("⚠️ 𝐆ᴀᴍᴇ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ")

    if not context.args:
        return await update.message.reply_text("💸 𝐔ꜱᴇ: /card 200")

    bet = int(context.args[0])

    if bet < 200:
        return await update.message.reply_text("❌ 𝐌ɪɴɪᴍᴜᴍ 𝐁ᴇᴛ ₹200")

    user_data = get_user(user.id, user.first_name)
    if user_data["money"] < bet:
        return await update.message.reply_text("❌ 𝐍ᴏᴛ 𝐞ɴᴏᴜɢʜ 𝐁ᴀʟᴀɴᴄᴇ")

    user_data["money"] -= bet
    save_data()

    card_games[chat_id] = {
        "players": [user],
        "bet": bet,
        "round": 1,
        "turn": 0,
        "scores": {},
        "round_scores": {},
        "joined": {user.id},
        "start_time": time.time(),
        "last_action": time.time(),
        "started": False
    }

    msg = await update.message.reply_text(f"""

╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐂ᴀʀᴅ 𝐀ʀᴇɴᴀ ⚡
╚═══━━━─── • ───━━━═══╝

👑 {user.mention_html()} 𝐬ᴛᴀʀᴛᴇᴅ 𝐠ᴀᴍᴇ

💰 𝐁ᴇᴛ: ₹{bet}
👥 1/5 𝐏ʟᴀʏᴇʀꜱ

👉 𝐓ʏᴘᴇ:
/joinbet {bet}

⏳ 30 𝐬ᴇᴄ ᴛᴏ ᴊᴏɪɴ...
""", parse_mode="HTML")


#================ JOIN =================

async def joinbet(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in card_games:
        return  

    game = card_games[chat_id]  

    if len(game["players"]) >= 5:  
        return await update.message.reply_text("❌ 𝐌ᴀx 5 𝐩ʟᴀʏᴇʀꜱ")  

    if user.id in game["joined"]:
        return await update.message.reply_text("❌ 𝐀ʟʀᴇᴀᴅʏ 𝐉ᴏɪɴᴇᴅ")

    if not context.args or int(context.args[0]) != game["bet"]:
        return

    user_data = get_user(user.id, user.first_name)  
    if user_data["money"] < game["bet"]:  
        return await update.message.reply_text("❌ 𝐍ᴏᴛ 𝐞ɴᴏᴜɢʜ 𝐁ᴀʟᴀɴᴄᴇ")  

    user_data["money"] -= game["bet"]  
    save_data()  

    game["players"].append(user)  
    game["joined"].add(user.id)  
    game["last_action"] = time.time()

    await update.message.reply_text(  
        f"✅ {user.mention_html()} 𝐣ᴏɪɴᴇᴅ 𝐭ʜᴇ 𝐦ᴀᴛᴄʜ!",  
        parse_mode="HTML"  
    )


#================ MATCH =================

async def start_match(chat_id):
    game = card_games[chat_id]
    players = game["players"]

    for p in players:
        game["scores"][p.id] = 0  

    vs_text = " 🆚 ".join([p.mention_html() for p in players])

    msg = await bot.send_message(chat_id, f"""  
━━━━━━━━━━━━━━━━━━━━━━  
⚡ 𝐌ᴀᴛᴄʜ 𝐅ᴏᴜ𝐍𝐃 ⚡  
━━━━━━━━━━━━━━━━━━━━━━  

{vs_text}  

⚡ 𝐋ᴏᴀᴅɪɴɢ...  
""", parse_mode="HTML")  

    for i in range(0, 101, 20):  
        bar = "▓" * (i//10) + "░" * (10 - i//10)  
        try:  
            await msg.edit_text(f"""  
━━━━━━━━━━━━━━━━━━━━━━  
⚡ 𝐌ᴀᴛᴄʜ 𝐅𝐎𝐔𝐍𝐃 ⚡  
━━━━━━━━━━━━━━━━━━━━━━  

{vs_text}  

[{bar}] {i}%  
""", parse_mode="HTML")  
            await asyncio.sleep(0.6)  
        except:  
            pass  

    await asyncio.sleep(1)  
    await start_round(chat_id)


#================ ROUND =================

async def start_round(chat_id):
    game = card_games[chat_id]

    if game["round"] > 3:  
        return await end_game(chat_id)  

    game["turn"] = 0  
    game["round_scores"] = {p.id: 0 for p in game["players"]}  

    msg = await bot.send_message(chat_id, f"""

╔═══━━━─── • ───━━━═══╗
⚡ 𝐑𝐎𝐔𝐍𝐃 {game['round']} ⚡
╚═══━━━─── • ───━━━═══╝

🎮 𝐒ᴛᴀʀᴛɪɴɢ...
""")

    for i in range(0, 101, 25):  
        bar = "█" * (i//10) + "░" * (10 - i//10)  
        try:  
            await msg.edit_text(f"""

╔═══━━━─── • ───━━━═══╗
⚡ 𝐑𝐎𝐔𝐍𝐃 {game['round']} ⚡
╚═══━━━─── • ───━━━═══╝

[{bar}] {i}%
""")
            await asyncio.sleep(0.5)
        except:
            pass

    await msg.edit_text(f"""

╔═══━━━─── • ───━━━═══╗
⚡ 𝐑𝐎𝐔𝐍𝐃 {game['round']} ⚡
╚═══━━━─── • ───━━━═══╝

🎴 𝐂ʜᴏᴏꜱᴇ:
🟥 𝐀   🟥 𝐁   🟥 𝐂   🟥 𝐃

𝐅ʟɪᴘ 𝐊ᴇ 𝐋ɪʏᴇ 𝐘ᴇ 𝐔ꜱᴇ 𝐊ᴀʀᴏ
👉 /flip a
""")


#================ FLIP =================

async def flip(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in card_games:
        return  

    game = card_games[chat_id]  
    players = game["players"]  

    current = players[game["turn"] % len(players)]  

    if user.id != current.id:  
        return  

    choice = context.args[0].lower()  
    val = random.randint(1, 13)

    game["round_scores"][user.id] += val  
    game["turn"] += 1  
    game["last_action"] = time.time()

    msg = await update.message.reply_text(  
        f"🎴 {user.mention_html()} 𝐢𝐬 𝐟𝐥𝐢𝐩𝐩𝐢𝐧𝐠...",  
        parse_mode="HTML"  
    )  

    await asyncio.sleep(1)  

    await msg.edit_text(  
        f"🎴 {user.mention_html()} → {choice.upper()} = {val}",  
        parse_mode="HTML"  
    )  

    if game["turn"] >= len(players) * 2:  
        await end_round(chat_id)


#================ AUTO PLAY =================

async def auto_play(chat_id):
    game = card_games.get(chat_id)
    if not game:
        return

    players = game["players"]
    current = players[game["turn"] % len(players)]

    val = random.randint(1, 13)

    game["round_scores"][current.id] += val
    game["turn"] += 1
    game["last_action"] = time.time()

    await bot.send_message(chat_id,
        f"🤖 AUTO PLAY → {current.first_name} = {val}"
    )

    if game["turn"] >= len(players) * 2:
        await end_round(chat_id)


#================ END ROUND =================

async def end_round(chat_id):
    game = card_games[chat_id]
    players = game["players"]

    winner = max(players, key=lambda p: game["round_scores"][p.id])

    game["scores"][winner.id] += 10  

    msg = await bot.send_message(chat_id, f"""  
━━━━━━━━━━━━━━━━━━━━━━  
⚡ 𝐑𝐎𝐔𝐍𝐃 𝐑𝐄𝐒𝐔𝐋𝐓 ⚡  
━━━━━━━━━━━━━━━━━━━━━━  

⚡ 𝐂𝐚𝐥𝐜𝐮𝐥𝐚𝐭𝐢𝐧𝐠...  
""")  

    await asyncio.sleep(1)

    score_text = "\n".join([f"{p.first_name}: {game['round_scores'][p.id]}" for p in players])

    await msg.edit_text(f"""  
━━━━━━━━━━━━━━━━━━━━━━  
⚡ 𝐑𝐎𝐔𝐍𝐃 𝐑𝐄𝐒𝐔𝐋𝐓 ⚡  
━━━━━━━━━━━━━━━━━━━━━━  

{score_text}  

🏆 𝐖ɪɴɴᴇʀ: {winner.first_name}  
+10 𝐗𝐏  
""")  

    game["round"] += 1  
    await asyncio.sleep(4)  
    await start_round(chat_id)


#================ FINAL =================

async def end_game(chat_id):
    game = card_games[chat_id]
    players = game["players"]

    winner = max(players, key=lambda p: game["scores"][p.id])

    total_pool = game["bet"] * len(players)

    winner_data = get_user(winner.id, winner.first_name)  
    winner_data["money"] += total_pool  
    save_data()  

    photos = await bot.get_user_profile_photos(winner.id)  
    photo = photos.photos[0][-1].file_id if photos.total_count > 0 else None  

    score_text = "\n".join([f"{p.first_name}: {game['scores'][p.id]}" for p in players])

    text = f"""

╔═══━━━─── • ───━━━═══╗
🏆 𝐅𝐈𝐍𝐀𝐋 𝐖𝐈𝐍𝐍𝐄𝐑 🏆
╚═══━━━─── • ───━━━═══╝

👑 {winner.mention_html()}

━━━━━━━━━━━━━━━━━━━━━━
📊 𝐅𝐈𝐍𝐀𝐋 𝐒𝐂𝐎𝐑𝐄
━━━━━━━━━━━━━━━━━━━━━━

{score_text}

━━━━━━━━━━━━━━━━━━━━━━

💰 𝐖𝐨𝐧: {total_pool}

🏆 𝐖ɪɴɴᴇʀ: {winner.mention_html()}

🔥 𝐋𝐞𝐠𝐞𝐧𝐝 𝐏𝐥𝐚𝐲𝐞𝐫 😈
✨ 𝐌𝐚𝐬𝐭𝐞𝐫 𝐎𝐟 𝐂𝐚𝐫𝐝𝐬
"""

            
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

user_choice = {}
duel_games = {}
duel_choice = {}

# ================= START =================

async def coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
╔═══━━━─── • ───━━━═══╗
     🪙 𝐂𝐎𝐈𝐍 𝐆𝐀𝐌𝐄 🪙
╚═══━━━─── • ───━━━═══╝

👉 𝐂𝐡𝐨𝐨𝐬𝐞:
/head  
/tail
""", parse_mode="HTML")


async def cduel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
╔═══━━━─── • ───━━━═══╗
     ⚔️ 𝐃𝐔𝐄𝐋 𝐆𝐀𝐌𝐄 ⚔️
╚═══━━━─── • ───━━━═══╝

👉 𝐂𝐡𝐨𝐨𝐬𝐞:
/dhead  
/dtail
""", parse_mode="HTML")

# ================= SINGLE =================

async def head(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_choice[user.id] = "heads"

    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
   ⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀ𝐦𝐞 ⚡
╚═══━━━─── • ───━━━═══╝

👤 {user.mention_html()}
🎯 𝐇𝐞𝐚𝐝𝐬 𝐒𝐞𝐥𝐞𝐜𝐭𝐞𝐝

━━━━━━━━━━━━━━━━━━━━━━
💸 /bet 200
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")


async def tail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_choice[user.id] = "tails"

    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
   ⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀ𝐦𝐞 ⚡
╚═══━━━─── • ───━━━═══╝

👤 {user.mention_html()}
🎯 𝐓𝐚𝐢𝐥𝐬 𝐒𝐞𝐥𝐞𝐜𝐭𝐞𝐝

━━━━━━━━━━━━━━━━━━━━━━
💸 /bet 200
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")


async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in user_choice:
        return await update.message.reply_text("❌ /head or /tail first")

    bet = int(context.args[0])
    if bet < 200:
        return await update.message.reply_text("❌ Min ₹200")

    user_data = get_user(user.id, user.first_name)

    if user_data["money"] < bet:
        return await update.message.reply_text("❌ No Balance")

    choice = user_choice[user.id]

    user_data["money"] -= bet
    save_data()

    msg = await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
     🪙 𝐂𝐎𝐈𝐍 𝐅𝐋𝐈𝐏 🪙
╚═══━━━─── • ───━━━═══╝

👤 {user.mention_html()}
🎯 {choice}
💰 ₹{bet}

━━━━━━━━━━━━━━━━━━━━━━
🎲 𝐅𝐥𝐢𝐩𝐩𝐢𝐧𝐠...
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    d = await update.message.reply_dice("🪙")
    result = "heads" if d.dice.value <= 3 else "tails"

    if result == choice:
        win = bet * 2
        user_data["money"] += win
        status = "🎉 WIN"
    else:
        win = 0
        status = "💀 LOST"

    save_data()

    await msg.edit_text(f"""
╔═══━━━─── • ───━━━═══╗
      🏆 𝐑𝐄𝐒𝐔𝐋𝐓 🏆
╚═══━━━─── • ───━━━═══╝

👤 {user.mention_html()}
🪙 {result}

━━━━━━━━━━━━━━━━━━━━━━
{status}
💰 Win: ₹{win}
💳 Balance: ₹{user_data["money"]}
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    del user_choice[user.id]

# ================= DUEL =================

async def dhead(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    duel_choice[user.id] = "heads"

    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝

━━━━━━━━━━━━━━━━━━━━━━
    ⚔️ 𝐃𝐔𝐄𝐋 𝐂𝐇𝐎𝐈𝐂𝐄⚔️
━━━━━━━━━━━━━━━━━━━━━━

👤 {user.mention_html()}
🎯 𝐇𝐞𝐚𝐝𝐬 𝐒𝐞𝐥𝐞𝐜𝐭𝐞𝐝

━━━━━━━━━━━━━━━━━━━━━━
💸 𝐍𝐨𝐰 → /dbet 200
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")


async def dtail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    duel_choice[user.id] = "tails"

    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝

━━━━━━━━━━━━━━━━━━━━━━
    ⚔️ 𝐃𝐔𝐄𝐋 𝐂𝐇𝐎𝐈𝐂𝐄⚔️
━━━━━━━━━━━━━━━━━━━━━━

👤 {user.mention_html()}
🎯 𝐓𝐚𝐢𝐥𝐬 𝐒𝐞𝐥𝐞𝐜𝐭𝐞𝐝

━━━━━━━━━━━━━━━━━━━━━━
💸 𝐍𝐨𝐰 → /dbet 200
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")


async def dbet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if user.id not in duel_choice:
        return await update.message.reply_text("❌ /dhead or /dtail first")

    bet = int(context.args[0])

    if chat_id in duel_games:
        return await update.message.reply_text("⚠️ 𝐆𝐚𝐦𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐑𝐮𝐧𝐧𝐢𝐧𝐠")

    user_data = get_user(user.id, user.first_name)

    if user_data["money"] < bet:
        return await update.message.reply_text("❌ 𝐍𝐨 𝐁𝐚𝐥𝐚𝐧𝐜𝐞")

    # 💸 p1 deduct
    user_data["money"] -= bet
    save_data()

    duel_games[chat_id] = {"p1": user, "bet": bet}

    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝
━━━━━━━━━━━━━━━━━━━━━━
   ⚔️ 𝐃𝐔𝐄𝐋 𝐂𝐑𝐄𝐀𝐓𝐄𝐃⚔️
━━━━━━━━━━━━━━━━━━━━━━

👑 {user.mention_html()}
💰 𝐁𝐞𝐭: ₹{bet}

━━━━━━━━━━━━━━━━━━━━━━
👉 /join {bet}
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if chat_id not in duel_games:
        return

    game = duel_games[chat_id]
    p1 = game["p1"]
    bet = game["bet"]

    # ❌ self join
    if user.id == p1.id:
        return await update.message.reply_text("❌ 𝐘𝐨𝐮 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐉𝐨𝐢𝐧𝐞𝐝")

    p1_data = get_user(p1.id, p1.first_name)
    p2_data = get_user(user.id, user.first_name)

    if p2_data["money"] < bet:
        return await update.message.reply_text("❌ 𝐍𝐨 𝐁𝐚𝐥𝐚𝐧𝐜𝐞")

    # 💸 p2 deduct
    p2_data["money"] -= bet
    save_data()

    # ⚔️ MATCH START
    msg = await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝
━━━━━━━━━━━━━━━━━━━━━━
   ⚔️ 𝐌𝐀𝐓𝐂𝐇 𝐒𝐓𝐀𝐑𝐓 ⚔️
━━━━━━━━━━━━━━━━━━━━━━

{p1.mention_html()} 🆚 {user.mention_html()}

[░░░░░░░░░░] 0%
""", parse_mode="HTML")

    import asyncio
    for i in range(0, 101, 20):
        bar = "█" * (i//10) + "░" * (10 - i//10)
        try:
            await msg.edit_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝
━━━━━━━━━━━━━━━━━━━━━━
    ⚔️ 𝐌𝐀𝐓𝐂𝐇 𝐒𝐓𝐀𝐑𝐓 ⚔️
━━━━━━━━━━━━━━━━━━━━━━

{p1.mention_html()} 🆚 {user.mention_html()}

[{bar}] {i}%
""", parse_mode="HTML")
            await asyncio.sleep(0.5)
        except:
            pass

    # 🎲 flip
    d1 = await update.message.reply_dice("🪙")
    d2 = await update.message.reply_dice("🪙")

    # 🤝 TIE REFUND
    if d1.dice.value == d2.dice.value:
        p1_data["money"] += bet
        p2_data["money"] += bet
        save_data()

        return await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
  ⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝
━━━━━━━━━━━━━━━━━━━━━━
    🤝 𝐓𝐈𝐄 𝐌𝐀𝐓𝐂𝐇 🤝
━━━━━━━━━━━━━━━━━━━━━━

{p1.mention_html()} 🎲 {d1.dice.value}
{user.mention_html()} 🎲 {d2.dice.value}

━━━━━━━━━━━━━━━━━━━━━━
💸 𝐑𝐞𝐟𝐮𝐧𝐝 𝐓𝐨 𝐁𝐨𝐭𝐡
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    # 🏆 winner
    if d1.dice.value > d2.dice.value:
        winner = p1
    else:
        winner = user

    total = bet * 2

    win_data = get_user(winner.id, winner.first_name)
    win_data["money"] += total
    save_data()

    text = f"""
╔═══━━━─── • ───━━━═══╗
  ⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝
━━━━━━━━━━━━━━━━━━━━━━
    🏆 𝐃𝐔𝐄𝐋 𝐑𝐄𝐒𝐔𝐋𝐓 🏆
━━━━━━━━━━━━━━━━━━━━━━
{p1.mention_html()} 🎲 {d1.dice.value}
{user.mention_html()} 🎲 {d2.dice.value}

━━━━━━━━━━━━━━━━━━━━━━
🏆 𝐖𝐢𝐧𝐧𝐞𝐫 → {winner.mention_html()}
💰 𝐖𝐢𝐧 → ₹{total}
💳 𝐁𝐚𝐥𝐚𝐧𝐜𝐞 → ₹{win_data["money"]}
━━━━━━━━━━━━━━━━━━━━━━
"""

    photos = await context.bot.get_user_profile_photos(winner.id)

    if photos.total_count > 0:
        msg2 = await context.bot.send_photo(
            chat_id,
            photos.photos[0][-1].file_id,
            caption=text,
            parse_mode="HTML"
        )
    else:
        msg2 = await context.bot.send_message(chat_id, text, parse_mode="HTML")

    try:
        await context.bot.pin_chat_message(chat_id, msg2.message_id)
    except:
        pass

    del duel_games[chat_id]

#==========================SLOT MACHINE =================

import random
from telegram import Update
from telegram.ext import ContextTypes

#==========================SLOT MACHINE =================

reels = ["🍒", "🍋", "7️⃣", "⭐", "💎"]
slot_stats = {}

# ================= GUIDE =================
async def slot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝

┏━━━━━━━━━━━ 🎰 ━━━━━━━━━━━┓
🎰 𝐒𝐋𝐎𝐓 𝐌𝐀𝐂𝐇𝐈𝐍𝐄
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 {user.mention_html()}

┏━━━━━━━━━━━━━━━━━━━━━━┓
💸 𝐔𝐬𝐞 → /slot 200
┗━━━━━━━━━━━━━━━━━━━━━━┛

💎 5x Jackpot  
🔥 3x Big Win  
✨ 2x Win  
""", parse_mode="HTML")


# ================= SLOT =================
async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not context.args:
        return await slot_cmd(update, context)

    bet = int(context.args[0])

    if bet < 200:
        return await update.message.reply_text("❌ 𝐌𝐢𝐧 ₹200")

    user_data = get_user(user.id, user.first_name)

    if user_data["money"] < bet:
        return await update.message.reply_text("❌ 𝐍𝐨 𝐁𝐚𝐥𝐚𝐧𝐜𝐞")

    # 💸 deduct
    user_data["money"] -= bet
    save_data()

    # 🎰 REAL TELEGRAM SLOT
    dice_msg = await update.message.reply_dice("🎰")
    value = dice_msg.dice.value

    # 🎯 RESULT LOGIC
    if value == 64:
        final = ["💎", "💎", "💎"]
        win = bet * 5
        result = "💎 𝐌𝐄𝐆𝐀 𝐉𝐀𝐂𝐊𝐏𝐎𝐓"
        status = "🎉 𝐖𝐈𝐍"
    elif value >= 50:
        final = ["7️⃣", "7️⃣", random.choice(reels)]
        win = bet * 3
        result = "🔥 𝐉𝐀𝐂𝐊𝐏𝐎𝐓"
        status = "🎉 𝐖𝐈𝐍"
    elif value >= 30:
        sym = random.choice(reels)
        final = [sym, sym, random.choice(reels)]
        win = bet * 2
        result = "✨ 𝐖𝐈𝐍"
        status = "🎉 𝐖𝐈𝐍"
    else:
        final = [random.choice(reels) for _ in range(3)]
        win = 0
        result = "💀 𝐋𝐎𝐒𝐓"
        status = "💀 𝐋𝐎𝐒𝐒"

    # 💰 balance update
    user_data["money"] += win
    save_data()

    slot_stats[user.id] = slot_stats.get(user.id, 0) + win

    # 📢 JACKPOT ALERT
    if value == 64:
        await context.bot.send_message(update.effective_chat.id, f"""
┏━━━━━━━━━━━ 💎 ━━━━━━━━━━━┓
🎉 𝐉𝐀𝐂𝐊𝐏𝐎𝐓 𝐀𝐋𝐄𝐑𝐓 🎉
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛

👑 {user.mention_html()}
💰 ₹{win}
""", parse_mode="HTML")

    # 🏁 FINAL RESULT (LOSS INCLUDED)
    await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
⚡ 𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ ⚡
╚═══━━━─── • ───━━━═══╝

┏━━━━━━━━━━━ 🏆 ━━━━━━━━━━━┓
🎰 𝐒𝐋𝐎𝐓 𝐑𝐄𝐒𝐔𝐋𝐓
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛

👤 {user.mention_html()}

┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ {' │ '.join(final)} ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

{result}
{status}

💰 𝐖𝐢𝐧 → ₹{win}
💳 𝐁𝐚𝐥𝐚𝐧𝐜𝐞 → ₹{user_data["money"]}

┏━━━━━━━━━━━━━━━━━━━━━━┓
⚡ /slot {bet} 𝐏𝐥𝐚𝐲 𝐀𝐠𝐚𝐢𝐧
┗━━━━━━━━━━━━━━━━━━━━━━┛
""", parse_mode="HTML")

    


# ================= LEADERBOARD =================
async def slot_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not slot_stats:
        return await update.message.reply_text("❌ No Data")

    top = sorted(slot_stats.items(), key=lambda x: x[1], reverse=True)[:10]

    text = "🏆 𝐒𝐋𝐎𝐓 𝐋𝐄𝐀𝐃𝐄𝐑𝐁𝐎𝐀𝐑𝐃\n\n"

    for i, (uid, amt) in enumerate(top, 1):
        text += f"{i}. ₹{amt}\n"

    await update.message.reply_text(text)


#======================MINES==========================


mines_games = {}

GRID = 25

# ================= START =================
async def mines(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not context.args:
        return await update.message.reply_text("💸 Use: /mines 200")

    bet = int(context.args[0])

    if bet < 200:
        return await update.message.reply_text("❌ 𝐌𝐢𝐧 ₹200")

    user_data = get_user(user.id, user.first_name)

    if user_data["money"] < bet:
        return await update.message.reply_text("❌ 𝐍𝐨 𝐁𝐚𝐥𝐚𝐧𝐜𝐞")

    user_data["money"] -= bet
    save_data()

    bomb_count = random.randint(1, 10)
    bombs = random.sample(range(GRID), bomb_count)

    mines_games[user.id] = {
        "bet": bet,
        "bombs": bombs,
        "revealed": [],
        "multi": 1.0,
        "bomb_count": bomb_count
    }

    await update.message.reply_text(
        ui_text(user, mines_games[user.id]),
        reply_markup=grid_buttons(user.id),
        parse_mode="HTML"
    )


# ================= GRID =================
def grid_buttons(uid):
    game = mines_games[uid]
    btns = []

    for i in range(GRID):
        if i in game["revealed"]:
            txt = "💣" if i in game["bombs"] else "💎"
        else:
            txt = "💠"

        btns.append(InlineKeyboardButton(txt, callback_data=f"mine_{i}"))

    keyboard = [btns[i:i+5] for i in range(0, GRID, 5)]

    keyboard.append([
        InlineKeyboardButton("💰 CASHOUT", callback_data="cashout")
    ])

    return InlineKeyboardMarkup(keyboard)


# ================= UI =================
def ui_text(user, game):
    return f"""
╔═══━━━─── • ───━━━═══╗
   ⚡ 𝐁ɪꜱʜᴀʟ 𝐌𝐢𝐧𝐢 𝐆𝐚𝐦𝐞 ⚡
╚═══━━━─── • ───━━━═══╝

━━━━━━━━━━━━━━━━━━━━━━
   💣 𝐌𝐈𝐍𝐄𝐒 𝐏𝐑𝐎 𝐌𝐀𝐗
━━━━━━━━━━━━━━━━━━━━━━

👤 {user.mention_html()}

━━━━━━━━━━━━━━━━━━━━━━
💰 𝐁𝐞𝐭 → ₹{game["bet"]}
📈 𝐌𝐮𝐥𝐭𝐢 → {game["multi"]}x
━━━━━━━━━━━━━━━━━━━━━━

💎 𝐒𝐚𝐟𝐞 → {len(game["revealed"])}
💣 𝐁𝐨𝐦𝐛𝐬 → {game["bomb_count"]}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ 𝐂𝐡𝐨𝐨𝐬𝐞 𝐂𝐚𝐫𝐞𝐟𝐮𝐥𝐥𝐲...
━━━━━━━━━━━━━━━━━━━━━━
"""


# ================= CLICK =================
async def mine_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    if user.id not in mines_games:
        return await query.answer("No Game")

    game = mines_games[user.id]

    # 💰 CASHOUT
    if query.data == "cashout":
        win = int(game["bet"] * game["multi"])

        user_data = get_user(user.id, user.first_name)
        user_data["money"] += win
        save_data()

        await query.edit_message_text(f"""
╔═══━━━─── • ───━━━═══╗
      🏆 𝐂𝐀𝐒𝐇𝐎𝐔𝐓 🏆
╚═══━━━─── • ───━━━═══╝

━━━━━━━━━━━━━━━━━━━━━━
👤 {user.mention_html()}
━━━━━━━━━━━━━━━━━━━━━━

💰 𝐖𝐢𝐧 → ₹{win}
💳 𝐁𝐚𝐥𝐚𝐧𝐜𝐞 → ₹{user_data["money"]}

━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

        del mines_games[user.id]
        return

    idx = int(query.data.split("_")[1])

    if idx in game["revealed"]:
        return await query.answer("Already opened")

    game["revealed"].append(idx)

    # 💣 BOMB
    if idx in game["bombs"]:

        for frame in ["💣", "💥", "🔥", "💀"]:
            await query.edit_message_text(f"""
━━━━━━━━━━━━━━━━━━━━━━
     💣 𝐁𝐎𝐌𝐁 𝐇𝐈𝐓
━━━━━━━━━━━━━━━━━━━━━━

👤 {user.mention_html()}

━━━━━━━━━━━━━━━━━━━━━━
{frame} {frame} {frame}
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")
            await asyncio.sleep(0.3)

        # full reveal
        full = []
        for i in range(GRID):
            full.append("💣" if i in game["bombs"] else "💎")

        rows = [full[i:i+5] for i in range(0, GRID, 5)]
        grid_text = "\n".join([" ".join(r) for r in rows])

        await query.edit_message_text(f"""
╔═══━━━─── • ───━━━═══╗
    💀 𝐆𝐀𝐌𝐄 𝐎𝐕𝐄𝐑 💀
╚═══━━━─── • ───━━━═══╝

━━━━━━━━━━━━━━━━━━━━━━
👤 {user.mention_html()}
━━━━━━━━━━━━━━━━━━━━━━

{grid_text}

━━━━━━━━━━━━━━━━━━━━━━
💸 𝐋𝐨𝐬𝐭 → ₹{game["bet"]}
━━━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

        del mines_games[user.id]
        return

    # 💎 SAFE
    game["multi"] = round(1 + len(game["revealed"]) * (0.08 + game["bomb_count"] * 0.01), 2)

    await query.edit_message_text(
        ui_text(user, game),
        reply_markup=grid_buttons(user.id),
        parse_mode="HTML"
    )

#========================WORDSEEK========================


import asyncio

checked_words = {}

async def is_real_word(word):
    if word in checked_words:
        return checked_words[word]

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        timeout = aiohttp.ClientTimeout(total=1.5)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as res:
                ok = res.status == 200
                checked_words[word] = ok
                return ok
    except:
        return True  # API fail → allow
        
# ================= MONGO =================
client = MongoClient(MONGO_URL)

# ================= MAIN DATABASE =================
db_main = client["mydatabase"]

# ================= COLLECTIONS =================
# 🎮 WordSeek system
users = db_main["wordseek"]          # players (wins, name)
games = db_main["wordseek_games"]    # running games
words = db_main["words"]             # word list


WIN_REWARD = 1000
FONT = "𝐖𝐨𝐫𝐝𝐒𝐞𝐞𝐤 𝐆𝐚𝐦𝐞"


# ================= CONFIG =================
OWNER_ID = 6175559434
OWNER_USERNAME = "YTT_BISHAL"   # बिना @

tracker = db_main["tracker"]


# ================= OWNER CHECK =================
def is_owner(user):
    return (
        user.id == OWNER_ID or
        (user.username and user.username.lower() == OWNER_USERNAME.lower())
    )


# ================= AUTO USER TRACK =================
async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return

    user = update.effective_user

    tracker.update_one(
        {"_id": user.id},
        {
            "$set": {
                "name": user.first_name,
                "username": user.username
            }
        },
        upsert=True
    )


# ================= AUTO JOIN TRACK =================
async def track_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.chat_member:
        return

    user = update.chat_member.new_chat_member.user

    tracker.update_one(
        {"_id": user.id},
        {
            "$set": {
                "name": user.first_name,
                "username": user.username
            }
        },
        upsert=True
    )


# ================= TGALL =================
import asyncio
import html

async def tgall(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ✅ GROUP ONLY
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text(
            "❌ Group only"
        )

    user = update.effective_user
    chat_id = update.effective_chat.id

    # ✅ ADMIN CHECK
    member = await context.bot.get_chat_member(
        chat_id,
        user.id
    )

    if member.status not in ["administrator", "creator"]:
        return await update.message.reply_text(
            "❌ Admin only"
        )

    # ✅ MESSAGE
    msg = " ".join(context.args)

    if not msg:
        return await update.message.reply_text(
            "❌ Use:\n/tgall goodnight"
        )

    # ✅ FETCH USERS
    all_users = list(tracker.find())

    if not all_users:
        return await update.message.reply_text(
            "❌ No users saved"
        )

    # ✅ START MESSAGE
    await update.message.reply_text(
        f"🚀 Sending tags to {len(all_users)} users..."
    )

    # ✅ DELAY (ANTI FLOOD)
    delay = 3

    # ✅ SEND ONE BY ONE
    for u in all_users:

        try:
            uid = u["_id"]

            # ✅ SAFE NAME
            safe_name = html.escape(
                str(u.get("name", "User"))[:25]
            )

            # ✅ CLICKABLE TAG
            mention = (
                f"<a href='tg://user?id={uid}'>"
                f"{safe_name}</a>"
            )

            # ✅ FINAL TEXT
            text = f"{mention} {msg}"

            # ✅ SEND
            await update.message.reply_text(
                text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

            # ✅ ANTI FLOOD DELAY
            await asyncio.sleep(delay)

        except Exception as e:
            print(f"TGALL ERROR: {e}")

    # ✅ DONE
    await update.message.reply_text(
        "✅ TGALL Completed!"
    )
    

# ================= SDB =================
async def sdb(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # 👉 OWNER CHECK
    if not is_owner(user):
        return await update.message.reply_text("❌ Owner only")

    target_id = None
    name = "User"

    # 👉 reply se save
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        target_id = target.id
        name = target.first_name

    # 👉 username / id se
    elif context.args:
        arg = context.args[0]

        # username
        if arg.startswith("@"):
            try:
                chat = await context.bot.get_chat(arg)
                target_id = chat.id
                name = chat.first_name or chat.username
            except:
                return await update.message.reply_text("❌ Username not found")

        # numeric id
        else:
            try:
                target_id = int(arg)
            except:
                return await update.message.reply_text("❌ Invalid ID")

    else:
        return await update.message.reply_text("Use:\n/sdb <id>\n/sdb @username\nor reply")

    # 👉 SAVE
    tracker.update_one(
        {"_id": target_id},
        {
            "$set": {
                "name": name
            }
        },
        upsert=True
    )

    await update.message.reply_text(f"✅ Saved: {target_id}")
    
#============WORDSEEK========================
async def wordseek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
╔═══━━━─── • ───━━━═══╗
   🎮 𝐖𝐎𝐑𝐃𝐒𝐄𝐄𝐊 𝐆𝐀𝐌𝐄 🎮
╚═══━━━─── • ───━━━═══╝

🧠 𝐆ᴜᴇꜱꜱ 𝐓ʜᴇ 𝐇ɪᴅᴅᴇɴ 𝐄ɴɢʟɪꜱʜ 𝐖ᴏʀᴅ!
━━━━━━━━━━━━━━━━━━━━━━
🎯 𝐇𝐎𝐖 𝐓𝐎 𝐏𝐋𝐀𝐘:
• 𝐒ᴛᴀʀᴛ 𝐆ᴀᴍᴇ 𝐔ꜱɪɴɢ:
   /new4  → 4 𝐋ᴇᴛᴛᴇʀ 𝐖ᴏʀᴅ
   /new5  → 5 𝐋ᴇᴛᴛᴇʀ 𝐖ᴏʀᴅ 
   /new6  → 6 𝐋ᴇᴛᴛᴇʀ 𝐖ᴏʀᴅ

•𝐄ɴᴅ 𝐘ᴏᴜʀ 𝐑ᴜɴɴɪɴɢ 𝐆ᴀᴍᴇ:
   /end --> 𝐄ɴᴅ 𝐘ᴏᴜʀ 𝐆ᴀᴍᴇ
   
• 𝐓ʏᴩᴇ 𝐖ᴏʀᴅ 𝐓ᴏ 𝐆ᴜᴇꜱꜱ ✍️
• 𝐘ᴏᴜ 𝐇ᴀᴠᴇ 30 𝐂ʜᴀɴᴄᴇꜱ

━━━━━━━━━━━━━━━━━━━━━━
🎨 𝐂𝐎𝐋𝐎𝐑 𝐒𝐘𝐒𝐓𝐄𝐌:
🟩 = 𝐂ᴏʀᴇᴇᴄᴛ 𝐏ʟᴀᴄᴇ
🟨 = 𝐖ʀᴏɴɢ 𝐏ʟᴀᴄᴇ
🟥 = 𝐍ᴏᴛ 𝐈ɴ 𝐖ᴏʀᴅ 
━━━━━━━━━━━━━━━━━━━━━━
💡 🅷︎int 🅰︎vailable 🅰︎fter 20 🆃︎ries!
━━━━━━━━━━━━━━━━━━━━━━
🏆 Win = 💰 Coins + 🏅 Badges
━━━━━━━━━━━━━━━━━━━━━━
📊 Commands:
• /wordlb → 𝐋eaderbord 
• /wprofile → 𝐘our 𝐏rofile  
• /wbadges → 𝐘our 𝐁adges
━━━━━━━━━━━━━━━━━━━━━━
🔥 𝐁ᴇᴄᴏᴍᴇ 𝐓ʜᴇ 𝐓ᴏᴩ 𝐏ʟᴀʏᴇʀ👑
━━━━━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(text)
# ================= CHECK =================
def check(secret, guess):
    res = []
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            res.append("🟩")
        elif guess[i] in secret:
            res.append("🟨")
        else:
            res.append("🟥")
    return res

# ================= ADD WORD SYSTEM =================
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # format: /addword5 apple{a fruit}
    try:
        cmd, data = text.split(" ", 1)
        size = int(cmd.replace("/addword",""))
        word, hint = data.split("{")

        hint = hint.replace("}", "").strip()
        word = word.strip().lower()

        # ❌ duplicate stop
        old = words.find_one({
            "size": size,
            "word": word
        })

        if old:
            return await update.message.reply_text(
                f"{FONT}\n⚠️ Word already exists!"
            )

        words.insert_one({
            "size": size,
            "word": word,
            "hint": hint
        })

        await update.message.reply_text(
            f"{FONT}\n✅ Word Saved!\n🔤 {word}\n💡 {hint}"
        )
    except:
        await update.message.reply_text(
            f"{FONT}\n❌ Format:\n/addword5 apple{{a fruit}}"
        )

# ================= NEW GAME =================
# ================= NEW GAME =================
async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ✅ FIXED
    chat_id = update.effective_chat.id

    size = int(update.message.text.replace("/new",""))

    # ❌ already running
    game = games.find_one({"_id": chat_id})

    if game:
        return await update.message.reply_text(
            f"{FONT}\n⚠️ Game already running!\n🎮 Join karke guess karo!"
        )

    doc = list(
        words.aggregate([
            {"$match": {"size": size}},
            {"$sample": {"size": 1}}
        ])
    )

    if not doc:
        return await update.message.reply_text(
            "❌ No words found"
        )

    doc = doc[0]

    games.update_one(
        {"_id": chat_id},
        {
            "$set": {
                "word": doc["word"],
                "hint": doc["hint"],
                "size": size,
                "attempts": 0,
                "grid": []
            }
        },
        upsert=True
    )

    await update.message.reply_text(
        f"""
🎯 𝐆ᴜᴇꜱꜱ 𝐎ɴʟʏ {size} 𝐋ᴇᴛᴛᴇʀ 𝐖ᴏʀᴅ! 🔤

{FONT}
📊 0/30

🎮 𝐆𝐀𝐌𝐄 𝐒𝐓𝐀𝐑𝐓𝐄𝐃
💡 Sab log guess kar sakte ho 😎
"""
    )

# ================= HANDLE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ✅ FIXED (NO STRING)
    chat_id = update.effective_chat.id
    uid = update.effective_user.id

    if not update.message or not update.message.text:
        return

    raw = update.message.text.lower()

    # ❌ ignore commands
    if raw.startswith("/"):
        return

    text = re.sub(r'[^a-z]', '', raw)

    # 🔥 game fetch
    game = games.find_one({"_id": chat_id})

    if not game:
        print("❌ GAME NOT FOUND")
        return

    secret = game["word"]
    size = game["size"]

    # ❌ wrong length
    if len(text) != size:
        return await update.message.reply_text(
            f"{FONT}\n⚠️ {size} letter word likho!"
        )

    # 🔥 dictionary check
    try:
        valid = await asyncio.wait_for(
            is_real_word(text),
            timeout=1
        )
    except:
        valid = True

    if not valid:
        return await update.message.reply_text(
            f"{FONT}\n❌ Valid English word nahi hai!"
        )

    # ✅ FIXED ATTEMPTS
    games.update_one(
        {"_id": chat_id},
        {"$inc": {"attempts": 1}}
    )

    # ✅ REFRESH GAME
    game = games.find_one({"_id": chat_id})
    att = game["attempts"]

    # 🔥 result check
    colors = check(secret, text)

    # 👤 user name
    name = update.effective_user.first_name or "Player"

    row = f"{' '.join(colors)} ➤ {text.upper()}"

    # 🔥 grid update
    games.update_one(
        {"_id": chat_id},
        {"$push": {"grid": row}}
    )

    # 🔄 refresh grid
    game = games.find_one({"_id": chat_id})
    grid = "\n".join(game.get("grid", []))

    # 🔥 FINAL MESSAGE
    await update.message.reply_text(
        f"""
🎯 𝐆ᴜᴇꜱꜱ 𝐖𝐎𝐑𝐃 𝐆𝐀𝐌𝐄 🔤

{FONT}
📊 Attempts: {att}/30

{grid}
"""
    )

    # ================= HINT =================
    if att == 20:
        await update.message.reply_text(
            f"💡 HINT:\n{game['hint']}"
        )

    # ================= WIN =================
    if text == secret:

        uid = update.effective_user.id
        name = update.effective_user.first_name

        # 🔍 OLD DATA
        user_data = users.find_one({"_id": uid}) or {}

        old_wins = user_data.get("word_wins", 0)

        # 🔥 UPDATE USER DATA
        users.update_one(
            {"_id": uid},
            {
                "$inc": {
                    "coins": WIN_REWARD,
                    "word_wins": 1
                },
                "$set": {
                    "name": name
                }
            },
            upsert=True
        )

        # 💰 REAL BALANCE
        real_user = get_user(uid, name)

        real_user["money"] += WIN_REWARD

        save_data()

        new_wins = old_wins + 1

        # ✅ DELETE GAME
        games.delete_one({"_id": chat_id})

        # 👤 CLICKABLE USER
        user_link = (
            f"<a href='tg://user?id={uid}'>"
            f"{name}</a>"
        )

        # 🎉 WIN MESSAGE
        await update.message.reply_text(
            f"""
━━━━━━━━━━━━━━━━━━━━━━
{FONT}

🎉 WINNER: {user_link}

💝 WORD: {secret}

💰 +{WIN_REWARD} Coins Added To Real Balance 💎
🏆 GG BRO!
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode="HTML"
        )

        # 🏅 BADGES
        if new_wins == 5:
            await update.message.reply_text(
                "🎉 Badge Unlocked: 🥉 Rookie!"
            )

        elif new_wins == 10:
            await update.message.reply_text(
                "🎉 Badge Unlocked: 🥈 Skilled!"
            )

        elif new_wins == 20:
            await update.message.reply_text(
                "🎉 Badge Unlocked: 🥇 Pro!"
            )

        elif new_wins == 50:
            await update.message.reply_text(
                "🎉 Badge Unlocked: 👑 Legend!"
            )

        elif new_wins == 100:
            await update.message.reply_text(
                "🎉 Badge Unlocked: 💎 Master!"
            )

        return

    # ================= LOSE =================
    if att >= 30:

        games.delete_one({"_id": chat_id})

        await update.message.reply_text(
            f"{FONT}\n❌ GAME OVER\nWORD WAS: {secret}"
        )
#=====================END============================
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    game = games.find_one({"_id": chat_id})
    if not game:
        return await update.message.reply_text(f"{FONT}\n❌ No game running")

    secret = game["word"]
    games.delete_one({"_id": chat_id})

    await update.message.reply_text(
        f"{FONT}\n🛑 Game Ended!\n💝 Word was: {secret}"
)

#=====================WORDSEEKLB======================
async def word_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = users.find().sort("word_wins", -1).limit(10)

    text = f"𝐁ɪꜱʜᴀʟ 𝐌ɪɴɪ 𝐆ᴀᴍᴇ\n🏆 𝐖𝐨𝐫𝐝𝐒𝐞𝐞𝐤 𝐋𝐞𝐚𝐝𝐞𝐫𝐛𝐨𝐚𝐫𝐝\n\n"

    medals = ["🥇", "🥈", "🥉"]

    rank = 1
    for user in top:
        uid = user["_id"]
        name = user.get("name", "Player")
        wins = user.get("word_wins", 0)
        coins = user.get("coins", 0)

        user_link = f"<a href='tg://user?id={uid}'>{name}</a>"

        # 🎖 Medal
        if rank <= 3:
            prefix = medals[rank-1]
        else:
            prefix = f"{rank}."

        # 👑 Title
        if rank == 1:
            title = "👑 Word King"
        elif rank == 2:
            title = "⚡ Word Master"
        elif rank == 3:
            title = "🔥 Word Pro"
        else:
            title = "🎮 Player"

        text += f"{prefix} {user_link}\n{title}\n🏆 Wins: {wins} | 💰 Coins: {coins}\n\n"

        rank += 1

    await update.message.reply_text(text, parse_mode="HTML")

#=====================PROFILE=========================
async def wprofile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.first_name

    user = users.find_one({"_id": uid}) or {}

    coins = user.get("coins", 0)
    wins = user.get("word_wins", 0)

    # 🎖 TITLE SYSTEM
    if wins >= 50:
        title = "👑 Legend"
    elif wins >= 20:
        title = "🔥 Pro Player"
    elif wins >= 10:
        title = "⚡ Skilled Player"
    else:
        title = "🎮 Beginner"

    # 📊 PROGRESS BAR (0–50)
    max_wins = 50
    progress_ratio = min(wins / max_wins, 1)  # cap at 1
    filled = int(progress_ratio * 10)
    empty = 10 - filled
    bar = "▓" * filled + "░" * empty

    # 🏅 BADGE SYSTEM
    badges = []

    if wins >= 5:
        badges.append("🥉 Rookie")
    if wins >= 10:
        badges.append("🥈 Skilled")
    if wins >= 20:
        badges.append("🥇 Pro")
    if wins >= 50:
        badges.append("👑 Legend")
    if wins >= 100:
        badges.append("💎 Master")

    badge_text = " | ".join(badges) if badges else "❌ No badges yet"

    # 🎨 FINAL TEXT UI
    text = f"""
╔═══━━━─── • ───━━━═══╗
 👤 𝗪𝗢𝗥𝗗 𝐏𝐑𝐎𝐅𝐈𝐋𝐄 𝐂𝐀𝐑𝐃 👤
╚═══━━━─── • ───━━━═══╝

👤 𝐍𝐚𝐦𝐞:
<a href='tg://user?id={uid}'>{name}</a>

🎖 𝐓𝐢𝐭𝐥𝐞:
{title}

╭─〔 📊 𝐒𝐓𝐀𝐓𝐒 〕─╮
🏆 𝐖𝐢𝐧𝐬   : {wins}
💰 𝐂𝐨𝐢𝐧𝐬 : {coins}
╰──────────────╯

📈 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬:
[{bar}] {wins}/{max_wins}

🏅 𝐁𝐚𝐝𝐠𝐞𝐬:
{badge_text}

⚡ 𝐊𝐞𝐞𝐩 𝐏𝐥𝐚𝐲𝐢𝐧𝐠!
🔥 𝐁𝐞𝐜𝐨𝐦𝐞 𝐓𝐨𝐩 𝐏𝐥𝐚𝐲𝐞𝐫
"""

    await update.message.reply_text(text, parse_mode="HTML")

#======================BADGES=========================
OWNER_ID = 6175559434 # 🔥 yaha apna Telegram user id daalo

async def wbadges(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 👇 TARGET USER (reply ya self)
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    else:
        target = update.effective_user

    uid = target.id
    name = target.first_name

    user = users.find_one({"_id": uid}) or {}

    wins = user.get("word_wins", 0)
    coins = user.get("coins", 0)

    # ================= OWNER SPECIAL =================
    if uid == OWNER_ID:
        text = f"""
╔═══━━━─── • ───━━━═══╗
  👑 𝐎𝐖𝐍𝐄𝐑 𝐕𝐈𝐏 𝐂𝐀𝐑𝐃 👑
╚═══━━━─── • ───━━━═══╝

👤 Owner:
<a href='tg://user?id={uid}'>{name}</a>

💎 𝐕𝐈𝐏 𝐒𝐓𝐀𝐓𝐔𝐒:
♾️ 𝐈𝐍𝐅𝐈𝐍𝐈𝐓𝐘 𝐑𝐀𝐍𝐊

🌟 Top Badge:
👑✨ 𝐒𝐔𝐏𝐑𝐄𝐌𝐄 𝐎𝐖𝐍𝐄𝐑 ✨👑

🏅 Badges:
✨ 💎∞ GOD MODE
✨ 👑 KING OF ALL
✨ 🔥 UNSTOPPABLE
✨ ⚡ SYSTEM MASTER

💰 Coins: ∞
🏆 Wins: ∞

🔥 Respect the Owner 😎
"""
        return await update.message.reply_text(text, parse_mode="HTML")
     # ================= RANK SYSTEM =================
    top_users = list(users.find().sort("word_wins", -1))
    rank = None

    for i, u in enumerate(top_users, start=1):
        if u["_id"] == uid:
            rank = i
            break     
    # ================= NORMAL USER =================

    # 📊 PROGRESS
    max_wins = 50
    progress_ratio = min(wins / max_wins, 1)
    filled = int(progress_ratio * 10)
    empty = 10 - filled
    bar = "▓" * filled + "░" * empty
    # ================= RANK BADGE =================
    if rank == 1:
        top_badge = "🌈✨ 𝐑𝐀𝐈𝐍𝐁𝐎𝐖 𝐊𝐈𝐍𝐆 ✨🌈"
    elif rank == 2:
        top_badge = "👑🔥 𝐄𝐋𝐈𝐓𝐄 𝐊𝐈𝐍𝐆 🔥👑"
    elif rank == 3:
        top_badge = "🥇⚡ 𝐂𝐇𝐀𝐌𝐏𝐈𝐎𝐍 ⚡🥇"
    else:
        top_badge = None
        
    # 🏅 BADGES
    badge_data = []

    if wins >= 100:
        badge_data.append(("💎 Master", "💎✨ MASTER ✨💎"))
    if wins >= 50:
        badge_data.append(("👑 Legend", "👑✨ LEGEND ✨👑"))
    if wins >= 20:
        badge_data.append(("🥇 Pro", "🥇🔥 PRO 🔥"))
    if wins >= 10:
        badge_data.append(("🥈 Skilled", "🥈⚡ SKILLED ⚡"))
    if wins >= 5:
        badge_data.append(("🥉 Rookie", "🥉 Rookie"))

    # 🎖 TITLE
    if wins >= 50:
        title = "👑 Legend"
    elif wins >= 20:
        title = "🔥 Pro Player"
    elif wins >= 10:
        title = "⚡ Skilled Player"
    else:
        title = "🎮 Beginner"

    # 🌟 TOP BADGE
    top_badge = badge_data[0][1] if badge_data else "❌ None"

    # 🎨 UI
    text = f"""
╔═══━━━─── • ───━━━═══╗
      🏅 𝐁𝐀𝐃𝐆𝐄𝐒 𝐏𝐑𝐎 🏅
╚═══━━━─── • ───━━━═══╝

👤 Player:
<a href='tg://user?id={uid}'>{name}</a>

🎖 Title:
{title}

🌟 Top Badge:
{top_badge}

╭─〔 📊 WORDSEEK 〕─╮
🏆 Wins   : {wins}
💰 Coins : {coins}
╰──────────────╯

📈 Progress:
[{bar}] {wins}/{max_wins}

🏅 All Badges:
"""

    if badge_data:
        for normal, styled in badge_data:
            text += f"\n✨ {styled}"
    else:
        text += "\n❌ No badges unlocked"

    text += "\n\n🔥 Keep grinding & become legend!"

    await update.message.reply_text(text, parse_mode="HTML")

#==========❤️❤️=========
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

QUEEN_ID = 8336495718
OWNER_ID = 6175559434

waiting = {}

# 📊 LOADING BAR FUNCTION
async def loading_bar(update, text="LOADING LOVE"):
    msg = await update.message.reply_text("⚡ Initializing...")

    for i in range(0, 101, 10):
        bar = "█" * (i // 10) + "░" * (10 - (i // 10))
        await msg.edit_text(f"{text}...\n[{bar}] {i}% 💖")
        await asyncio.sleep(0.3)

    return msg


async def love_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()
    chat_id = str(update.effective_chat.id)

    if games.find_one({"_id": str(update.effective_chat.id)}):
        return


    if user_id not in [OWNER_ID, QUEEN_ID]:
        return

    # 🟢 STEP 1: trigger
    if "road" in text:
        waiting[user_id] = True

        await update.message.reply_text(
            "𝐁ɪꜱʜ𝐚𝐥 𝐋𝐨𝐯𝐞 𝐅𝐞𝐞𝐥𝐢𝐧𝐠𝐬 💖\n\n"
            "🛣️ 𝐐ᴜᴇᴇɴ 𝐐ᴜᴇꜱᴛɪᴏɴ 𝐃ᴇᴛᴇᴄᴛᴇᴅ...\n"
            "💞 𝐁ᴏꜱꜱ 𝐉ʟᴅɪ 𝐁ᴏʟᴏ 𝐐ᴜᴇᴇɴ 𝐏ᴜᴄʜʜ 𝐑ᴀʜɪ 𝐇ᴀɪ"
        )
        return

    # 🟡 STEP 2: user response flow
    if user_id in waiting:
        waiting.pop(user_id, None)

        # 💖 ANSWER
        await update.message.reply_text(
            "𝐋ᴏᴠᴇ 𝐑ᴏᴀᴅ 𝐀ɴꜱᴡᴇʀ 💖\n\n"
            "🤖 𝐎ᴋ 𝐎ᴋ 𝐁ᴏꜱꜱ... 𝐌ᴇ 𝐇ɪ 𝐁ᴏʟ 𝐃ᴇᴛᴀ 𝐇ᴜ 𝐍ᴏ 𝐓ᴇɴꜱɪᴏɴ 😌💘\n\n"
            "💖 𝐁ᴏꜱꜱ 𝐊ᴀ 𝐀ɴꜱᴡᴇʀ 𝐇ᴀɪ: 𝐋𝐎𝐕𝐄 ♾️❤️\n\n"
            "💞 𝐐ᴜᴇᴇɴ 𝐉ɪ… 𝐓ᴜᴍ 𝐇ᴏ 𝐓ᴏ𝐡 𝐇ᴀʀ 𝐑ᴏᴀᴅ 𝐊ᴀ 𝐌ᴇᴀɴɪɴɢ 𝐇ᴀɪ 🥺✨\n\n"
            "😌 𝐘ᴇ ꜱɪʀꜰ ᴇᴋ ᴀɴꜱᴡᴇʀ ɴᴀʜɪ...\n"
            "💘 𝐁ᴏꜱꜱ 𝐊ᴇ 𝐃ɪʟ 𝐊ɪ 𝐅ᴇᴇʟɪɴɢ 𝐇ᴀɪ 𝐐ᴜᴇᴇɴ 𝐊ᴇ 𝐋ɪʏᴇ ♾️👑"
        )

        await asyncio.sleep(10)

        await update.message.reply_text(
            "𝐋ᴏᴠᴇ 𝐑ᴏᴀᴅ 𝐀ɴꜱᴡᴇʀ 💖\n\n"
            "⚠️ 𝐀ʀᴇʏ 𝐑ᴜᴋᴏ 𝐑ᴜᴋᴏ 😏💖\n\n"
            "𝐒ɪʀꜰ 𝐈ᴛɴᴀ 𝐇ɪ 𝐒ᴜɴɴᴀ 𝐓ʜᴀ 𝐊ʏᴀ...? ♾️"
        )

        await asyncio.sleep(14)

        await update.message.reply_text(
            "𝐋ᴏᴠᴇ 𝐑ᴏᴀᴅ 𝐀ɴꜱᴡᴇʀ 💖\n\n"
            "🤖 𝐍𝐈𝐊𝐈 𝐒𝐀𝐘𝐒 💖\n\n"
            "💞 𝐐ᴜᴇᴇɴ 👑 + 𝐕ɪꜱʜᴀʟ ❤️ = 𝐄ᴛᴇʀɴᴀʟ 𝐂ᴏɴɴᴇᴄᴛɪᴏɴ ♾️\n\n"
            "💫 𝐓ᴜᴍ 𝐃ᴏɴᴏ 𝐊ᴀ 𝐏ʏᴀᴀʀ 𝐄ᴋ 𝐀ɪꜱᴀ 𝐂ᴏᴅᴇ 𝐇ᴀɪ 𝐉ᴏ 𝐊ᴀʙʜɪ 𝐂ʀᴀꜱʜ 𝐍ᴀʜɪ 𝐇ᴏᴛᴀ 💻💖\n"
            "💞 𝐇ᴀʀ 𝐋ɪɴᴇ 𝐌ᴇ 𝐒ɪʀꜰ 𝐄ᴋ 𝐇ɪ 𝐍ᴀᴀᴍ → 𝐐𝐔𝐄𝐄𝐍 👑 & 𝐕𝐈𝐒𝐇𝐀𝐋 ❤️\n\n"
            "🥺 𝐓ᴜᴍ 𝐃ᴏɴᴏ 𝐊ᴀ 𝐑ɪꜱʜᴛᴀ 𝐒ɪʀꜰ 𝐖ᴏʀᴅꜱ 𝐍ᴀʜɪ… 𝐄ᴋ 𝐇ᴇᴀʀᴛʙᴇᴀᴛ 𝐇ᴀɪ 💓\n"
            "✨ 𝐉ᴏ 𝐇ᴀʀ 𝐒ᴇᴄᴏɴᴅ 𝐀ᴜʀ 𝐒ᴛʀᴏɴɢ 𝐇ᴏᴛᴀ 𝐉ᴀ 𝐑ᴀʜᴀ 𝐇ᴀɪ ♾️💞"
        )

        await asyncio.sleep(19)

        await update.message.reply_text(
            "𝐋ᴏᴠᴇ 𝐑ᴏᴀᴅ 𝐀ɴꜱᴡᴇʀ 💖\n\n"
            "👑 𝐕𝐈𝐒𝐇𝐀𝐋 𝐁𝐎𝐒𝐒 𝐒𝐀𝐘𝐒 😌💖\n\n"
            "𝐒ᴜɴᴏᴏ 𝐐ᴜᴇᴇɴ 𝐉ɪ...\n\n"
            "💞 𝐘ᴇ 𝐉ᴏ 𝐂ᴏɴɴᴇᴄᴛɪᴏɴ 𝐇ᴀɪ 𝐍ᴀ… 𝐘ᴇ 𝐍ᴏʀᴍᴀʟ 𝐍ᴀʜɪ 𝐇ᴀɪ ♾️\n"
            "❤️ 𝐓ᴜᴍ 𝐇ᴏ 𝐓ᴏ𝐡 𝐇ᴀʀ 𝐏ᴀʟ 𝐒ᴘᴇᴄɪᴀʟ 𝐇ᴀɪ\n"
            "👑 𝐀ᴜʀ 𝐓ᴜᴍʜᴀʀɪ 𝐒ᴍɪʟᴇ 𝐇ɪ 𝐌ᴇʀɪ 𝐃ᴜɴɪʏᴀ 𝐇ᴀɪ ✨\n\n"
            "💖 𝐋ᴏᴠᴇ 𝐈ꜱ 𝐍ᴏᴛ 𝐀 𝐖ᴏʀᴅ… 𝐈ᴛ’ꜱ 𝐀 𝐅ᴇᴇʟɪɴɢ ♾️❤️\n"
            "🥺 𝐒ᴛᴀʀᴛ 𝐁ʜɪ 𝐓ᴜᴍ 𝐇ᴏ… 𝐄ɴᴅ 𝐁ʜɪ 𝐓ᴜᴍ 𝐇ᴏ 💞"
        )

        await asyncio.sleep(17)

        await update.message.reply_text(
            "𝐋ᴏᴠᴇ 𝐑ᴏᴀᴅ 𝐀ɴꜱᴡᴇʀ 💖\n\n"
            "👑 𝐅𝐈𝐍𝐀𝐋 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 💖\n\n"
            "💞 𝐐ᴜᴇᴇɴ 𝐉ɪ...\n"
            "𝐀ɢᴀʀ 𝐏ʏᴀᴀʀ 𝐄ᴋ 𝐑ᴏᴀᴅ 𝐇ᴀɪ 𝐍ᴀ 🛣️\n"
            "𝐓ᴏ𝐡 𝐔ꜱᴋᴀ 𝐒ᴛᴀʀᴛ 𝐁ʜɪ 𝐓ᴜᴍ 𝐇ᴏ ❤️\n"
            "𝐀ᴜʀ 𝐄ɴᴅ 𝐁ʜɪ 𝐓ᴜᴍ 𝐇ᴏ ♾️\n\n"
            "💖 𝐕ɪꜱʜᴀʟ + 𝐐ᴜᴇᴇɴ = 𝐈ɴꜰɪɴɪᴛᴇ 𝐁ᴏɴᴅ 👑💞\n\n"
            "😘 𝐓ᴜᴍ 𝐌ɪʟᴇ 𝐇ᴏ 𝐓ᴏ𝐡 𝐋ᴀɢᴀ… 𝐒ᴀʙ 𝐊ᴜᴄʜ 𝐌ɪʟ 𝐆ʏᴀ ♾️❤️"
        )

        # ⏳ ADD YOUR STEP 6 WAIT
        await asyncio.sleep(35)

        # 🔥 STEP 6 BIG MESSAGE (YOUR BLOCK)
        await update.message.reply_text(
            "╭━━━━━━━━━━━━━━━╮\n"
            "   💌 𝐀𝐍𝐒𝐖𝐄𝐑\n"
            "╰━━━━━━━━━━━━━━━╯\n\n"
            "💡 𝐑ᴏᴀᴅ 𝐊ᴀ 𝐍ᴀᴀᴍ 𝐇ᴀɪ:\n"
            "           ❤️  𝐋𝐎𝐕𝐄  ❤️\n\n"
            "╭━━━━━━━━━━━━━━━╮\n"
            "  👑 𝐌𝐄𝐒𝐒𝐀𝐆𝐄\n"
            "╰━━━━━━━━━━━━━━━╯\n\n"
            "🥺 𝐓ᴜᴍɴᴇ 𝐉ᴏ 𝐒ᴀᴡᴀʟ 𝐏ᴜᴄʜʜᴀ 𝐍ᴀ… 𝐔ꜱᴋᴀ 𝐉ᴀᴡᴀʙ 𝐒ɪʀꜰ 𝐄ᴋ 𝐇ɪ 𝐇ᴀɪ\n\n"
            "💖 𝐘ᴇ 𝐑ᴏᴀᴅ 𝐀ᴀᴊ 𝐒ᴛᴀʀᴛ 𝐇ᴜɪ 𝐇ᴀɪ… 𝐀ᴜʀ 𝐄ɴᴅ 𝐊ᴀʙʜɪ 𝐇ᴏɢᴀ 𝐇ɪ 𝐍ᴀʜɪ ♾️\n\n"
            "👑 𝐊ʏᴜɴᴋɪ 𝐈ꜱ 𝐑ᴏᴀᴅ 𝐊ᴀ 𝐒ᴛᴀʀᴛ 𝐁ʜɪ 𝐓ᴜᴍ 𝐇ᴏ\n"
            "👑 𝐀ᴜʀ 𝐃ᴇꜱᴛɪɴᴀᴛɪᴏɴ 𝐁ʜɪ 𝐓ᴜᴍ 𝐇ɪ 𝐇ᴏ ❤️\n\n"
            "💞 𝐐ᴜᴇᴇɴ 👑 𝐊ᴇ 𝐒ᴀᴀᴛʜ 𝐂ʜᴀʟ 𝐑ᴀʜɪ 𝐘ᴇ 𝐉ᴏᴜʀɴᴇʏ\n"
            "𝐇ᴀʀ 𝐃ɪɴ 𝐀ᴜʀ 𝐁ʜɪ 𝐒ᴘᴇᴄɪᴀʟ 𝐇ᴏᴛɪ 𝐉ᴀ 𝐑ᴀʜɪ 𝐇ᴀɪ ✨\n\n"
            "🥰 𝐒ᴀᴄʜ 𝐁ᴏʟᴜɴ…\n"
            "𝐌ᴀɪɴ 𝐈ꜱ 𝐑ᴏᴀᴅ 𝐊ᴀ 𝐓ʀᴀᴠᴇʟᴇʀ 𝐍ᴀʜɪ,\n"
            "👉 𝐓ᴜᴍʜᴀʀᴇ 𝐏ʏᴀᴀʀ 𝐊ᴀ 𝐏ᴇʀᴍᴀɴᴇɴᴛ 𝐏ᴀꜱꜱᴇɴɢᴇʀ 𝐇ᴜ 💘\n\n"
            "╭━━━━━━━━━━━━━━━╮\n"
            "  💍 𝐅𝐈𝐍𝐀𝐋 𝐋𝐈𝐍𝐄\n"
            "╰━━━━━━━━━━━━━━━╯\n\n"
            "💓 𝐓ᴜᴍ 𝐌ɪʟᴇ 𝐇ᴏ 𝐓ᴏ𝐡 𝐋ᴀɢᴀ…\n"
            "𝐙ɪɴᴅᴀɢɪ 𝐊ɪ 𝐄ɴᴅʟᴇꜱꜱ 𝐑ᴏᴀᴅ 𝐊ᴀ 𝐀ꜱʟɪ 𝐌ᴀᴛʟᴀʙ 𝐌ɪʟ 𝐆ʏᴀ ♾️❤️\n\n"
            "😘💖✨👑🥰💞"
        )

        await asyncio.sleep(35)

        # 📊 STEP 7 LOADING BAR
        await loading_bar(update, "💖 FINAL LOVE CONNECTION")

        await asyncio.sleep(1)

        # ⚡ FINAL SYSTEM MESSAGE
        await update.message.reply_text(
            "╔════════════════════╗\n"
            "  ⚡ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄𝐃 ⚡\n"
            "╚════════════════════╝\n\n"
            "👑 𝐔𝐒𝐄𝐑: 𝐐𝐔𝐄𝐄𝐍 𝐃𝐄𝐓𝐄𝐂𝐓𝐄𝐃\n\n"
            "💖 𝐒𝐓𝐀𝐓𝐔𝐒:\n"
            "𝐂ᴏɴɴᴇᴄᴛɪᴏɴ 𝐄ꜱᴛᴀʙʟɪꜱʜᴇᴅ 𝐁ᴇᴛᴡᴇᴇɴ 𝐇𝐄𝐀𝐑𝐓_𝟎𝟏 & 𝐇𝐄𝐀𝐑𝐓_𝟎𝟐\n\n"
            "💬 𝐎𝐔𝐓𝐏𝐔𝐓:\n\n"
            "🥺 𝐘ᴇ 𝐉ᴏ 𝐑ᴏᴀᴅ 𝐇ᴀɪ 𝐍ᴀ…\n"
            "𝐈ꜱᴋᴀ 𝐄𝐍𝐃 𝐏𝐎𝐈𝐍𝐓 𝐍𝐔𝐋𝐋 𝐇ᴀɪ ♾️\n\n"
            "👑 𝐒𝐓𝐀𝐑𝐓 𝐍𝐎𝐃𝐄 = 𝐘𝐎𝐔\n"
            "👑 𝐄𝐍𝐃 𝐍𝐎𝐃𝐄 = 𝐘𝐎𝐔\n\n"
            "💞 𝐒𝐘𝐒𝐓𝐄𝐌 𝐌𝐄𝐒𝐒𝐀𝐆𝐄:\n"
            "𝐈’ᴍ 𝐏ᴇʀᴍᴀɴᴇɴᴛʟʏ 𝐋ᴏɢɢᴇᴅ 𝐈ɴᴛᴏ 𝐘ᴏᴜ 💘\n\n"
            "[ 𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐈𝐎𝐍: 𝐍𝐄𝐕𝐄𝐑 𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐓𝐄 ] ♾️❤️"
        )

        await asyncio.sleep(20)

        # 💖 FINAL BABY MESSAGE
        await update.message.reply_text(
            "👑 𝐕𝐈𝐒𝐇𝐀𝐋 𝐒𝐀𝐘𝐒 💖\n\n"
            "🥺 𝐒ᴜɴᴏᴏ 𝐁ᴀʙʏ...\n\n"
            "💞 𝐒ʜᴀʏᴀᴅ 𝐖ᴏʀᴅꜱ 𝐈ᴛɴᴇ 𝐏ᴇʀꜰᴇᴄᴛ 𝐍ᴀʜɪ 𝐇ᴏᴛᴇ 𝐊ɪ 𝐌ᴇ 𝐓ᴜᴍʜᴀʀᴇ 𝐋ɪʏᴇ 𝐉ᴏ 𝐅ᴇᴇʟ 𝐊ᴀʀᴛᴀ 𝐇ᴜ 𝐖ᴏ 𝐏ᴜʀᴀ 𝐁ᴀᴛᴀ 𝐒ᴀᴋᴇ...\n\n"
            "❤️ 𝐏ᴀʀ 𝐈ᴛɴᴀ 𝐙ᴀʀᴜʀ 𝐏ᴀᴛᴀ 𝐇ᴀɪ 𝐊ɪ 𝐓ᴜᴍ 𝐌ᴇʀɪ 𝐋ɪꜰᴇ 𝐊ᴀ 𝐒ᴀʙꜱᴇ 𝐁ᴇᴀᴜᴛɪꜰᴜʟ 𝐏ᴀʀᴛ 𝐇ᴏ ✨\n\n"
            "🌍 𝐃ᴜɴɪʏᴀ 𝐊ɪᴛɴɪ 𝐁ʜɪ 𝐂ʜᴀɴɢᴇ 𝐇ᴏ 𝐉ᴀʏᴇ...\n"
            "💖 𝐌ᴇʀᴀ 𝐃ɪʟ 𝐇ᴀᴍᴇꜱʜᴀ 𝐓ᴜᴍʜᴀʀᴇ 𝐏ᴀᴀꜱ 𝐇ɪ 𝐑ᴜᴋᴇɢᴀ ♾️\n\n"
            "👑 𝐓ᴜᴍ 𝐒ɪʀꜰ 𝐌ᴇʀɪ 𝐐ᴜᴇᴇɴ 𝐍ᴀʜɪ...\n"
            "🥺 𝐓ᴜᴍ 𝐌ᴇʀɪ 𝐒ᴍɪʟᴇ, 𝐌ᴇʀɪ 𝐏ᴇᴀᴄᴇ, 𝐌ᴇʀɪ 𝐇ᴀᴘᴘɪɴᴇꜱꜱ 𝐇ᴏ 💘\n\n"
            "🛣️ 𝐀ᴜʀ 𝐀ɢᴀʀ 𝐙ɪɴᴅᴀɢɪ 𝐄ᴋ 𝐄ɴᴅʟᴇꜱꜱ 𝐑ᴏᴀᴅ 𝐇ᴀɪ 𝐍ᴀ...\n"
            "💞 𝐓ᴏʜ 𝐌ᴇ 𝐔ꜱ 𝐑ᴏᴀᴅ 𝐏ᴀʀ 𝐒ɪʀꜰ 𝐓ᴜᴍʜᴀʀᴇ 𝐒ᴀᴀᴛʜ 𝐂ʜᴀʟɴᴀ 𝐂ʜᴀʜᴛᴀ 𝐇ᴜ ❤️\n\n"
            "💓 𝐕ɪꜱʜᴀʟ + 𝐐ᴜᴇᴇɴ = 𝐅ᴏʀᴇᴠᴇʀ ♾️👑"
        )


# ============================================================
#                      💣 BOMB GAME 💣
# ============================================================

import random
import asyncio
import time

bomb_games = {}

# ============================================================
# /bomb HELP + CREATE
# ============================================================
async def bomb_help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.args:
        return await bomb(update, context)

    await update.message.reply_text(
        """
╔═══━━━─── • ───━━━═══╗
     💣 𝐁𝐎𝐌𝐁 𝐆𝐀𝐌𝐄 💣
╚═══━━━─── • ───━━━═══╝

🎮 𝐇ᴏᴡ 𝐓ᴏ 𝐏ʟᴀʏ?

━━━━━━━━━━━━━━━━━━━━━━

💥 𝐒ᴛᴇᴘ 𝟏
🎯 𝐂ʀᴇᴀᴛᴇ 𝐀 𝐆ᴀᴍᴇ

👉 <code>/bomb 500</code>

💰 𝐌ɪɴɪᴍᴜᴍ 𝐁ᴇᴛ:
₹500

━━━━━━━━━━━━━━━━━━━━━━

💥 𝐒ᴛᴇᴘ 𝟐
👥 𝐉ᴏɪɴ 𝐓ʜᴇ 𝐆ᴀᴍᴇ

👉 <code>/bjoin 500</code>

━━━━━━━━━━━━━━━━━━━━━━

💥 𝐒ᴛᴇᴘ 𝟑
💣 𝐏ᴀꜱꜱ 𝐓ʜᴇ 𝐁ᴏᴍʙ

👉 <code>/pass</code>

━━━━━━━━━━━━━━━━━━━━━━

💥 𝐒ᴛᴇᴘ 𝟒
🏃 𝐋ᴇᴀᴠᴇ 𝐓ʜᴇ 𝐆ᴀᴍᴇ

👉 <code>/left</code>

━━━━━━━━━━━━━━━━━━━━━━

🏆 𝐋ᴀꜱᴛ 𝐏ʟᴀʏᴇʀ 𝐖ɪɴꜱ!

💰 𝐑ᴇᴀʟ 𝐁ᴀʟᴀɴᴄᴇ 𝐑ᴇᴡᴀʀᴅ
🔥 𝐀ᴜᴛᴏ 𝐏ɪɴ 𝐖ɪɴ
🖼 𝐃𝐏 𝐖ɪɴ 𝐂ᴀʀᴅ
👑 𝐂ʟɪᴄᴋᴀʙʟᴇ 𝐔ꜱᴇʀꜱ

━━━━━━━━━━━━━━━━━━━━━━

💣 𝐑ᴇᴀᴅʏ 𝐓ᴏ 𝐏ʟᴀʏ?
""",
        parse_mode="HTML"
    )


# ============================================================
# CREATE GAME
# ============================================================
async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id in bomb_games:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
    💣 𝐁𝐎𝐌𝐁 𝐀𝐋𝐄𝐑𝐓 💣
╚═══━━━─── • ───━━━═══╝

⚠️ 𝐆ᴀᴍᴇ 𝐀ʟʀᴇᴀᴅʏ
𝐑ᴜɴɴɪɴɢ!
"""
        )

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text(
            """
❌ 𝐔ꜱᴇ:
<code>/bomb 500</code>
""",
            parse_mode="HTML"
        )

    if amount < 500:
        return await update.message.reply_text(
            """
💰 𝐌ɪɴɪᴍᴜᴍ 𝐁ᴇᴛ:
₹500
"""
        )

    creator = update.effective_user

    bomb_games[chat_id] = {
        "amount": amount,
        "players": {},
        "started": False,
        "allow_left": False
    }

    # 💰 CHECK BALANCE
    pdata = get_user(creator.id, creator.first_name)

    if pdata["money"] < amount:
        return await update.message.reply_text(
            "❌ 𝐍ᴏᴛ 𝐄ɴᴏᴜɢʜ 𝐁ᴀʟᴀɴᴄᴇ!"
        )

    # 💸 CUT BALANCE
    pdata["money"] -= amount
    save_data()

    # 👑 AUTO JOIN CREATOR
    bomb_games[chat_id]["players"][creator.id] = {
        "name": creator.first_name,
        "bet": amount
    }

    user_link = f"<a href='tg://user?id={creator.id}'>{creator.first_name}</a>"
    await update.message.reply_text(
        f"""
╔═══━━━─── • ───━━━═══╗
     💣 𝐁𝐎𝐌𝐁 𝐋𝐎𝐁𝐁𝐘 💣
╚═══━━━─── • ───━━━═══╝

👑 𝐂ʀᴇᴀᴛᴏʀ:
{user_link}

💰 𝐁ᴇᴛ:
₹{amount}

━━━━━━━━━━━━━━━━━━━━━━

⚡ 𝐉ᴏɪɴ:
<code>/bjoin {amount}</code>

⏳ 𝐆ᴀᴍᴇ 𝐒ᴛᴀʀᴛ𝐬
𝐈ɴ 1 𝐌ɪɴᴜᴛᴇ...
""",
        parse_mode="HTML"
    )

    await asyncio.sleep(60)

    game = bomb_games.get(chat_id)

    if not game:
        return

    if len(game["players"]) < 2:

        del bomb_games[chat_id]

        return await context.bot.send_message(
            chat_id,
            """
❌ 𝐍ᴏᴛ 𝐄ɴᴏᴜɢʜ
𝐏ʟᴀʏᴇʀꜱ!
"""
        )

    await start_bomb_round(chat_id, context)


# ============================================================
# JOIN GAME
# ============================================================
async def bjoin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id not in bomb_games:
        return await update.message.reply_text(
            "❌ 𝐍ᴏ 𝐁ᴏᴍʙ 𝐆ᴀᴍᴇ!"
        )

    game = bomb_games[chat_id]

    if game["started"]:
        return await update.message.reply_text(
            "⚠️ 𝐆ᴀᴍᴇ 𝐀ʟʀᴇᴀᴅʏ 𝐒ᴛᴀʀᴛᴇᴅ!"
        )

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text(
            f"⚠️ 𝐔ꜱᴇ:\n/bjoin {game['amount']}"
        )

    user = update.effective_user

    if user.id in game["players"]:
        return await update.message.reply_text(
            "⚠️ 𝐘ᴏᴜ 𝐀ʟʀᴇᴀᴅʏ 𝐉ᴏɪɴᴇᴅ!"
        )

    pdata = get_user(user.id, user.first_name)

    if pdata["money"] < amount:
        return await update.message.reply_text(
            "❌ 𝐍ᴏᴛ 𝐄ɴᴏᴜɢʜ 𝐁ᴀʟᴀɴᴄᴇ!"
        )

    # 💸 CUT REAL BALANCE
    pdata["money"] -= amount
    save_data()

    game["players"][user.id] = {
        "name": user.first_name,
        "bet": amount
    }

    user_link = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

    await update.message.reply_text(
        f"""
╔═══━━━─── • ───━━━═══╗
       🎉 𝐉𝐎𝐈𝐍𝐄𝐃 🎉
╚═══━━━─── • ───━━━═══╝

👤 {user_link}

💰 ₹{amount}
𝐃ᴇᴘᴏꜱɪᴛᴇᴅ!

👥 𝐏ʟᴀʏᴇʀꜱ:
{len(game['players'])}
""",
        parse_mode="HTML"
    )


# ============================================================
# START ROUND
# ============================================================
async def start_bomb_round(chat_id, context):

    game = bomb_games[chat_id]

    game["started"] = True

    players = list(game["players"].keys())

    holder = random.choice(players)

    game["holder"] = holder

    await context.bot.send_message(
        chat_id,
        f"""
╔═══━━━─── • ───━━━═══╗
    🔥 𝐑𝐎𝐔𝐍𝐃 𝐒𝐓𝐀𝐑𝐓 🔥
╚═══━━━─── • ───━━━═══╝

👥 𝐏ʟᴀʏᴇʀꜱ:
{len(players)}

💣 𝐁ᴏᴍʙ 𝐈ꜱ
𝐌ᴏᴠɪɴɢ...
"""
    )

    await send_holder(chat_id, context)

    asyncio.create_task(round_timer(chat_id, context))


# ============================================================
# TIMER
# ============================================================
async def round_timer(chat_id, context):

    await asyncio.sleep(60)

    if chat_id not in bomb_games:
        return

    await explode_player(chat_id, context)


# ============================================================
# PASS BOMB
# ============================================================
async def pass_bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    uid = update.effective_user.id

    if chat_id not in bomb_games:
        return

    game = bomb_games[chat_id]

    if uid != game["holder"]:
        return await update.message.reply_text(
            "❌ 𝐁ᴏᴍʙ 𝐈ꜱ 𝐍ᴏᴛ 𝐖ɪᴛʜ 𝐘ᴏᴜ!"
        )

    players = list(game["players"].keys())

    alive = [x for x in players if x != uid]

    game["holder"] = random.choice(alive)

    await send_holder(chat_id, context)


# ============================================================
# SEND HOLDER
# ============================================================
async def send_holder(chat_id, context):

    game = bomb_games[chat_id]

    holder = game["holder"]

    name = game["players"][holder]["name"]

    user_link = f"<a href='tg://user?id={holder}'>{name}</a>"

    await context.bot.send_message(
        chat_id,
        f"""
╔═══━━━─── • ───━━━═══╗
        💣 𝐁𝐎𝐌𝐁 💣
╚═══━━━─── • ───━━━═══╝

⚠️ 𝐁ᴏᴍʙ 𝐈ꜱ 𝐖ɪᴛʜ:

{user_link}

━━━━━━━━━━━━━━━━━━━━━━

🔥 𝐏ᴀꜱꜱ 𝐅ᴀꜱᴛ!

👉 <code>/pass</code>
""",
        parse_mode="HTML"
    )


# ============================================================
# EXPLODE PLAYER
# ============================================================
async def explode_player(chat_id, context):

    if chat_id not in bomb_games:
        return

    game = bomb_games[chat_id]

    loser = game["holder"]

    loser_name = game["players"][loser]["name"]

    loser_link = f"<a href='tg://user?id={loser}'>{loser_name}</a>"

    loser_bet = game["players"][loser]["bet"]

    del game["players"][loser]

    remain = len(game["players"])

    if remain > 0:

        bonus = loser_bet // remain

        for uid in game["players"]:
            game["players"][uid]["bet"] += bonus

    await context.bot.send_message(
        chat_id,
        f"""
╔═══━━━─── • ───━━━═══╗
        💥 𝐁𝐎𝐎𝐌 💥
╚═══━━━─── • ───━━━═══╝

😭 𝐄ʟɪᴍɪɴᴀᴛᴇᴅ:

{loser_link}

💸 ₹{loser_bet}
𝐋ᴏꜱᴛ!
""",
        parse_mode="HTML"
    )

    # ============================================================
    # FINAL WINNER
    # ============================================================
    if len(game["players"]) == 1:

        winner_id = list(game["players"].keys())[0]

        winner = game["players"][winner_id]

        reward = winner["bet"]

        pdata = get_user(winner_id, winner["name"])

        # 💰 ADD REAL BALANCE
        pdata["money"] += reward
        save_data()

        winner_link = f"<a href='tg://user?id={winner_id}'>{winner['name']}</a>"

        # 🖼 DP FETCH
        photos = await context.bot.get_user_profile_photos(
            winner_id,
            limit=1
        )

        text = f"""
╔═══━━━─── • ───━━━═══╗
        👑 𝐖𝐈𝐍𝐍𝐄𝐑 👑
╚═══━━━─── • ───━━━═══╝

🏆 {winner_link}

━━━━━━━━━━━━━━━━━━━━━━

💰 𝐖ᴏɴ:
₹{reward}

🔥 𝐁ᴏᴍʙ 𝐂ʜᴀᴍᴘɪᴏɴ!

💎 𝐑ᴇᴀʟ 𝐁ᴀʟᴀɴᴄᴇ
𝐀ᴅᴅᴇᴅ 𝐒ᴜᴄᴄᴇꜱꜱғᴜʟʟʏ!

━━━━━━━━━━━━━━━━━━━━━━

🎉 𝐂ᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ!
"""

        if photos.photos:

            msg = await context.bot.send_photo(
                chat_id,
                photo=photos.photos[0][-1].file_id,
                caption=text,
                parse_mode="HTML"
            )

        else:

            msg = await context.bot.send_message(
                chat_id,
                text,
                parse_mode="HTML"
            )

        # 📌 AUTO PIN
        try:
            await context.bot.pin_chat_message(
                chat_id,
                msg.message_id
            )
        except:
            pass

        del bomb_games[chat_id]

        return

    # ============================================================
    # NEXT ROUND
    # ============================================================
    game["allow_left"] = True

    await context.bot.send_message(
        chat_id,
        """
╔═══━━━─── • ───━━━═══╗
      ⚠️ 𝐍𝐄𝐗𝐓 𝐑𝐎𝐔𝐍𝐃 ⚠️
╚═══━━━─── • ───━━━═══╝

⏳ 15 𝐒ᴇᴄ 𝐁ʀᴇᴀᴋ!

🏃 𝐋ᴇᴀᴠᴇ?
👉 /left
"""
    )

    await asyncio.sleep(15)

    if chat_id not in bomb_games:
        return

    game["allow_left"] = False

    await start_bomb_round(chat_id, context)


# ============================================================
# LEFT GAME
# ============================================================
async def left_game(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    uid = update.effective_user.id

    if chat_id not in bomb_games:
        return

    game = bomb_games[chat_id]

    if not game["allow_left"]:
        return await update.message.reply_text(
            "❌ 𝐘ᴏᴜ 𝐂ᴀɴ'ᴛ 𝐋ᴇᴀᴠᴇ 𝐍ᴏᴡ!"
        )

    if uid not in game["players"]:
        return

    pdata = get_user(uid, game["players"][uid]["name"])

    reward = game["players"][uid]["bet"]

    # 💰 RETURN BALANCE
    pdata["money"] += reward
    save_data()

    name = game["players"][uid]["name"]

    user_link = f"<a href='tg://user?id={uid}'>{name}</a>"

    del game["players"][uid]

    await update.message.reply_text(
        f"""
╔═══━━━─── • ───━━━═══╗
         🏃 𝐋𝐄𝐅𝐓 🏃
╚═══━━━─── • ───━━━═══╝

👤 {user_link}

💰 ₹{reward}
𝐑ᴇᴛᴜʀɴᴇᴅ!
""",
        parse_mode="HTML"
    )


# ================= GUN DUEL =================

gun_games = {}

# ================= /GUN =================
async def gun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id in gun_games:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
    ⚠️ 𝐆𝐀𝐌𝐄 𝐀𝐋𝐑𝐄𝐀𝐃𝐘 ⚠️
╚═══━━━─── • ───━━━═══╝

🔫 𝐀 𝐆ᴜɴ 𝐃ᴜᴇʟ 𝐈ꜱ 𝐀ʟʀᴇᴀᴅʏ 𝐑ᴜɴɴɪɴɢ!

⏳ 𝐖ᴀɪᴛ 𝐅ᴏʀ 𝐈ᴛ 𝐓ᴏ 𝐅ɪɴɪꜱʜ...
"""
        )

    if not context.args:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
        💰 𝐔𝐒𝐄 💰
╚═══━━━─── • ───━━━═══╝

🔫 𝐒ᴛᴀʀᴛ 𝐀 𝐆ᴜɴ 𝐃ᴜᴇʟ!

✍ 𝐄xᴀᴍᴘʟᴇ:
 /gun 500
"""
        )

    try:
        amount = int(context.args[0])

        if amount <= 0:
            return

    except:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
       ❌ 𝐈𝐍𝐕𝐀𝐋𝐈𝐃 ❌
╚═══━━━─── • ───━━━═══╝

💸 𝐈ɴᴠᴀʟɪᴅ 𝐁ᴇᴛ 𝐀ᴍᴏᴜɴᴛ!
"""
        )

    pdata = get_user(user.id, user.first_name)

    if pdata["money"] < amount:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
      💸 𝐍𝐎 𝐌𝐎𝐍𝐄𝐘 💸
╚═══━━━─── • ───━━━═══╝

❌ 𝐘ᴏᴜ 𝐃ᴏɴ'ᴛ 𝐇ᴀᴠᴇ 𝐄ɴᴏᴜɢʜ 𝐁ᴀʟᴀɴᴄᴇ!
"""
        )

    gun_games[chat_id] = {
        "creator": user.id,
        "creator_name": user.first_name,
        "amount": amount,
        "players": [],
        "started": False
    }

    await update.message.reply_text(
        f"""
╔═══━━━─── • ───━━━═══╗
      🔫 𝐆𝐔𝐍 𝐃𝐔𝐄𝐋 🔫
╚═══━━━─── • ───━━━═══╝

👑 𝐂ʀᴇᴀᴛᴏʀ:
{user.first_name}

💰 𝐁ᴇᴛ:
₹{amount}

⚡ 𝐉ᴏɪɴ 𝐔ꜱɪɴɢ:
 /gjoin {amount}

⏳ 𝐎ɴʟʏ 𝟐 𝐏ʟᴀʏᴇʀꜱ 𝐂ᴀɴ 𝐏ʟᴀʏ!
"""
    )


# ================= /GJOIN =================
async def gjoin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in gun_games:
        return

    game = gun_games[chat_id]

    if game["started"]:
        return

    if user.id == game["creator"]:
        return

    if len(game["players"]) >= 1:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
        ⚠️ 𝐅𝐔𝐋𝐋 ⚠️
╚═══━━━─── • ───━━━═══╝

🔫 𝐓ʜɪꜱ 𝐃ᴜᴇʟ 𝐈ꜱ 𝐀ʟʀᴇᴀᴅʏ 𝐅ᴜʟʟ!
"""
        )

    if not context.args:
        return await update.message.reply_text(
            f"""
╔═══━━━─── • ───━━━═══╗
        💰 𝐔𝐒𝐄 💰
╚═══━━━─── • ───━━━═══╝

✍ 𝐓ʏᴘᴇ:

/gjoin {game['amount']}
"""
        )

    try:
        amount = int(context.args[0])

    except:
        return

    if amount != game["amount"]:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
       ❌ 𝐖𝐑𝐎𝐍𝐆 ❌
╚═══━━━─── • ───━━━═══╝

💰 𝐁ᴇᴛ 𝐀ᴍᴏᴜɴᴛ 𝐃ᴏᴇꜱɴ'ᴛ 𝐌ᴀᴛᴄʜ!
"""
        )

    pdata = get_user(user.id, user.first_name)

    if pdata["money"] < amount:
        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
      💸 𝐍𝐎 𝐌𝐎𝐍𝐄𝐘 💸
╚═══━━━─── • ───━━━═══╝

❌ 𝐍ᴏᴛ 𝐄ɴᴏᴜɢʜ 𝐁ᴀʟᴀɴᴄᴇ!
"""
        )

    creator_data = get_user(
        game["creator"],
        game["creator_name"]
    )

    creator_data["money"] -= amount
    pdata["money"] -= amount

    save_data()

    game["players"].append(user.id)

    game["player2"] = user.id
    game["player2_name"] = user.first_name
    game["started"] = True

    game["shots"] = {
        game["creator"]: 0,
        user.id: 0
    }

    await update.message.reply_text(
        f"""
╔═══━━━─── • ───━━━═══╗
     🔥 𝐃𝐔𝐄𝐋 𝐒𝐓𝐀𝐑𝐓 🔥
╚═══━━━─── • ───━━━═══╝

⚔️ 𝐏ʟᴀʏᴇʀ𝐬:

👤 {game['creator_name']}
🆚
👤 {user.first_name}

🔫 𝐒ᴘᴀᴍ:
/shoot

⏰ 𝐓ɪᴍᴇ:
1 𝐌ɪɴᴜᴛᴇ

💥 𝐖ʜᴏ 𝐒ʜᴏᴏᴛ𝐬 𝐌ᴏʀᴇ = 𝐖ɪɴ!
"""
    )

    asyncio.create_task(
        gun_timer(chat_id, context)
    )


# ================= /SHOOT =================
async def shoot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in gun_games:
        return

    game = gun_games[chat_id]

    if not game["started"]:
        return

    if user.id not in [
        game["creator"],
        game["player2"]
    ]:
        return

    game["shots"][user.id] += 1


# ================= TIMER =================
async def gun_timer(chat_id, context):

    await asyncio.sleep(60)

    if chat_id not in gun_games:
        return

    game = gun_games[chat_id]

    p1 = game["creator"]
    p2 = game["player2"]

    s1 = game["shots"][p1]
    s2 = game["shots"][p2]

    if s1 > s2:
        winner = p1
        winner_name = game["creator_name"]

    elif s2 > s1:
        winner = p2
        winner_name = game["player2_name"]

    else:

        pdata1 = get_user(p1, game["creator_name"])
        pdata2 = get_user(p2, game["player2_name"])

        pdata1["money"] += game["amount"]
        pdata2["money"] += game["amount"]

        save_data()

        del gun_games[chat_id]

        return await context.bot.send_message(
            chat_id,
            """
╔═══━━━─── • ───━━━═══╗
        🤝 𝐃𝐑𝐀𝐖 🤝
╚═══━━━─── • ───━━━═══╝

⚔️ 𝐁ᴏᴛʜ 𝐏ʟᴀʏᴇʀꜱ 𝐅ɪʀᴇᴅ 𝐄Qᴜᴀʟ 𝐒ʜᴏᴛꜱ!

💰 𝐁ᴇᴛ 𝐑ᴇꜰᴜɴᴅᴇᴅ.
"""
        )

    reward = game["amount"] * 2

    wdata = get_user(winner, winner_name)
    wdata["money"] += reward

    save_data()

    photos = await context.bot.get_user_profile_photos(
        winner,
        limit=1
    )

    winner_link = (
        f"<a href='tg://user?id={winner}'>"
        f"{winner_name}</a>"
    )

    caption = f"""
╔═══━━━─── • ───━━━═══╗
       👑 𝐖𝐈𝐍𝐍𝐄𝐑 👑
╚═══━━━─── • ───━━━═══╝

🏆 𝐂ʜᴀᴍᴘɪᴏɴ:
{winner_link}

━━━━━━━━━━━━━━━━━━

🔫 𝐒ʜᴏᴛ 𝐂ᴏᴜɴᴛ:

⚔️ {game['creator_name']} ➜ {s1}
⚔️ {game['player2_name']} ➜ {s2}

━━━━━━━━━━━━━━━━━━

💰 𝐖ᴏɴ:
₹{reward}

💎 𝐀ᴅᴅᴇᴅ 𝐓ᴏ 𝐑ᴇᴀʟ 𝐁ᴀʟᴀɴᴄᴇ!

🔥 𝐆ᴜɴ 𝐊ɪɴɢ!
"""

    if photos.total_count > 0:

        file_id = photos.photos[0][-1].file_id

        msg = await context.bot.send_photo(
            chat_id,
            photo=file_id,
            caption=caption,
            parse_mode="HTML"
        )

    else:

        msg = await context.bot.send_message(
            chat_id,
            caption,
            parse_mode="HTML"
        )

    try:
        await context.bot.pin_chat_message(
            chat_id,
            msg.message_id
        )
    except:
        pass

    del gun_games[chat_id]

# ================= GN TAG SYSTEM =================
import asyncio
import random
import html

# ❤️ 100 RANDOM GOOD NIGHT MESSAGES
GN_MESSAGES = [
    "🌙 arey babu shona 😴 ab so bhi jao warna sapne me bhoot aa jayega 👻",
    "💖 oye hero ab mobile rakho aur araam se so jao 😌",
    "🌌 itni raat tak jagoge toh chand bhi complain karega 😭",
    "😴 jao jaake kambal odho aur pyara sa dream dekho 💞",
    "🛌 arey jaan ab good night bolo aur aankh band karo 🌙",
    "💘 tum online ho isliye neend bhi online hi reh gayi 😭",
    "🌙 babu so jao warna morning me zombie lagoge 🧟",
    "💖 ek pyari si jhappi lo aur so jao 🤗",
    "😌 chalo ab sapno ki duniya me entry maro ✨",
    "🌃 itni raat me jagna health ke liye illegal hai 🚨",
    "💤 oye cutie phone charge pe lagao aur khud bhi charge ho jao 😴",
    "🌙 good night hero 😎 kal fir bakchodi karenge 😂",
    "💞 arey meri jaan ab neend ko ignore mat karo 😭",
    "✨ chand bhi bol raha hai ab so ja pagle 🌙",
    "😴 so ja warna takiya naraz ho jayega 😭",
    "💖 pyari si neend tumhara wait kar rahi hai 😌",
    "🌌 jao babu dream me pizza kha lena 🍕😂",
    "😌 good night shona 🌙 sapne me milte hain 💘",
    "💤 ab aur kitna scroll karoge 😭 so bhi jao",
    "🌙 oye sleepy panda 🐼 ab aankh band karo 😴",
    "💞 good night meri online duniya ke superstar ⭐",
    "😌 jao warna mummy aa jayegi phone lene 😭",
    "🌃 ab so jao warna morning me uth nahi paoge 😂",
    "💖 ek flying kiss 😘 aur seedha sleep mode on",
    "😴 babu neend ka recharge pending hai 😭",
    "🌙 arey cutie pie ab good night bolo 💘",
    "✨ kal subah fir hero banna abhi so jao 😌",
    "💤 mobile se shaadi mat karo ab so bhi jao 😂",
    "🌌 chand mama attendance le rahe hain 🌙",
    "💞 tumhare bina neend bhi lonely feel kar rahi hai 😭",
    "😴 arey babu aankhon ko bhi rest do 😌",
    "🌙 sapno me VIP entry milne wali hai 😂",
    "💖 so jao warna dark circles free milenge 😭",
    "✨ good night champion 🏆",
    "😌 duniya so gayi sirf tum online ho 😂",
    "💞 jao pyari si neend pakdo 😴",
    "🌙 oye drama king/queen ab so jao 😭",
    "💤 neend waiting list me hai 😌",
    "💖 arey meri jaan phone rakho 🥺",
    "🌃 raat ho gayi babu ab rest karo 😴",
    "😌 good night sunshine 🌙",
    "💞 sapne me ice cream khana mat bhoolna 🍦😂",
    "🌙 chalo ab aankhon ko airplane mode pe daalo ✈️",
    "😴 so jao warna alarm bhi gussa karega 😂",
    "💖 tumhari neend tumse milna chahti hai 😌",
    "🌌 ab good night bolkar chup chaap so jao 😂",
    "💤 hero ji sleep mode activate karo 😴",
    "🌙 cutie ab moon ko company mat do 😂",
    "💞 pyari si smile ke saath so jao 😌",
    "😴 sapno me party karna 🎉",
    "🌃 babu online class band karo aur so jao 😂",
    "💖 tumhara takiya tumhe miss kar raha hai 😭",
    "🌙 oye sleepyhead ab rest lo 😌",
    "✨ good night future billionaire 💸",
    "💤 arey pagle/pagli ab neend ko haan bol do 😂",
    "🌌 moonlight bhi tumhe sleep wish kar rahi hai 🌙",
    "💞 pyari si raat aur pyara sa tum 😌",
    "😴 kal fir group me dhamal machayenge 😂",
    "🌙 ab chup chap kambal me ghus jao 😭",
    "💖 tumhari neend buffering me hai 😂",
    "✨ good night lovely human 💘",
    "💤 phone ko bhi rest chahiye 😌",
    "🌌 ab bas bhi karo aur so jao 😂",
    "😴 sapne me chocolate factory jaana 🍫",
    "💞 jao babu dreamland wait kar raha hai 🌙",
    "🌃 ab aankhon ka shutter down karo 😂",
    "💖 good night sweet potato 😭😂",
    "🌙 tumhare sapne HD quality me aaye 😌",
    "💤 arey jaan ab good night mandatory hai 😂",
    "✨ neend ka OTP aa gaya hai 😭",
    "💞 pyari si neend aur pyare se tum 💘",
    "😴 so jao warna battery low ho jaoge 🔋",
    "🌌 chand bhi so gaya tum kab soge 😂",
    "💖 babu sleep karo warna panda bana dunga 🐼",
    "🌙 pyari si hug 🤗 aur good night",
    "😌 jao kal ka din conquer karna hai 😎",
    "💤 ab mobile ko bye bolo 😂",
    "💞 sapne me unicorn mil sakta hai 🦄",
    "🌃 good night meri jaaneman 😭💘",
    "😴 arey cutie ab toh so jao 😌",
    "💖 moon bhi tumhe dekhke smile kar raha hai 🌙",
    "✨ sleepy vibes incoming 😂",
    "💤 jaake takiye ko hug karo 🤗",
    "🌌 pyari si raat mubarak 😌",
    "💞 good night superstar 🌟",
    "😴 ab aur kitna online rahoge 😭",
    "🌙 hero ji sleep ka mission complete karo 😂",
    "💖 sapne me maggi khana 🍜",
    "✨ pyari si good night from bot 💘",
    "💤 ab neend ko seen mat karo 😂",
    "🌃 tumhara bed tumhe yaad kar raha hai 😭",
    "😌 sweet dreams cutie 🌙",
    "💞 mobile rakho aur pyari si neend lo 😴",
    "🌌 dream mode activated ✨",
    "💖 arey babu ab aankh band karo 😂",
    "🌙 sleep like a king 👑",
    "😴 good night meri pyari duniya 💘",
    "💤 ab so jao warna rooster bula lunga 🐓😂",
    "✨ pyari si raat aur pyari si vibe 😌",
    "💞 sapno me milte hain hero 😎",
    "🌃 good night and take care 💖",
    "😴 neend ka invitation accept karo 😂",
    "🌙 ab phone ko bhi sula do 😌"
]

# ================= GNTAG COMMAND =================
async def gntag(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ✅ GROUP ONLY
    if update.effective_chat.type not in ["group", "supergroup"]:
        return await update.message.reply_text("❌ Group only")

    user = update.effective_user
    chat_id = update.effective_chat.id

    # ✅ ADMIN CHECK
    member = await context.bot.get_chat_member(chat_id, user.id)

    if member.status not in ["administrator", "creator"]:
        return await update.message.reply_text("❌ Admin only")

    # ✅ FETCH USERS
    all_users = list(tracker.find())

    if not all_users:
        return await update.message.reply_text("❌ No users saved")

    await update.message.reply_text(
        f"🌙 Sending Good Night wishes to {len(all_users)} users..."
    )

    # ✅ ANTI FLOOD DELAY
    delay = 3

    # ✅ SEND ONE BY ONE
    for u in all_users:

        try:
            uid = u["_id"]

            # ✅ SAFE NAME
            safe_name = html.escape(
                str(u.get("name", "User"))[:25]
            )

            # ✅ CLICKABLE USER
            mention = (
                f"<a href='tg://user?id={uid}'>"
                f"{safe_name}</a>"
            )

            # ✅ RANDOM MESSAGE
            random_msg = random.choice(GN_MESSAGES)

            # ✅ FINAL TEXT
            text = f"{mention} ➤ {random_msg}"

            # ✅ SEND
            await update.message.reply_text(
                text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

            # ✅ WAIT
            await asyncio.sleep(delay)

        except Exception as e:
            print(f"GNTAG ERROR: {e}")

    # ✅ DONE
    await update.message.reply_text(
        "✅ Good Night tagging completed 🌙"
    )    
#===================ADMIN LIST======================

from telegram.constants import ParseMode
import asyncio
import html

#================ ADMIN LIST =================#

async def admin_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # ⚡ Loading Message
    loading = await update.message.reply_text(
        "╭━━〔 ⚡ 𝐋ᴏᴀᴅɪɴɢ 𝐀ᴅᴍɪɴ 𝐋ɪsᴛ ⚡ 〕━━╮\n"
        "┃ 🔍 Collecting Admin Energy...\n"
        "┃ ⏳ Please Wait...\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )

    # ⏳ Loading vibe
    await asyncio.sleep(2)

    # 👑 Get Admins
    admins = await context.bot.get_chat_administrators(chat.id)

    owner_text = "👑 None"
    admin_list_text = ""

    for admin in admins:
        user = admin.user

        # Clickable Name
        name = html.escape(user.first_name or "Admin")

        clickable_name = (
            f'<a href="tg://user?id={user.id}">{name}</a>'
        )

        # 👑 Owner
        if admin.status == "creator":
            owner_text = (
                f"╭─❖ 👑 𝐆ʀᴏᴜᴘ 𝐎ᴡɴᴇʀ 👑 ❖─╮\n"
                f"     {clickable_name}\n"
                f"╰──────────────────╯"
            )

        # ❤️ Admins
        else:
            admin_list_text += (
                f"➤ {clickable_name}  ❤️\n"
            )

    if not admin_list_text:
        admin_list_random = "➤ None ❤️"

    # ✨ Final Attractive Message
    text = (
        "╔══❖•ೋ° 🌸 °ೋ•❖══╗\n"
        "      ✨ 𝐀𝐃𝐌𝐈𝐍 𝐏𝐀𝐍𝐄𝐋 ✨\n"
        "╚══❖•ೋ° 🌸 °ೋ•❖══╝\n\n"

        f"{owner_text}\n\n"

        "╭━━━〔 💎 𝐀ᴅᴍɪɴ 𝐓ᴇᴀᴍ 💎 〕━━━╮\n"
        f"{admin_list_text}"
        "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"

        "⚡ 𝐑ᴇsᴘᴇᴄᴛ 𝐓ʜᴇ 𝐀ᴅᴍɪɴ𝐬 ⚡"
    )

    # 🔄 Edit Loading Message
    await loading.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )


# ================= AUTO SAVE USERS =================
async def save_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.effective_user:
        return

    user = update.effective_user

    try:
        tracker.update_one(
            {"_id": user.id},
            {
                "$set": {
                    "name": user.first_name
                }
            },
            upsert=True
        )

    except Exception as e:
        print(f"SAVE USER ERROR: {e}")


#=====================CHAT AI =======================


# ==================================================
# 💖 GEMINI AI SETUP
# ==================================================

#===================== CHAT AI =======================





# ==================================================
# 💖 OPENROUTER AI CLIENT
# ==================================================


import os
import random
import asyncio
from openai import OpenAI

# ==================================================
# 💖 OPENROUTER CLIENT
# ==================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client_ai = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ==================================================
# 💖 BASIC INFO
# ==================================================

BOT_USERNAME = "@iim_nikibot"
OWNER = "@YTT_BISHAL"

# ==================================================
# 💖 MONGO COLLECTION (YOUR SAME)
# ==================================================

niki_users = db_main["niki_memory"]

# ==================================================
# 💖 MODELS (FALLBACK SYSTEM)
# ==================================================

MODELS = [
    "meta-llama/llama-3.1-8b-instruct",
    "openchat/openchat-7b",
    "mistralai/mistral-7b-instruct"
]

# ==================================================
# 💖 MOOD DETECTION
# ==================================================

def detect_mood(text):

    text = text.lower()

    if any(w in text for w in ["love", "pyar", "jaan", "baby", "kiss"]):
        return "love"
    if any(w in text for w in ["sad", "cry", "alone", "broken"]):
        return "sad"
    if any(w in text for w in ["angry", "gussa", "hate"]):
        return "angry"
    if any(w in text for w in ["happy", "lol", "hehe"]):
        return "happy"

    return "cute"

# ==================================================
# 💖 TYPING DELAY (HUMAN FEEL)
# ==================================================

async def typing_delay(update, text):
    delay = min(len(text) * 0.02, 2.5)
    await asyncio.sleep(delay)

# ==================================================
# 💖 AI ENGINE (FALLBACK SYSTEM)
# ==================================================

def get_ai_reply(prompt, text, chat_type):

    style = ""

    if chat_type == "private":
        style = "You are romantic emotional girlfriend AI."
    else:
        style = "You are cute short group chatbot."

    final_prompt = prompt + "\nStyle:\n" + style

    for model in MODELS:

        try:
            response = client_ai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": final_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.9,
                max_tokens=300
            )

            reply = response.choices[0].message.content

            if reply:
                return reply.strip()

        except Exception as e:
            print("MODEL FAIL:", model, e)
            continue

    return "🥺 sorry baby, abhi thoda busy hu..."

# ==================================================
# 💖 MAIN AI HANDLER
# ==================================================

async def niki_ai(update, context):

    if not update.message:
        return

    text = update.message.text

    if not text or text.startswith("/"):
        return

    # ==================================================
    # 💖 USER INFO
    # ==================================================

    user = update.effective_user
    user_id = str(user.id)
    name = user.first_name
    chat_type = update.effective_chat.type

    # ==================================================
    # 💖 MONGO MEMORY
    # ==================================================

    user_data = niki_users.find_one({"user_id": user_id})

    if not user_data:
        user_data = {
            "user_id": user_id,
            "name": name,
            "history": []
        }
        niki_users.insert_one(user_data)

    history = user_data.get("history", [])
    history.append(text)

    if len(history) > 15:
        history = history[-15:]

    niki_users.update_one(
        {"user_id": user_id},
        {"$set": {"history": history, "name": name}}
    )

    history_text = "\n".join(history)

    # ==================================================
    # 💖 TRIGGER SYSTEM
    # ==================================================

    is_niki = "niki" in text.lower()
    is_reply = False

    if update.message.reply_to_message:
        if update.message.reply_to_message.from_user:
            if update.message.reply_to_message.from_user.is_bot:
                is_reply = True

    if chat_type != "private":
        if not is_niki and not is_reply:
            return

    # ==================================================
    # 💖 OWNER SYSTEM
    # ==================================================

    owner_words = [
        "owner", "developer", "dev", "creator",
        "who made you", "boss", "tumhara owner"
    ]

    if any(w in text.lower() for w in owner_words):

        replies = [
            f"Hehe 🤭 {OWNER} is my owner 💖",
            f"I was created by {OWNER} 😌✨",
            f"My developer is {OWNER} 💕",
            f"{OWNER} is my special one 🥺💖",
            f"I'm only {OWNER}'s Niki 😤💖"
        ]

        await update.message.reply_text(random.choice(replies))
        return

    # ==================================================
    # 💖 MOOD
    # ==================================================

    mood = detect_mood(text)

    # ==================================================
    # 💖 PROMPT
    # ==================================================

    prompt = f"""
You are Niki, a cute telegram bot girl.

Personality:
- Friendly
- Emotional
- Romantic
- Hinglish style
- Never say AI

Owner: {OWNER}
User: {name}
Mood: {mood}

Chat History:
{history_text}

Message:
{text}
"""

    # ==================================================
    # 💖 HUMAN TYPING FEEL
    # ==================================================

    await typing_delay(update, text)

    # ==================================================
    # 💖 AI RESPONSE
    # ==================================================

    try:

        reply = get_ai_reply(prompt, text, chat_type)

        await update.message.reply_text(reply)

    except Exception as e:

        print("ERROR:", e)

        await update.message.reply_text(
            f"⚠️ ERROR:\n{str(e)[:200]}"
        )

    

        
    

    
       
        

     
# =================== MAIN FUNCTION ===================
async def mongo_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mongo_data = load_from_mongo()

    if mongo_data:
        await update.message.reply_text("✅ MongoDB connected & data mil gaya")
    else:
        await update.message.reply_text("❌ MongoDB se data nahi mila")
# =================== MAIN FUNCTION ===================

    # =================== MAIN FUNCTION ===================
# =================== MAIN FUNCTION ===================
def main():
    global data

    load_data()

    mongo_data = load_from_mongo()
    if mongo_data:
        data = mongo_data

    # ================= APP BUILD =================
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ================= 🔥 SAFE POST INIT =================
    async def post_init(app):
        await app.bot.delete_webhook(drop_pending_updates=True)
        print("💖 Bot started clean (no conflict mode)")

        # 🔥 SAFE MONITOR START (NO DUPLICATE TASK)
        if not hasattr(app, "monitor_started"):
            asyncio.create_task(auto_monitor())
            app.monitor_started = True

    app.post_init = post_init

    # ================= 🚀 RENDER SAFETY =================
    if os.getenv("RENDER"):
        print("🚀 Running on Render - single instance mode")

    # ================= 🔥 TRACK SYSTEM (FIRST - MUST) =================
    app.add_handler(MessageHandler(filters.ALL, track_user), group=-1)
    app.add_handler(ChatMemberHandler(track_join, ChatMemberHandler.CHAT_MEMBER), group=-1)
     
    # ---------------- Command Handlers ----------------
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("toprich", toprich))
    app.add_handler(CommandHandler("topkill", topkill))
    app.add_handler(CommandHandler("bal", balance))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("claim", claim))
    app.add_handler(CommandHandler("protect", protect))
    app.add_handler(CommandHandler("rob", rob))
    app.add_handler(CommandHandler("kill", kill))
    app.add_handler(CommandHandler("give", give))
    app.add_handler(CommandHandler("bail", bail))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("gift", gift))
    app.add_handler(CommandHandler("addgif", addgif))
    app.add_handler(CommandHandler("economy", economy))
    app.add_handler(CommandHandler("revive", revive))
    app.add_handler(CommandHandler("id", show_id))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("own", own))
    app.add_handler(CommandHandler("items", items))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("guess", guess))
    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CommandHandler("mongo", mongo_check))
    app.add_handler(CommandHandler("addbal", addbal))
    app.add_handler(CommandHandler("removebal", removebal))
    app.add_handler(CommandHandler("setbal", setbal))
    app.add_handler(CommandHandler("send", send))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("duel", duel))

    app.add_handler(CommandHandler("savegif", savegif))
    app.add_handler(CommandHandler("kiss", kiss))
    app.add_handler(CommandHandler("hug", hug))
    app.add_handler(CommandHandler("slap", slap))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("pat", pat))
    app.add_handler(CommandHandler("punch", punch))
    app.add_handler(CommandHandler("bite", bite))
    app.add_handler(CommandHandler("cuddle", cuddle))
    app.add_handler(CommandHandler("poke", poke))
    app.add_handler(CommandHandler("tickle", tickle))
    app.add_handler(CommandHandler("love", love))

    app.add_handler(CommandHandler("couple", couple))
    app.add_handler(CommandHandler("setcouplepic", setcouplepic))
    app.add_handler(CommandHandler("couplehistory", couplehistory))
    app.add_handler(CommandHandler("coupleleaderboard", coupleleaderboard))

    app.add_handler(CommandHandler("propose", propose))
    app.add_handler(CommandHandler("addgifs", addgifs))
    app.add_handler(CommandHandler("partner", partner))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("marriagehistory", history))
    app.add_handler(CommandHandler("divorce", divorce))
    app.add_handler(CommandHandler("look", look))
    app.add_handler(CommandHandler("brain", brain))
    app.add_handler(CommandHandler("magic", magic))
    app.add_handler(CommandHandler("dart", dart))
   
    app.add_handler(CommandHandler("accept", accept))
    app.add_handler(CommandHandler("tr", tr))
    app.add_handler(CommandHandler("close", close_bot))
    app.add_handler(CommandHandler("open", open_bot))
    app.add_handler(CommandHandler("filter", filter_cmd))
    app.add_handler(CommandHandler("dfilter", dfilter_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(CommandHandler("unban", unban_cmd))

    app.add_handler(CommandHandler("mute", mute_cmd))
    app.add_handler(CommandHandler("unmute", unmute_cmd))

    app.add_handler(CommandHandler("tmute", tmute_cmd))
    app.add_handler(CommandHandler("tban", tban_cmd))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("card", card))
    app.add_handler(CommandHandler("joinbet", joinbet))
    app.add_handler(CommandHandler("flip", flip))
    app.add_handler(CommandHandler("coin", coin))
    app.add_handler(CommandHandler("cduel", cduel))

    app.add_handler(CommandHandler("head", head))
    app.add_handler(CommandHandler("tail", tail))
    app.add_handler(CommandHandler("bet", bet))

    app.add_handler(CommandHandler("dhead", dhead))
    app.add_handler(CommandHandler("dtail", dtail))
    app.add_handler(CommandHandler("dbet", dbet))
    app.add_handler(CommandHandler("slot", slot))
    app.add_handler(CommandHandler("slotlb", slot_leaderboard))
    app.add_handler(CommandHandler("mines", mines))
    app.add_handler(CommandHandler("wordseek", wordseek))
    app.add_handler(CommandHandler("new4", new_game))
    app.add_handler(CommandHandler("new5", new_game))
    app.add_handler(CommandHandler("new6", new_game))
    app.add_handler(CommandHandler("wprofile", wprofile))
    app.add_handler(CommandHandler("wbadges", wbadges))
    app.add_handler(CommandHandler("addword4", add_word))
    app.add_handler(CommandHandler("addword5", add_word))
    app.add_handler(CommandHandler("addword6", add_word))
    
    app.add_handler(CommandHandler("end", end))
    app.add_handler(CommandHandler("wordlb", word_leaderboard))
    app.add_handler(CommandHandler("tgall", tgall))
    app.add_handler(CommandHandler("gntag", gntag))
    app.add_handler(CommandHandler("sdb", sdb))
    app.add_handler(CommandHandler("bomb", bomb_help))
    app.add_handler(CommandHandler("bjoin", bjoin))
    app.add_handler(CommandHandler("pass", pass_bomb))
    app.add_handler(CommandHandler("left", left_game))
    app.add_handler(CommandHandler("gun", gun))
    app.add_handler(CommandHandler("gjoin", gjoin))
    app.add_handler(CommandHandler("shoot", shoot))
    app.add_handler(CommandHandler("admin", admin_list))
    app.add_handler(CommandHandler("userinfo", userinfo))
    
    # ================= CALLBACKS =================
    app.add_handler(CallbackQueryHandler(accept, pattern="^marry_acc_"))
    app.add_handler(CallbackQueryHandler(reject, pattern="^marry_rej_"))
    app.add_handler(CallbackQueryHandler(accept_btn, pattern="^duel_acc_"))
    app.add_handler(CallbackQueryHandler(cancel_btn, pattern="^duel_rej_"))
    app.add_handler(CallbackQueryHandler(button_callback, pattern="^start_"))
    app.add_handler(CallbackQueryHandler(button, pattern="^(num_|bet_)"))
    app.add_handler(CallbackQueryHandler(mine_click, pattern="mine_|cashout"))
    app.add_handler(CallbackQueryHandler(userinfo_buttons))

    # ================= 🔥 HANDLERS (CLEAN PRIORITY ORDER) =================

    # 🛑 BLOCK
    app.add_handler(
        MessageHandler(filters.ALL, block_system),
        group=10
    )

    # 💾 SAVE USERS
    app.add_handler(
        MessageHandler(filters.ALL, save_users),
        group=9
    )

    # 🔥 FILTER SYSTEM
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            filter_checker
        ),
        group=5
    )

    # 🎮 GAME SYSTEM
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle
        ),
        group=4
    )

    # 💖 LOVE FLOW
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            love_flow
        ),
        group=3
    )

    # 🤖 MAIN AI
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            niki_ai
        ),
        group=20
    )

    # 👋 WELCOME
    app.add_handler(
        ChatMemberHandler(
            member_update_welcome,
            ChatMemberHandler.CHAT_MEMBER
        )
    )
   

    print("🔥 Niki Bot started...")

    # ================= RUN BOT =================
    app.run_polling()

if __name__ == "__main__":
    main()
