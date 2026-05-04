# ================= MONGO SETUP (FINAL CLEAN) =================
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
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web).start()


# =================== IMPORTS ===================
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatPermissions, Update
from datetime import datetime, timedelta
from collections import deque
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
    
    # JSON save (optional)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
    # 🔥 MongoDB save
    backup.update_one(
        {"_id": "main_data"},
        {"$set": {"data": data}},
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

    if not update.message:
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

YOUR_OWNER_ID = 6175559434  # 👉 apna Telegram user ID daal

# ================= STORAGE =================
BOT_STATUS = {}  # {chat_id: True/False}


# ================= ADMIN / OWNER CHECK =================
async def is_admin_or_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat = update.effective_chat

    # 👑 Owner always allowed
    if user_id == YOUR_OWNER_ID:
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
    if user_id == YOUR_OWNER_ID:
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

    if user_id == YOUR_OWNER_ID:
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
            txt = "⬜"

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
client = MongoClient("YOUR_MONGO_URL")


users = db["chats"]
games = db["wordseek"]
words = db["words"]   # 👈 NEW COLLECTION

WIN_REWARD = 1000
FONT = "𝐖𝐨𝐫𝐝𝐒𝐞𝐞𝐤 𝐆𝐚𝐦𝐞"
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
async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    uid = update.effective_user.id
    size = int(update.message.text.replace("/new",""))
    

    if games.find_one({"_id": chat_id}):
        return await update.message.reply_text(
            f"{FONT}\n⚠️ 𝐆ame 𝐀lready 𝐑unning!"
        )
    doc = words.aggregate([{"$match": {"size": size}}, {"$sample": {"size": 1}}])
    doc = list(doc)

    if not doc:
        return await update.message.reply_text("❌ No words found in DB")

    doc = doc[0]

    games.update_one(
        {"_id": uid},
        {"$set": {
            "word": doc["word"],
            "hint": doc["hint"],
            "size": size,
            "attempts": 0,
            "grid": []
        }},
        upsert=True
    )

    await update.message.reply_text(
        f"{FONT}\n📊 0/30\n🎮 GAME STARTED"
    )

# ================= HANDLE =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    raw = update.message.text.lower()
    text = re.sub(r'[^a-z]', '', raw)   # 🔥 only letters allowed
    game = games.find_one({"_id": chat_id})

    # ❌ GAME NAHI HAI TOH KUCH NAHI KARNA
    if not game:
        return

    # ❌ agar command ya system text hai
    if text.startswith("/"):
        return

    secret = game["word"]
    size = game["size"]

    # ❌ wrong length ignore
    if len(text) != size:
        return

    # 🔥 REAL WORD CHECK (FAST + SAFE)
    try:
        valid = await asyncio.wait_for(is_real_word(text), timeout=1)
    except:
        valid = True

    if not valid:
         return await update.message.reply_text(
            f"{FONT}\n❌ 𝐘e 𝐕alid 𝐄nglish 𝐖ord 𝐍ehi 𝐇ai!"
        )

    games.update_one({"_id": chat_id}, {"$inc": {"attempts": 1}})
    game["attempts"] += 1
    att = game["attempts"]

    colors = check(secret, text)
    row = f"{' '.join(colors)}  = {text.upper()}"

    games.update_one({"_id": chat_id}, {"$push": {"grid": row}})

    games.update_one({"_id": chat_id})
    grid = "\n".join(game["grid"])

    await update.message.reply_text(
        f"{FONT}\n📊 {att}/30\n\n{grid}"
    )

    # ================= HINT =================
    if att == 20:
        await update.message.reply_text(f"💡 HINT:\n{game['hint']}")

    # ================= WIN =================
    # ================= WIN =================
    if text == secret:
        user_data = users.find_one({"_id": uid}) or {}
        old_wins = user_data.get("word_wins", 0)

        # 🔥 UPDATE DATA
        users.update_one(
            {"_id": uid},
            {
                "$inc": {
                    "coins": WIN_REWARD,
                    "word_wins": 1
                },
                "$set": {
                    "name": update.effective_user.first_name
                }
            },
            upsert=True
        )

        new_wins = old_wins + 1

        games.delete_one({"_id": chat_id})

        # 👤 USER LINK
        name = update.effective_user.first_name
        user_link = f"<a href='tg://user?id={uid}'>{name}</a>"

        # 🎉 WIN MESSAGE
        await update.message.reply_text(
            f"""
  ━━━━━━━━━━━━━━━━━━━━━━
    {FONT}

    🎉 WINNER: {user_link}

    💝 WORD: {secret}

    💰 +{WIN_REWARD} COINS
    🏆 GG BRO!
   ━━━━━━━━━━━━━━━━━━━━━━
    """,
            parse_mode="HTML"
        )

        # 🏅 BADGE UNLOCK SYSTEM
        if new_wins == 5:
            await update.message.reply_text("🎉 Badge Unlocked: 🥉 Rookie!")
        elif new_wins == 10:
            await update.message.reply_text("🎉 Badge Unlocked: 🥈 Skilled!")
        elif new_wins == 20:
            await update.message.reply_text("🎉 Badge Unlocked: 🥇 Pro!")
        elif new_wins == 50:
            await update.message.reply_text("🎉 Badge Unlocked: 👑 Legend!")
        elif new_wins == 100:
            await update.message.reply_text("🎉 Badge Unlocked: 💎 Master!")

            return

    # ================= LOSE =================
    if att >= 30:
        games.delete_one({"_id": uid})
        await update.message.reply_text(
            f"{FONT}\n❌ GAME OVER\nWORD WAS: {secret}"
        )

#=====================END============================
async def end_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
OWNER_ID = 123456789  # 🔥 yaha apna Telegram user id daalo

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

    app = ApplicationBuilder().token(BOT_TOKEN).build()

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
    app.add_handler(CommandHandler("userinfo", userinfo))
    app.add_handler(commandHandler("end", end_game))
    app.add_handler(CommandHandler("wordlb", word_leaderboard))
    
    # ================= CALLBACKS =================
    app.add_handler(CallbackQueryHandler(accept, pattern="^marry_acc_"))
    app.add_handler(CallbackQueryHandler(reject, pattern="^marry_rej_"))

    app.add_handler(CallbackQueryHandler(accept_btn, pattern="^duel_acc_"))
    app.add_handler(CallbackQueryHandler(cancel_btn, pattern="^duel_rej_"))

    app.add_handler(CallbackQueryHandler(button_callback, pattern="^start_"))
    
    app.add_handler(CallbackQueryHandler(button, pattern="^(num_|bet_)"))
    
    app.add_handler(CallbackQueryHandler(mine_click, pattern="mine_|cashout"))
    
    app.add_handler(CallbackQueryHandler(userinfo_buttons))

    # ================= MESSAGE =================
   

    # 1. Block system (first priority)
    app.add_handler(MessageHandler(filters.ALL, block_system), group=3)

    # 2. Filter system
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_checker), group=1)

    # 3. AI reply
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_niki_reply), group=2)

    # 4. WORD GAME (LAST)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle), group=0)

    # 🔹 5. Welcome system
    app.add_handler(ChatMemberHandler(member_update_welcome, ChatMemberHandler.CHAT_MEMBER))
 


    print("🔥 Niki Bot started...")
    
    async def start_background(app):
        asyncio.create_task(auto_monitor())

    app.post_init = start_background
    
    app.run_polling()

if __name__ == "__main__":
    main()
