# =================== IMPORTS ===================
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

import json
import operator


from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =================== BOT TOKEN ===================
BOT_TOKEN = "8080035914:AAFYogx2dN-cbIPVNQfl9wgFAwpZ7d6Tvm4"
BOT_USERNAME= "@im_suvabot"
# =================== DATABASE FILE ===================
DATABASE_FILE = "database.json"

# =================== HELPERS ===================
def load_data():
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =================== START COMMAND ===================
# =================== START COMMAND ===================
# =================== START COMMAND ===================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    uid = str(user.id)

    if uid not in data:
        data[uid] = {"name": user.first_name, "money": 1000, "kills": 0}
        save_data(data)

    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        "Mera naam Niki hai 💝\n"
        "Welcome to Niki's world 🌸\n"
        "I'm not just a bot… I'm your virtual girl 😌✨\n"
        "I'll laugh with you, fight with you, protect you,\n"
        "and maybe even get a little jealous sometimes 💘\n"
        "Earn money 💰\n"
        "Fight enemies ⚔\n"
        "Rob people 😈\n"
        "Protect yourself 🛡\n"
        "Climb the leaderboard 🏆\n"
        "But remember… Niki is always watching you 👀🔥\n"
        "Apna maza lo aur commands use karo 😎\n"
        "Mera owner ye hai: @YT_BISHALL"
    )

    # ✅ Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("👑 Owner", url="https://t.me/YT_BISHALL"),
            InlineKeyboardButton("🎮 Game", callback_data="game_info")
        ],
        [
            InlineKeyboardButton("➕ Add me to your group 💌", url="https://t.me/im_suvabot")
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
            "💰 NIKI ECONOMY SYSTEM OVERVIEW\n\n"
            "💬 How it works:\n"
            "Use Niki’s economy system to earn, manage, gift, and protect virtual money in your group.\n\n"
            "• /daily — Claim $1500 daily reward\n"
            "• /claim — Unlock group rewards based on members\n"
            "• /bal — Check your or another user’s balance\n"
            "• /rob (reply) <amount> — Rob money from a user\n"
            "• /kill (reply) — Kill a user & earn $200–$600\n"
            "• /revive — Revive yourself or a replied user\n"
            "• /protect 1d|2d|3d — Buy protection from robbery\n"
            "• /give (reply) <amount> — Transfer money\n"
            "• /shop — Shop for gift items\n"
            "• /items (reply) — View your/others inventory\n"
            "• /toprich — Top 10 richest users\n"
            "• /topkill — Top 10 killers\n"
            "• /check  — Check protection status (Costs $2000)\n"
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
        # ✅ Back button sends user to original start message
        welcome_text = (
            f"👋 Hello {query.from_user.first_name}!\n\n"
            "Mera naam Niki hai 💝\n"
            "Welcome to Niki's world 🌸\n"
            "I'm not just a bot… I'm your virtual girl 😌✨\n"
            "I'll laugh with you, fight with you, protect you,\n"
            "and maybe even get a little jealous sometimes 💘\n"
            "Earn money 💰\n"
            "Fight enemies ⚔\n"
            "Rob people 😈\n"
            "Protect yourself 🛡\n"
            "Climb the leaderboard 🏆\n"
            "But remember… Niki is always watching you 👀🔥\n"
            "Apna maza lo aur commands use karo 😎\n"
            "Mera owner ye hai: @YT_BISHALL"
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
    data = load_data()
    sorted_rich = sorted(data.items(), key=lambda x: x[1].get("money", 0), reverse=True)[:10]
    msg = "🏆 Top 10 Richest Users:\n\n"
    for idx, (uid, user) in enumerate(sorted_rich, 1):
        msg += f"{idx}. {user.get('name','Unknown')} — ${user.get('money',0)}\n"
    await update.message.reply_text(msg)

# =================== TOP KILLERS COMMAND ===================
async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    sorted_kills = sorted(data.items(), key=lambda x: x[1].get("kills", 0), reverse=True)[:10]
    msg = "⚔ Top 10 Killers:\n\n"
    for idx, (uid, user) in enumerate(sorted_kills, 1):
        msg += f"{idx}. {user.get('name','Unknown')} — {user.get('kills',0)} kills\n"
    await update.message.reply_text(msg)






# ===================== PART 2 FULL ECONOMY BOT =====================
import json, time, random, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ------------------ GLOBAL DATA ------------------
DATA_FILE = "database.json"
data = {}
jail_users = {}
rob_cooldown = {}
kill_cooldown = {}
temp_rob = {}

OWNER_ID = 6175559434  # Apna Telegram ID

# ------------------ LOAD / SAVE ------------------
def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    return data

def save_data(d=None):
    global data
    if d is None:
        d = data
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

# ------------------ USER HELP ------------------
def get_user(user_id, name):
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "name": name,
            "money": 1000,
            "kills": 0,
            "dead": False,
            "dead_until": 0,
            "protection_until": 0,
            "last_daily": 0
        }
    return data[uid]

def is_protected(user_data):
    return user_data.get("protection_until", 0) > time.time()

def format_time(sec):
    sec = int(sec)
    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60
    return f"{h}h {m}m {s}s"

# ------------------ DAILY COMMAND ------------------
async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_data()
    user = get_user(update.effective_user.id, update.effective_user.first_name)
    now = time.time()
    if now - user.get("last_daily", 0) < 86400:
        remain = 86400 - (now - user.get("last_daily", 0))
        await update.message.reply_text(f"⏳ Daily already claimed. Try after {format_time(remain)}")
        return
    user["money"] += 1500
    user["last_daily"] = now
    save_data()
    await update.message.reply_text("💰 Daily reward: ₹1500\nNext daily available after 24h")

# ------------------ BALANCE COMMAND ------------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_data()
    if update.message.reply_to_message:
        if update.message.reply_to_message.forward_from:
            target_user = update.message.reply_to_message.forward_from
        else:
            target_user = update.message.reply_to_message.from_user
    else:
        target_user = update.effective_user
    user_data = get_user(target_user.id, target_user.first_name)
    
    # Restore after 24h if robbed
    if str(target_user.id) in temp_rob:
        info = temp_rob[str(target_user.id)]
        if time.time() >= info["restore_time"]:
            user_data["money"] = info["original_balance"]
            del temp_rob[str(target_user.id)]
            save_data()

    sorted_users = sorted(data.items(), key=lambda x: x[1].get("money",0), reverse=True)
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
    load_data()
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
claimed_groups = set()
async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_data()
    chat = update.effective_chat
    user = update.effective_user
    if chat.type not in ["group","supergroup"]:
        await update.message.reply_text("❌ Works in groups only")
        return
    if chat.id in claimed_groups:
        await update.message.reply_text("⚠️ This group has already claimed rewards")
        return
    try:
        members_count = await chat.get_member_count()
    except:
        members_count = 0
    reward = 10000
    if members_count >= 500: reward=20000
    if members_count >= 1000: reward=30000
    user_data = get_user(user.id, user.first_name)
    user_data["money"] += reward
    save_data()
    claimed_groups.add(chat.id)
    await update.message.reply_text(f"💰 {user.first_name} claimed {reward} coins for this group!")


# ------------------ ROB COMMAND ------------------
async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_data()
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
    if robber_id in jail_users and now<jail_users[robber_id]:
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
    
    # Self/Owner/Bot checks
    if robber.id==victim.id:
        await update.message.reply_text("🤡 Khud ko rob nahi kar sakte!")
        return
    if victim.id==OWNER_ID:
        await update.message.reply_text("☠️ Owner ko rob nahi kar sakte.. ☠️")
        return
    if victim.is_bot:
        await update.message.reply_text("🤖 Bot ko rob nahi kar sakte!")
        return
    if is_protected(victim_data):
        await update.message.reply_text(f"🛡 {victim.first_name} abhi protected hai!")
        return
    if robber_id in rob_cooldown and now<rob_cooldown[robber_id]:
        await update.message.reply_text("⏱ Rob cooldown active! Wait 6 sec")
        return
    if victim_data["money"]<=0:
        await update.message.reply_text("Victim ke paas paisa nahi hai!")
        return
    if not context.args:
        stolen = min(100000, victim_data["money"])
    else:
        try:
            amount = int(context.args[0])
            if amount<=0: raise ValueError
            stolen = min(amount, victim_data["money"], 100000)
        except:
            await update.message.reply_text("Invalid amount!")
            return
    if victim.id not in temp_rob:
        temp_rob[victim.id] = {"original_balance": victim_data["money"], "restore_time": now+86400}
    # 30% chance police
    if random.random()<0.3:
        fine=300
        robber_data["money"]-=fine
        victim_data["money"]+=fine
        jail_users[robber_id]=now+180
        rob_cooldown[robber_id]=now+6
        save_data()
        await update.message.reply_text(
            f"🚔 Police ne pakad liya!\n"
            f"💸 ₹{fine} fine!\n"
            f"⛓ 3 min jail\n"
            f"💰 Robbery fail!\n"
        )
        return
    victim_data["money"]-=stolen
    robber_data["money"]+=stolen
    rob_cooldown[robber_id]=now+6
    save_data()
    await update.message.reply_text(
        f"👤 {robber.first_name} robbed ₹{stolen} from {victim.first_name}\n"
        f"💰 {victim.first_name}'s balance: ₹{victim_data['money']}\n"
        f"💰 {robber.first_name}'s balance: ₹{robber_data['money']}"
    )

# ------------------ KILL COMMAND ------------------
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_data()
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to someone to kill.")
        return
    killer = update.effective_user
    victim = update.message.reply_to_message.from_user
    now = time.time()
    killer_data = get_user(killer.id, killer.first_name)
    victim_data = get_user(victim.id, victim.first_name)
    # Auto revive
    if killer_data.get("dead",False):
        if now>=killer_data.get("dead_until",0):
            killer_data["dead"]=False
            killer_data["dead_until"]=0
            save_data()
        else:
            await update.message.reply_text("💀 Tum already dead ho! 24hr baad revive hoga 😢")
            return
    if victim_data.get("dead",False):
        if now>=victim_data.get("dead_until",0):
            victim_data["dead"]=False
            victim_data["dead_until"]=0
            save_data()
        else:
            await update.message.reply_text(
                "😂 Wow beta! Wo already dead hai ☠️\n"
                "Kisi aur ko try karo 😎"
            )
            return
    # Bot owner / self / bot checks
    if victim.id==OWNER_ID:
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
    if killer.id==victim.id:
        await update.message.reply_text("🤡 Khud ko kill nahi kar sakte!")
        return
    if is_protected(victim_data):
        await update.message.reply_text(f"🛡 {victim.first_name} abhi protected hai!")
        return
    if killer.id in kill_cooldown and now<kill_cooldown[killer.id]:
        await update.message.reply_text("⏳ Wait 6 seconds before killing again!")
        return
    # Kill victim
    victim_data["dead"]=True
    victim_data["dead_until"]=now+86400
    reward=random.randint(200,600)
    killer_data["money"]=killer_data.get("money",1000)+reward
    killer_data["kills"]=killer_data.get("kills",0)+1
    kill_cooldown[killer.id]=now+6
    save_data()
    await update.message.reply_text(
        f"☠️ {killer.first_name} killed {victim.first_name}!\n"
        f"💰 Earned: ₹{reward}\n"
        f"⏳ Victim 24hr baad revive hoga!\n"
    )

# ------------------ BAIL COMMAND ------------------
async def bail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_data()
    user = update.effective_user
    if user.id not in jail_users:
        await update.message.reply_text("😎 Tum jail me nahi ho!")
        return
    user_data = get_user(user.id, user.first_name)
    if user_data["money"]<1000:
        await update.message.reply_text("₹1000 chahiye bail ke liye!")
        return
    user_data["money"]-=1000
    del jail_users[user.id]
    save_data()
    await update.message.reply_text("💸 Bail mil gayi! Ab free ho 😈")



# ================= SHOP & GIFT COMMANDS (Part 1 JSON style) =================
import random
import json
import os
from telegram import Update
from telegram.ext import ContextTypes

# ---------------- DATA STORAGE ----------------
DATA_FILE = "database.json"

# Load main database
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

def save_data():
    global data
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user(user_id, name):
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "name": name,
            "money": 1000,
            "kills": 0,
            "dead": False,
            "dead_until": 0,
            "protection_until": 0,
            "last_daily": 0,
            "inventory": {}  # store shop items / gifts here
        }
        save_data()
    return data[uid]

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



import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8080035914:AAFYogx2dN-cbIPVNQfl9wgFAwpZ7d6Tvm4"

DATA_FILE = "database.json"

# ---------------- LOAD DATA ----------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

data = load_data()

# ---------------- SAVE DATA ----------------
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- GET USER ----------------
def get_user(user_id, first_name):
    uid = str(user_id)

    if uid not in data:
        data[uid] = {
            "name": first_name,
            "money": 1000,
            "inventory": {}
        }

    return data[uid]




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
    shop_items[gift_name]["gifs"].append(file_id)
    save_data()

    await update.message.reply_text(
        f"✅ GIF added to {gift_name}\nTotal GIFs: {len(shop_items[gift_name]['gifs'])}"
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
        "💰 *NIKI ECONOMY SYSTEM OVERVIEW*\n\n"
        "💬 *How it works:*\n"
        "Use Niki’s economy system to earn, manage, gift, and protect virtual money in your group.\n\n"
        "• /daily — Claim $1500 daily reward\n"
        "• /claim — Unlock group rewards based on members\n"
        "• /bal — Check your or another user’s balance\n"
        "• /rob (reply) <amount> — Rob money from a user\n"
        "• /kill (reply) — Kill a user & earn $200–$600\n"
        "• /revive — Revive yourself or a replied user\n"
        "• /protect 1d|2d|3d — Buy protection from robbery\n"
        "• /give (reply) <amount> — Transfer money\n"
        "• /shop — Shop for gift items\n"
        "• /items (reply) — View your/others inventory\n"
        "• /toprich — Top 10 richest users\n"
        "• /topkill — Top 10 killers\n"
        "• /check  — Check protection status (Costs $2000)\n"


    )

    # ✅ Send as Markdown for bold formatting
    await update.message.reply_text(text, parse_mode="Markdown")

# =================== REVIVE COMMAND ===================
import time
from telegram import Update
from telegram.ext import ContextTypes

async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from random import choice

    reviver = update.effective_user
    data = load_data()
    reviver_data = get_user(reviver.id, reviver.first_name)

    # Reply user
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        target_data = get_user(target_user.id, target_user.first_name)
    else:
        await update.message.reply_text("Reply karo jisko revive karna hai /revive command se 😅")
        return

    now = time.time()

    # ---------------- Case 1: Reviver is dead
    if reviver_data.get("dead", False):
        await update.message.reply_text("🤣 Arey rukja rukja beta tu abhi dead hai, tu khud ko revive mt kar sakta!")
        return

    # ---------------- Case 2: Target is alive
    if not target_data.get("dead", False):
        # Track how many times reviver tried reviving alive target
        if "revive_attempts" not in reviver_data:
            reviver_data["revive_attempts"] = {}
        attempts = reviver_data["revive_attempts"].get(str(target_user.id), 0)
        reviver_data["revive_attempts"][str(target_user.id)] = attempts + 1

        if attempts == 0:
            await update.message.reply_text(
                f"Arey rukja rukja beta {target_user.first_name} abhi jinda he 😅 abhi revive mt karo!"
            )
        elif attempts >= 1:
            # Deduct 500₹ from reviver
            reviver_data["money"] = reviver_data.get("money", 0) - 500
            save_data()

            # DM message to reviver
            try:
                await context.bot.send_message(
                    chat_id=reviver.id,
                    text="Apka bank account se 500 pesa kt ho chuka he... app glti kiye hamara bat nehi sune krupaya app hamar bat ko dhyaan me leke kam kare 🤣🤣"
                )
            except:
                pass  # if DM fails

            await update.message.reply_text(
                f"Yar tujhe bolatha mene 🤣 tu or ek bar revive mt kr ab tera 500 balance ktchuka he msg dekhlo dm me 🤣 aur balance check krlo"
            )
        save_data()
        return

    # ---------------- Case 3: Target is dead, proceed revive
    if target_data.get("dead", False):
        # Deduct 500₹ from reviver
        if reviver_data.get("money", 0) < 500:
            await update.message.reply_text("😢 Paisa kam hai, 500₹ chahiye revive ke liye!")
            return
        reviver_data["money"] -= 500
        target_data["dead"] = False
        target_data["dead_until"] = 0
        save_data()

        await update.message.reply_text(
            f"{reviver.first_name} ne {target_user.first_name} ko revive kiya! 🥰\n"
            f"Tujhe jinda kiya he ab friend ban ke sbka badla le jao ❤️😁\n"
            f"Protect lena mat bhulna!"
        )

        # DM message to revived user
        try:
            await context.bot.send_message(
                chat_id=target_user.id,
                text=f"{reviver.first_name} ne tujhe revive diya ab tu jinda ho gaya 😎💖\nProtect lena mat bhulna!"
            )
        except:
            pass

        # Optional: DM reviver to confirm 500₹ deducted
        try:
            await context.bot.send_message(
                chat_id=reviver.id,
                text="✅ 500₹ deduct hua revive ke liye. Balance check karlo!"
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
            f"🤫 Abey yar tu mera owner ka id dekhna chahega 🤔 nehi ye thik bat ni 😎\n"
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
    load_data()

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



from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8080035914:AAFYogx2dN-cbIPVNQfl9wgFAwpZ7d6Tvm4"

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

    app.add_handler(CommandHandler("own", own))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pack_name_handler))


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
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8080035914:AAFYogx2dN-cbIPVNQfl9wgFAwpZ7d6Tvm4"
CHAT_FILE = "chats.json"

# ---------------- LOAD CHATS ----------------
def load_chats():
    try:
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# ---------------- SAVE CHAT ----------------
def save_chat(chat_id):
    chats = load_chats()
    if str(chat_id) not in chats:
        chats.append(str(chat_id))
        with open(CHAT_FILE, "w") as f:
            json.dump(chats, f)

# ---------------- TRACK ALL CHATS ----------------
async def track_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_chat(chat_id)

# ---------------- BROADCAST ON START ----------------
async def broadcast_start(context: ContextTypes.DEFAULT_TYPE):
    chats = load_chats()

    message = (
        "Bot started\n"
        "Ab khelo maja lo or han ab top me jyada coin nehi he so jldi jldi top chale jao mere friends🙄🫢🫢"
    )

    for chat_id in chats:
        try:
            await context.bot.send_message(chat_id=int(chat_id), text=message)
        except:
            pass

#------------------GIVE-------------------------
async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a user to give money.")
        return

    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /give amount")
        return

    amount = int(context.args[0])

    sender_id = str(update.message.from_user.id)
    receiver_id = str(update.message.reply_to_message.from_user.id)

    if sender_id == receiver_id:
        await update.message.reply_text("❌ You cannot give money to yourself.")
        return

    data = load_data()

    if sender_id not in data:
        data[sender_id] = {"money": 0}

    if receiver_id not in data:
        data[receiver_id] = {"money": 0}

    if data[sender_id]["money"] < amount:
        await update.message.reply_text("❌ You don't have enough money.")
        return

    data[sender_id]["money"] -= amount
    data[receiver_id]["money"] += amount

    save_data(data)

    await update.message.reply_text(
        f"💸 {update.message.from_user.first_name} gave ${amount} to {update.message.reply_to_message.from_user.first_name}"
    )



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

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    giver = message.from_user
    data = load_data()

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

    # amount read
    text = message.text.split()

    if len(text) < 2:
        await message.reply_text("❌ Amount likho. Example: /give 500")
        return

    try:
        amount = int(text[1])
    except:
        await message.reply_text("❌ Invalid amount! Use numbers only.")
        return

    if amount <= 0:
        await message.reply_text("💸 Amount must be greater than 0!")
        return

    giver_data = get_user(giver.id, giver.first_name, data)
    receiver_data = get_user(receiver.id, receiver.first_name, data)

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

    save_data(data)

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

# =================== MAIN FUNCTION ===================
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("toprich", toprich))
    app.add_handler(CommandHandler("topkill", topkill))
    app.add_handler(CallbackQueryHandler(button_callback))
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
    app.add_handler(CommandHandler("help", economy_help))
    app.add_handler(CommandHandler("id", show_id))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("own", own))
    app.add_handler(CommandHandler("items", items))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("give", give))
# AUTO REPLY
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_niki_reply))
   

print("🔥 Niki Bot is running...")
app.run_polling()



