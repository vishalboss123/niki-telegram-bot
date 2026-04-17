from pymongo import MongoClient

MONGO_URL = "mongodb+srv://vishal:VISHAL123@vishal07.espy0qo.mongodb.net/?appName=Vishal07"

client = MongoClient(MONGO_URL)
db = client["mydatabase"]
backup = db["backup"]
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
        save_to_mongo()

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
        "👑 Oᴡɴᴇʀ: @YT_BISHALL"
    )

    # ✅ Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/YT_BISHALL"),
            InlineKeyboardButton("🎮 Game", callback_data="game_info")
        ],
        [
            InlineKeyboardButton("➕ Add me to your group 💌", url="https://t.me/iim_Nikibot?startgroup=true")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

# =================== CALLBACK HANDLER FOR GAME & BACK ===================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "game_info":
        game_text = (
            "🎲 Ye ek game ka rule aur command guide hai:\n\n"
            "⬇️ Neeche buttons use karke check karo ⬇️"
        )
        keyboard = [
            [
                InlineKeyboardButton("💰 Economy", callback_data="economy"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_to_start")
            ]
        ]
        await query.edit_message_text(
            game_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "economy":
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
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ]
        await query.edit_message_text(
            economy_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "help":
        help_text = "💡 Help ke liye apna owner dekho 👑"
        keyboard = [
            [InlineKeyboardButton("👑 Owner Profile", url="https://t.me/YT_BISHALL")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ]
        await query.edit_message_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "back_to_start":
        user = query.from_user  # ✅ ye add karo

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
        "👑 Oᴡɴᴇʀ: @YT_BISHALL"
    )

    keyboard = [
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/YT_BISHALL"),
            InlineKeyboardButton("🎮 Game", callback_data="game_info")
        ],
        [
            InlineKeyboardButton("➕ Add me to your group 💌", url="https://t.me/im_suvabot?startgroup=true")
        ]
    ]

    await query.edit_message_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
# =================== TOP RICHEST COMMAND ===================
async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

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
    global data
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()

                if content.count("{") > 1:
                    content = content[:content.rfind("}")+1]

                data = json.loads(content)
        else:
            data = {}
    except:
        data = {}

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
        save_to_mongo()

    return data[uid]   # ✅ correct

    return user
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
    

    if update.message.reply_to_message:
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
            f"👉 https://t.me/YT_BISHALL\n"
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

    if not update.message.reply_to_message.animation:
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
    text = "🛒 ITEM SHOP\n━━━━━━━━━━━━━━\n"
    for name, item in shop_items.items():
        text += f"• {item['emoji']} {name.title()} : ₹{item['price']}\n"
    text += "\nReply to a user and use /gift <amount> to send!"
    await update.message.reply_text(text)

# ---------------- GIFT COMMAND ----------------
# ---------------- GIFT COMMAND ----------------
# ---------------- GIFT COMMAND ----------------
async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "⚠️ If you face any problems, contact my owner 👉 @YT_BISHALL"
    )
    await update.message.reply_text(text, parse_mode="Markdown")





# =================== /ID COMMAND ===================
from telegram import Update
from telegram.ext import ContextTypes

OWNER_ID = 6175559434  # Owner numeric ID
OWNER_USERNAME = "YT_BISHALL"  # Owner Telegram username

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        save_to_mongo()

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
            save_to_mongo()

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
        save_to_mongo()

        await message.reply_text(
            f"🎉 Sahi pakda!\n\n"
            f"🤖 Bot number: {bot_number}\n"
            f"💰 Tum jeete ₹{win}"
        )
    else:
        loss = 50
        user_data["money"] -= loss
        save_data()
        save_to_mongo()

        await message.reply_text(
            f"💔 Galat guess\n\n"
            f"🤖 Bot number: {bot_number}\n"
            f"❌ ₹{loss} loss"
        )


# =================== DICE GAME ===================
import random
import asyncio

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):

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
            save_to_mongo()# auto save groups
            print(f"Group saved: {chat_id}")

    # === USERS SAVE ===
    if chat_type == "private":
        if "users" not in data:
            data["users"] = []
        if user_id not in data["users"]:
            data["users"].append(user_id)
            save_data() 
            save_to_mongo()# auto save users
            print(f"User saved: {user_id}")

# =================== FORWARD COMMAND /fw ===================
async def forward_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    OWNER_USERNAME = "@YT_BISHALL"  # sirf ye user use kar sake

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
db = client["niki_bot"]
col = db["chats"]

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
            InlineKeyboardButton("⚔️ Accept Duel", callback_data=f"accept_{user2.id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{user2.id}")
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

    for d in duels.values():

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
                    f"🎯 {d['p1_name']} ɴᴇ ɴᴜᴍʙᴇʀ ᴄʜᴏᴏꜱᴇ ᴋɪʏᴀ!"
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
                    f"🎯 {d['p2_name']} ʀᴇᴀᴅʏ!"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"🔥 {d['p1_name']} vs {d['p2_name']} ʀᴇᴀᴅʏ! Gᴀᴍᴇ ꜱᴛᴀʀᴛ ꜱᴏᴏɴ..."
                )

                await send_bet_choice(context, d["p1"])
                return


        if data[0] == "bet":

            uid = int(data[1])
            bet = int(data[2])

            if d["p1"] == uid:
                d["bet"] = bet

                await query.edit_message_text(
                    f"💰 {d['p1_name']} ɴᴇ ʙᴇᴛ ʟᴏᴄᴋ ᴋɪʏᴀ: {bet}"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"💰 {d['p1_name']} ɴᴇ {bet} ʙᴇᴛ ʟᴀɢᴀʏᴀ!"
                )

                await send_bet_choice(context, d["p2"])
                return

            if d["p2"] == uid:

                if not d.get("bet"):
                    await query.answer("Wait for P1 bet", show_alert=True)
                    return

                u1 = data_store[str(d["p1"])]
                u2 = data_store[str(d["p2"])]

                if u2["money"] < d["bet"]:
                    await context.bot.send_message(
                        d["chat"],
                        f"❌ {d['p2_name']} ke paas paise kam hai"
                    )
                    return

                u1["money"] -= d["bet"]
                u2["money"] -= d["bet"]

                save_data()
                save_to_mongo()

                await query.edit_message_text(
                    f"💰 {d['p2_name']} ɴᴇ ʙᴇᴛ ᴄᴏɴꜰɪʀᴍ ᴋɪʏᴀ: {d['bet']}"
                )

                await context.bot.send_message(
                    d["chat"],
                    f"🔥 {d['p1_name']} vs {d['p2_name']} ᴅᴜᴇʟ ꜱᴛᴀʀᴛ!"
                )

                await start_duel(context, d)
                return


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
    save_to_mongo()

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
gif_collection = db["gifs"]

# ================= LOAD GIF =================
def get_gifs(command):
    data = gif_collection.find_one({"cmd": command})
    if data:
        return data.get("gifs", [])
    return []

# ================= SAVE GIF =================
def save_gif(cmd, gif):
    gif_collection.update_one(
        {"cmd": cmd},
        {"$addToSet": {"gifs": gif}},  # duplicate avoid karega 🔥
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

    gif = random.choice(gifs)

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

    # 🔥 MongoDB se load
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
    app.add_handler(CallbackQueryHandler(accept_btn, pattern="^accept_"))
    app.add_handler(CallbackQueryHandler(cancel_btn, pattern="^cancel_"))
    app.add_handler(CallbackQueryHandler(button)) 
    app.add_handler(CommandHandler("savegif", savegif))  # 🔥 NEW
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

    # Callback
    app.add_handler(CallbackQueryHandler(button_callback))

    # Message Handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_chat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_niki_reply))

    print("🔥 Niki Bot started...")

    app.run_polling()


if __name__ == "__main__":
    main()
