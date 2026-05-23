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
from telegram.ext import InlineQueryHandler
from openai import OpenAI
from telegram.constants import ChatAction
from datetime import datetime, timezone
from telegram import ChatPermissions
from telegram.helpers import mention_html
from telegram.ext import ChatJoinRequestHandler
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
import asyncio
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
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes

# =====================================================
# 💖 START COMMAND
# =====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    user = update.effective_user
    chat = update.effective_chat

    # ================= SAVE USER =================

    col.update_one(
        {"chat_id": chat.id},
        {"$set": {"chat_id": chat.id, "type": chat.type}},
        upsert=True
    )

    uid = str(user.id)

    if uid not in data:
        data[uid] = {
            "name": user.first_name,
            "money": 1000,
            "kills": 0
        }
        save_data()

    # ================= WELCOME =================

    welcome_text = (
        f"✨ Hᴇʏʏʏ {user.first_name}… ʏᴇs ʏᴏᴜ ᴄᴜᴛɪᴇ 😚✨\n\n"

        "<blockquote>"
        "❝ I’ᴍ Nɪᴋɪ — ʏᴏᴜʀ ᴄʜᴀᴏs ᴘᴀʀᴛɴᴇʀ & ғᴜɴ ᴅᴇᴀʟᴇʀ 💃🔥\n"
        "❝ Yᴏᴜʀ ᴀʟʟ-ɪɴ-ᴏɴᴇ ʙᴏᴛ 🤖💎\n"
        "❝ Mᴜsɪᴄ • Gᴀᴍᴇs • Aɪ Cʜᴀᴛ • Pʀᴏᴛᴇᴄᴛɪᴏɴ 🛡️\n"
        "❝ Wʜᴇʀᴇ ᴠɪʙᴇs ɢᴇᴛ ᴡɪʟᴅ ᴀɴᴅ ᴄʜᴀᴛs ɢᴇᴛ sᴘɪᴄʏ 🌶️😉"
        "</blockquote>\n\n"

        "✨🧸 <b>Nɪᴋɪ — Tʜᴇ Cᴜᴛᴇ Gɪʀʟ Bᴀʙʏ!</b> 🌸\n\n"

        "<blockquote>"
        "❝ 👀 <b>Sᴛᴏᴘ Sᴄʀᴏʟʟɪɴɢ…</b>\n"
        "❝ Sᴀᴄʜ ʙᴀᴛᴀᴏ… Gʀᴏᴜᴘ ᴍᴇ ʙᴏʀᴇ ʜᴏ ʀᴀʜᴇ ʜᴏ ɴᴀ? 😏\n\n"
        "</blockquote>\n\n"

        
        "❝Tᴏ ᴀᴀᴏ… ᴛʜᴏᴅᴀ sᴀ ғᴜɴ ᴋᴀʀᴛᴇ ʜᴀɪɴ 😈✨\n\n"
        

        
        "🎮 <b>Fᴇᴀᴛᴜʀᴇs:</b>\n"
        "<tg-spoiler>‣ Rᴘɢ: Sᴛᴀʙ = Kɪʟʟ, Sᴛᴇᴀʟ = Rᴏʙ, Pʀᴏᴛᴇᴄᴛ 🛡️</tg-spoiler>\n"
        "<tg-spoiler>‣ Sᴏᴄɪᴀʟ: Kɪss, Hᴜɢ, Sʟᴀᴘ, Kɪᴄᴋ, Pᴜɴᴄʜ 💋👊</tg-spoiler>\n"
        "<tg-spoiler>‣ Eᴄᴏɴᴏᴍʏ: Cʟᴀɪᴍ, Gɪᴠᴇ, Eᴀʀɴ & Fʟᴇx 💰</tg-spoiler>\n"
        "<tg-spoiler>‣ Mᴜsɪᴄ: Pʟᴀʏ, Vᴘʟᴀʏ, Sᴋɪᴘ, Sᴇᴇᴋ 🎶</tg-spoiler>\n"
        "<tg-spoiler>‣ Gᴀᴍᴇs: Dᴜᴇʟ, Dᴀʀᴛ, Mɪɴᴇs, Sʟᴏᴛ, Bᴏᴍʙ 🎲</tg-spoiler>\n\n"

        "😈 <b>Pᴏᴡᴇʀ sʜᴏᴡ ᴋᴀʀᴏ…</b>\n"
        "Fʀɪᴇɴᴅs ᴋᴏ ʟᴏᴏᴛᴏ, Tᴏᴘ ᴘᴇ ᴀᴀᴏ, ᴀᴜʀ ɢʀᴏᴜᴘ ᴍᴇ ᴅᴏᴍɪɴᴀᴛᴇ ᴋᴀʀᴏ 👑🔥\n\n"

        "🌸 <b>Wᴀʀɴɪɴɢ:</b>\n"
        "Eᴋ ʙᴀᴀʀ sᴛᴀʀᴛ ᴋɪʏᴀ… ᴛᴏ ᴀᴅᴅɪᴄᴛ ʜᴏ ᴊᴀᴏɢᴇ 😌💖"
    )

    # ================= BUTTONS =================

    keyboard = [

        [
            InlineKeyboardButton(
                "👑 𝐕ɪsʜᴀʟ ✘ 𝐃ᴇᴠɪʟ⚡",
                url="https://t.me/YTT_BISHAL"
            ),

            InlineKeyboardButton(
                "💖 𝐒𝐔𝐏𝐏𝐎𝐑𝐓",
                url="https://t.me/+EooSNZ9sR2AyZDlh"
            )
        ],

        [
            InlineKeyboardButton(
                "⚡ 𝐇𝐄𝐋𝐏 & 𝐂𝐌𝐃𝐒 ⚡",
                callback_data="help_cmds"
            )
        ],

        [
            InlineKeyboardButton(
                "🌸 𝐀𝐁𝐎𝐔𝐓",
                url="https://t.me/YTN_BISHAL"
            ),

            InlineKeyboardButton(
                "➕ 🗯️ 𝐊𝐈𝐃𝐍𝐀𝐏 𝐌𝐄 💌",
                url="https://t.me/iim_nikibot?startgroup=true"
            )
        ]
    ]

    # ================= BOT DP AUTO FETCH =================

    photos = await context.bot.get_user_profile_photos(
        context.bot.id,
        limit=1
    )

    bot_photo = None

    if photos.total_count > 0:
        bot_photo = photos.photos[0][-1].file_id

    # ================= SEND PHOTO =================

    await update.message.reply_photo(
        photo=bot_photo,
        caption=welcome_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =====================================================
# 🔘 BUTTON CALLBACK
# =====================================================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # =====================================================
    # ⚡ HELP MENU
    # =====================================================

    if data == "help_cmds":

        text = """
✨ <b>Nɪᴋɪ Hᴇʟᴘ & Cᴏᴍᴍᴀɴᴅs</b>

💖 Sᴇʟᴇᴄᴛ A Cᴀᴛᴇɢᴏʀʏ Bᴇʟᴏᴡ 😌
"""

        keyboard = [

            [
                InlineKeyboardButton(
                    "💰 𝐄𝐂𝐎𝐍𝐎𝐌𝐘",
                    callback_data="economy_menu"
                ),

                InlineKeyboardButton(
                    "🎮 𝐆𝐀𝐌𝐄𝐒",
                    callback_data="games_menu"
                )
            ],

            [
                InlineKeyboardButton(
                    "🎵 𝐌𝐔𝐒𝐈𝐂",
                    callback_data="music_menu"
                ),

                InlineKeyboardButton(
                    "🛠 𝐌𝐀𝐍𝐀𝐆𝐄𝐌𝐄𝐍𝐓",
                    callback_data="manage_menu"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏆 𝐑𝐄𝐖𝐀𝐑𝐃𝐒",
                    callback_data="reward_menu"
                ),

                InlineKeyboardButton(
                    "💞 𝐒𝐎𝐂𝐈𝐀𝐋",
                    callback_data="social_menu"
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 𝐇𝐎𝐌𝐄",
                    callback_data="home_menu"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # 💰 ECONOMY
    # =====================================================

    elif data == "economy_menu":

        text = """
👤 <b>Nᴏʀᴍᴀʟ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Oᴠᴇʀᴠɪᴇᴡ</b>

💬 <b>Hᴏᴡ Iᴛ Wᴏʀᴋꜱ:</b>
Uꜱᴇ Nɪᴋɪ’ꜱ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Tᴏ Eᴀʀɴ, Mᴀɴᴀɢᴇ, Gɪꜰᴛ, Aɴᴅ Pʀᴏᴛᴇᴄᴛ Vɪʀᴛᴜᴀʟ Mᴏɴᴇʏ 😌

• /daily — Cʟᴀɪᴍ $1500 Dᴀɪʟʏ Rᴇᴡᴀʀᴅ
• /claim — Uɴʟᴏᴄᴋ Gʀᴏᴜᴘ Rᴇᴡᴀʀᴅꜱ
• /bal — Cʜᴇᴄᴋ Bᴀʟᴀɴᴄᴇ
• /rob — Rᴏʙ Uᴘ Tᴏ $20000
• /kill — Eᴀʀɴ $200–$400
• /revive — Rᴇᴠɪᴠᴇ Uꜱᴇʀ
• /protect — Bᴜʏ Pʀᴏᴛᴇᴄᴛɪᴏɴ
• /give — Tʀᴀɴꜱꜰᴇʀ Mᴏɴᴇʏ
• /shop — Sʜᴏᴘ Iᴛᴇᴍꜱ
• /items — Vɪᴇᴡ Iɴᴠᴇɴᴛᴏʀʏ
• /toprich — Tᴏᴘ 10 Rɪᴄʜᴇꜱᴛ
• /topkill — Tᴏᴘ 10 Kɪʟʟᴇʀꜱ
• /check — Cʜᴇᴄᴋ Pʀᴏᴛᴇᴄᴛɪᴏɴ

━━━━━━━━━━━━━━━━━━━

💓 <b>Pʀᴇᴍɪᴜᴍ Eᴄᴏɴᴏᴍʏ</b>

• /daily — ₹5000 Dᴀɪʟʏ
• /rob — Bᴇᴛᴛᴇʀ Rᴏʙ
• /kill — Mᴏʀᴇ Rᴇᴡᴀʀᴅ
• /check — Fʀᴇᴇ Pʀᴏᴛᴇᴄᴛɪᴏɴ Cʜᴇᴄᴋ
• /bail — Pʀᴇᴍɪᴜᴍ Bᴀɪʟ
• ⚡ Fᴀsᴛᴇʀ Cᴏᴏʟᴅᴏᴡɴ
• 🚔 Lᴇss Jᴀɪʟ Tɪᴍᴇ
• 💓 Pʀᴇᴍɪᴜᴍ Bᴀᴅɢᴇ

💳 Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ → /pay
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 𝐁𝐀𝐂𝐊",
                    callback_data="help_cmds"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # 🎮 GAMES
    # =====================================================

    elif data == "games_menu":

        text = """
🎮 <b>𝐆𝐀𝐌𝐄𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒</b>

⚔ /duel → Fight Duel  
🃏 /cduel → Card Duel  
🎯 /dart → Throw Dart  
💣 /bomb → Bomb Game  
🔫 /gun → Russian Roulette  
🎰 /slot → Slot Machine  
💎 /mines → Mines Game  
🪙 /coin → Coin Flip  
🧠 /guess → Guess Number  
📝 /wordseek → Word Game  
🏆 /wordlb → Word Leaderboard  
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 𝐁𝐀𝐂𝐊",
                    callback_data="help_cmds"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # 🎵 MUSIC
    # =====================================================

    elif data == "music_menu":

        text = """
🎵 <b>𝐌𝐔𝐒𝐈𝐂 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒</b>

▶ /play → Play Song  
📺 /vplay → Video Play  
⏭ /skip → Skip Song  
⏹ /stop → Stop Music  
🔎 /seek → Seek Track  
🔁 /loop → Loop Music  
📜 /queue → Queue List  
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 𝐁𝐀𝐂𝐊",
                    callback_data="help_cmds"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # 🛠 MANAGEMENT
    # =====================================================

    elif data == "manage_menu":

        text = """
🛠 <b>𝐌𝐀𝐍𝐀𝐆𝐄𝐌𝐄𝐍𝐓 ⚡</b>

⛔ /ban – Ban User
✔ /unban – Unban User
🔇 /mute – Mute User
🔊 /unmute – Unmute User
⏳ /tmute – Temp Mute
🚫 /tban – Temp Ban
⭐ /promote – Promote User
📌 /pin – Pin Message
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 𝐁𝐀𝐂𝐊",
                    callback_data="help_cmds"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # 🏆 REWARDS
    # =====================================================

    elif data == "reward_menu":

        text = """
🏆 <b>𝐆𝐑𝐎𝐔𝐏 𝐑𝐄𝐖𝐀𝐑𝐃𝐒 💰</b>

👥 100+ → $10000
👥 500+ → $20000
👥 1000+ → $30000
👥 2000+ → $40000
👥 3000+ → $50000

⚠️ One Time Claim
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 𝐁𝐀𝐂𝐊",
                    callback_data="help_cmds"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # 💞 SOCIAL
    # =====================================================

    elif data == "social_menu":

        text = """
💞 <b>𝐒𝐎𝐂𝐈𝐀𝐋 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒</b>

💋 /kiss → Kiss Someone
🤗 /hug → Hug User
👋 /slap → Slap User
🦵 /kick → Kick Someone
👊 /punch → Punch User
🧸 /cuddle → Romantic Cuddle
👉 /poke → Poke User
😈 /bite → Bite Someone
😂 /tickle → Tickle User
❤️ /love → Love Meter

💍 /propose → Propose Someone
💕 /partner → Check Partner
👩‍❤️‍👨 /couple → Couple Profile
📜 /couplehistory → Love History
🏆 /coupleleaderboard → Top Couples
💔 /divorce → Break Relationship
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 𝐁𝐀𝐂𝐊",
                    callback_data="help_cmds"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # =====================================================
    # =====================================================
# =====================================================
    # 🏠 HOME MENU
    # =====================================================

    elif data == "home_menu":

        user = query.from_user

        welcome_text = (
            f"✨ Hᴇʏʏʏ {user.first_name}… ʏᴇs ʏᴏᴜ ᴄᴜᴛɪᴇ 😚✨\n\n"

            "<blockquote>"
            "I’ᴍ Nɪᴋɪ — ʏᴏᴜʀ ᴄʜᴀᴏs ᴘᴀʀᴛɴᴇʀ & ғᴜɴ ᴅᴇᴀʟᴇʀ 💃🔥\n"
            "Yᴏᴜʀ ᴀʟʟ-ɪɴ-ᴏɴᴇ ʙᴏᴛ 🤖💎\n"
            "Mᴜsɪᴄ • Gᴀᴍᴇs • Aɪ Cʜᴀᴛ • Pʀᴏᴛᴇᴄᴛɪᴏɴ 🛡️\n"
            "Wʜᴇʀᴇ ᴠɪʙᴇs ɢᴇᴛ ᴡɪʟᴅ ᴀɴᴅ ᴄʜᴀᴛs ɢᴇᴛ sᴘɪᴄʏ 🌶️😉"
            "</blockquote>\n\n"

            "✨🧸 <b>Nɪᴋɪ — Tʜᴇ Cᴜᴛᴇ Gɪʀʟ Bᴀʙʏ!</b> 🌸\n\n"

            "👀 <b>Sᴛᴏᴘ Sᴄʀᴏʟʟɪɴɢ…</b>\n"
            "Sᴀᴄʜ ʙᴀᴛᴀᴏ… Gʀᴏᴜᴘ ᴍᴇ ʙᴏʀᴇ ʜᴏ ʀᴀʜᴇ ʜᴏ ɴᴀ? 😏\n\n"

            "Tᴏ ᴀᴀᴏ… ᴛʜᴏᴅᴀ sᴀ ғᴜɴ ᴋᴀʀᴛᴇ ʜᴀɪɴ 😈✨\n\n"

            "🎮 <b>Fᴇᴀᴛᴜʀᴇs:</b>\n"
            "<tg-spoiler>‣ Rᴘɢ: Sᴛᴀʙ = Kɪʟʟ, Sᴛᴇᴀʟ = Rᴏʙ, Pʀᴏᴛᴇᴄᴛ 🛡️</tg-spoiler>\n"
            "<tg-spoiler>‣ Sᴏᴄɪᴀʟ: Kɪss, Hᴜɢ, Sʟᴀᴘ, Kɪᴄᴋ, Pᴜɴᴄʜ 💋👊</tg-spoiler>\n"
            "<tg-spoiler>‣ Eᴄᴏɴᴏᴍʏ: Cʟᴀɪᴍ, Gɪᴠᴇ, Eᴀʀɴ & Fʟᴇx 💰</tg-spoiler>\n"
            "<tg-spoiler>‣ Mᴜsɪᴄ: Pʟᴀʏ, Vᴘʟᴀʏ, Sᴋɪᴘ, Sᴇᴇᴋ 🎶</tg-spoiler>\n"
            "<tg-spoiler>‣ Gᴀᴍᴇs: Dᴜᴇʟ, Dᴀʀᴛ, Mɪɴᴇs, Sʟᴏᴛ, Bᴏᴍʙ 🎲</tg-spoiler>\n\n"

            "😈 <b>Pᴏᴡᴇʀ sʜᴏᴡ ᴋᴀʀᴏ…</b>\n"
            "Fʀɪᴇɴᴅs ᴋᴏ ʟᴏᴏᴛᴏ, Tᴏᴘ ᴘᴇ ᴀᴀᴏ, ᴀᴜʀ ɢʀᴏᴜᴘ ᴍᴇ ᴅᴏᴍɪɴᴀᴛᴇ ᴋᴀʀᴏ 👑🔥\n\n"

            "🌸 <b>Wᴀʀɴɪɴɢ:</b>\n"
            "Eᴋ ʙᴀᴀʀ sᴛᴀʀᴛ ᴋɪʏᴀ… ᴛᴏ ᴀᴅᴅɪᴄᴛ ʜᴏ ᴊᴀᴏɢᴇ 😌💖"
        )

        keyboard = [

            [
                InlineKeyboardButton(
                    "👑 𝐕ɪsʜᴀʟ ✘ 𝐃ᴇᴠɪʟ⚡",
                    url="https://t.me/YTT_BISHAL"
                ),

                InlineKeyboardButton(
                    "💖 𝐒𝐔𝐏𝐏𝐎𝐑𝐓",
                    url="https://t.me/+EooSNZ9sR2AyZDlh"
                )
            ],

            [
                InlineKeyboardButton(
                    "⚡ 𝐇𝐄𝐋𝐏 & 𝐂𝐌𝐃𝐒 ⚡",
                    callback_data="help_cmds"
                )
            ],

            [
                InlineKeyboardButton(
                    "🌸 𝐀𝐁𝐎𝐔𝐓",
                    url="https://t.me/YTN_BISHAL"
                ),

                InlineKeyboardButton(
                    "➕ 🗯️ 𝐊𝐈𝐃𝐍𝐀𝐏 𝐌𝐄 💌",
                    url="https://t.me/iim_nikibot?startgroup=true"
                )
            ]
        ]

        await query.edit_message_caption(
            caption=welcome_text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
# =================== TOP RICHEST COMMAND ===================

async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    users_only = {
        uid: u for uid, u in data.items()
        if isinstance(u, dict) and "money" in u
    }

    if not users_only:

        await update.message.reply_text(
            "❌ Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ!"
        )
        return

    sorted_rich = sorted(
        users_only.items(),
        key=lambda x: x[1]["money"],
        reverse=True
    )[:10]

    msg = (
        "╔═══━━━─── • ───━━━═══╗\n"
        "     💰 𝐓𝐎𝐏 𝐑𝐈𝐂𝐇 💰\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"
    )

    for idx, (uid, user) in enumerate(sorted_rich, 1):

        badge = "💓" if user.get("premium", False) else "👤"

        msg += (
            f"{idx}. {badge} "
            f"{user.get('name', 'Unknown')} "
            f"➜ ₹{user.get('money', 0)}\n"
        )

    msg += (
        "\n━━━━━━━━━━━━━━━━━━\n"
        "💖 Rɪᴄʜᴇꜱᴛ Pʟᴀʏᴇʀꜱ Oғ Nɪᴋɪ 😈\n\n"
        "💓 Premium User\n"
        "👤 Normal User"
    )

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

        await update.message.reply_text(
            "❌ Nᴏ Dᴀᴛᴀ Fᴏᴜɴᴅ!"
        )
        return

    sorted_kills = sorted(
        users_only.items(),
        key=lambda x: x[1]["kills"],
        reverse=True
    )[:10]

    msg = (
        "╔═══━━━─── • ───━━━═══╗\n"
        "    ⚔ 𝐓𝐎𝐏 𝐊𝐈𝐋𝐋 ⚔\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"
    )

    for idx, (uid, user) in enumerate(sorted_kills, 1):

        badge = "💓" if user.get("premium", False) else "👤"

        msg += (
            f"{idx}. {badge} "
            f"{user.get('name', 'Unknown')} "
            f"➜ {user.get('kills', 0)} Kɪʟʟꜱ\n"
        )

    msg += (
        "\n━━━━━━━━━━━━━━━━━━\n"
        "☠️ Dᴇᴀᴅʟɪᴇꜱᴛ Pʟᴀʏᴇʀꜱ Oғ Nɪᴋɪ 🔥\n\n"
        "💓 Premium User\n"
        "👤 Normal User"
    )

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

    # 🔥 CLEAN DATA
    safe_data = {}

    for k, v in data.items():
        if isinstance(v, (dict, list, str, int, float, bool)):
            safe_data[k] = v

    # 💖 JSON SAVE
    with open(DATA_FILE, "w") as f:
        json.dump(safe_data, f, indent=2, default=lambda o: None)
    # 💖 MONGO SAVE
    backup.update_one(
        {"_id": "main_data"},
        {"$set": {"data": json.loads(json.dumps(safe_data, default=lambda o: None))}},
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

import time
import random

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import ContextTypes

pending_daily = {}

# ==================================================
# 💰 DAILY COMMAND
# ==================================================

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user = update.effective_user
    user_data = get_user(user.id, user.first_name)

    now = time.time()

    # ==================================================
    # 💓 GROUP → DM REDIRECT
    # ==================================================

    if update.effective_chat.type != "private":

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🚀 Start Daily In DM",
                    url=f"https://t.me/{context.bot.username}?start=daily"
                )
            ]
        ])

        await update.message.reply_text(
            "💓 Dᴀɪʟʏ Rᴇᴡᴀʀᴅ Oɴʟʏ Iɴ DM 😏\n"
            "👉 Start bot in private chat to claim reward",
            reply_markup=keyboard
        )
        return

    # ==================================================
    # ⏳ COOLDOWN
    # ==================================================

    if now - user_data.get("last_daily", 0) < 86400:

        remain = 86400 - (
            now - user_data.get("last_daily", 0)
        )

        await update.message.reply_text(
            f"⏳ Aʟʀᴇᴀᴅʏ Cʟᴀɪᴍᴇᴅ!\n"
            f"🕒 Tʀʏ Aғᴛᴇʀ {format_time(remain)}"
        )
        return

    # ==================================================
    # 💎 PREMIUM USER
    # ==================================================

    if user_data.get("premium", False):

        reward = 5000

        # ✅ DIRECT BALANCE ADD
        user_data["money"] = (
            user_data.get("money", 0)
            + reward
        )

        user_data["last_daily"] = time.time()

        save_data()

        await update.message.reply_text(
            "╔═══━━━─── • ───━━━═══╗\n"
            "      💎 𝐏ʀᴇᴍɪᴜᴍ 𝐃ᴀɪʟʏ 💎\n"
            "╚═══━━━─── • ───━━━═══╝\n\n"

            "✨ 𝐏ʀᴇᴍɪᴜᴍ 𝐔sᴇʀ 𝐃ᴇᴛᴇᴄᴛᴇᴅ 😈\n\n"

            f"💰 ₹{reward} 𝐀ᴅᴅᴇᴅ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐁ᴀʟᴀɴᴄᴇ\n\n"

            f"🏦 𝐍ᴇᴡ 𝐁ᴀʟᴀɴᴄᴇ: ₹{user_data['money']}\n\n"

            "⚡ Nᴏ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ RᴇQᴜɪʀᴇᴅ\n"
            "🔥 Fᴀsᴛ Pʀᴇᴍɪᴜᴍ Cʟᴀɪᴍ Sᴜᴄᴄᴇss"
        )

        return
# ==================================================
    # 🤖 NORMAL USER CAPTCHA
    # ==================================================

    pending_daily[user.id] = {
        "time": now
    }

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🤖 I Aᴍ Nᴏᴛ Rᴏʙᴏᴛ",
                callback_data=f"daily_verify_{user.id}"
            )
        ],

        [
            InlineKeyboardButton(
                "💖 Cʟɪᴄᴋ Tᴏ Eɴᴛᴇʀ Nɪᴋɪ Wᴏʀʟᴅ",
                url="https://t.me/YTN_BISHAL"
            )
        ]

    ])

    await update.message.reply_text(
        "╔═══━━━─── • ───━━━═══╗\n"
        "      🎁 𝐃ᴀɪʟʏ 𝐑ᴇᴡᴀʀᴅ 🎁\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"

        "🤖 𝐂ᴏᴍᴘʟᴇᴛᴇ 𝐕ᴇʀɪғɪᴄᴀᴛɪᴏɴ\n"
        "💓 𝐓ᴏ 𝐂ʟᴀɪᴍ 𝐘ᴏᴜʀ 𝐃ᴀɪʟʏ\n\n"

        "✨ 𝐂ʟɪᴄᴋ 𝐓ʜᴇ 𝐁ᴜᴛᴛᴏɴ𝐬 𝐁ᴇʟᴏᴡ 😈\n\n"

        "💡 𝐇ɪɢʜᴇʀ 𝐃ᴀɪʟʏ?\n"
        "👉 Use /pay To Unlock Premium 💎",

        reply_markup=keyboard
    )


# ==================================================
# 🤖 DAILY VERIFY CALLBACK
# ==================================================

async def daily_verify(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    # ==================================================
    # ❌ NO PENDING
    # ==================================================

    if user.id not in pending_daily:

        return await query.answer(
            "❌ Nᴏ Pᴇɴᴅɪɴɢ Dᴀɪʟʏ",
            show_alert=True
        )

    user_data = get_user(
        user.id,
        user.first_name
    )

    reward = 1500

    # ==================================================
    # 💰 ADD MONEY
    # ==================================================

    user_data["money"] = (
        user_data.get("money", 0)
        + reward
    )

    user_data["last_daily"] = time.time()

    save_data()

    del pending_daily[user.id]

    # ==================================================
    # ✅ SUCCESS
    # ==================================================

    await query.edit_message_text(

        "╔═══━━━─── • ───━━━═══╗\n"
        "      💰 𝐃ᴀɪʟʏ 𝐒ᴜᴄᴄᴇss 💰\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"

        "🎉 𝐕ᴇʀɪғɪᴄᴀᴛɪᴏɴ 𝐂ᴏᴍᴘʟᴇᴛᴇ𝐃\n\n"

        f"💸 ₹{reward} 𝐀ᴅᴅᴇᴅ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐁ᴀʟᴀɴᴄᴇ\n\n"

        f"🏦 𝐍ᴇᴡ 𝐁ᴀʟᴀɴᴄᴇ: ₹{user_data['money']}\n\n"

        "💎 𝐖ᴀɴᴛ 𝐌ᴏʀᴇ 𝐃ᴀɪʟʏ?\n"
        "👉 Upgrade To Premium Using /pay 😈"
    
        "💓 Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ Fᴏʀ Hɪɢʜᴇʀ Dᴀɪʟʏ Rᴇᴡᴀʀᴅ Aɴᴅ Sᴋɪᴘ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ → /pay\n"
        
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

    badge = get_badge(user_data)

    await update.message.reply_text(
        f"┏━━━ 💼 PROFILE ━━━\n"
        f"{badge} Name  : {target_user.first_name}\n"
        f"💰 Bal    : ₹{user_data.get('money',0)}\n"
        f"🏆 Rank   : {rank}\n"
        f"❤️ Status : {status_text}\n"
        f"⚔ Kills  : {user_data.get('kills',0)}\n"
        f"┗━━━━━━━━━━━━━━━"
    )
# ------------------ PROTECT COMMAND ------------------
# ------------------ PROTECT COMMAND ------------------

# ------------------ PROTECT COMMAND ------------------

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    user = get_user(
        update.effective_user.id,
        update.effective_user.first_name
    )

    now = time.time()

    # ==================================================
    # 💎 PROTECTION PLANS
    # ==================================================

    cost_map = {
        "1d": (800, 86400),
        "2d": (1000, 172800),
        "3d": (2000, 259200)
    }

    # ---------------- NO ARG ----------------

    if not context.args:

        await update.message.reply_text(
            "👑 Vɪꜱʜᴀʟ Bᴏꜱꜱ Kᴀ Hᴜᴋᴜᴍ 😎🔥\n\n"
            "/protect 1d → ₹800\n"
            "/protect 2d → ₹1000\n"
            "/protect 3d → ₹2000\n\n"
            "💓 Pʀᴇᴍɪᴜᴍ Uꜱᴇʀꜱ Cᴀɴ Uꜱᴇ 2ᴅ & 3ᴅ"
        )
        return

    choice = context.args[0].lower()

    # ---------------- INVALID ----------------

    if choice not in cost_map:

        await update.message.reply_text(
            "❌ Iɴᴠᴀʟɪᴅ Oᴘᴛɪᴏɴ.\n"
            "Uꜱᴇ: 1ᴅ / 2ᴅ / 3ᴅ"
        )
        return

    # ---------------- PREMIUM CHECK ----------------

    if not user.get("premium", False):

        if choice in ["2d", "3d"]:

            await update.message.reply_text(
                "❗ Nᴏʀᴍᴀʟ Uꜱᴇʀꜱ Cᴀɴ Oɴʟʏ Uꜱᴇ: 1ᴅ\n"
                "💓 Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ → /pay"
            )
            return

    # ---------------- COST ----------------

    cost, duration = cost_map[choice]

    # ---------------- ALREADY PROTECTED ----------------

    if user.get("protection_until", 0) > now:

        rem = user["protection_until"] - now

        await update.message.reply_text(
            f"🛡 Aʟʀᴇᴀᴅʏ Pʀᴏᴛᴇᴄᴛᴇᴅ.\n"
            f"⏳ {format_time(rem)} Rᴇᴍᴀɪɴɪɴɢ"
        )
        return

    # ---------------- MONEY CHECK ----------------

    if user["money"] < cost:

        await update.message.reply_text(
            "💸 Pᴀɪꜱᴀ Kᴀᴍ Hᴀɪ."
        )
        return

    # ---------------- APPLY ----------------

    user["money"] -= cost

    user["protection_until"] = now + duration

    save_data()

    # ---------------- SUCCESS ----------------

    if user.get("premium", False):

        await update.message.reply_text(
            f"💓 Pʀᴇᴍɪᴜᴍ Pʀᴏᴛᴇᴄᴛɪᴏɴ Aᴄᴛɪᴠᴇᴅ.\n"
            f"🛡️ Yᴏᴜ Aʀᴇ Pʀᴏᴛᴇᴄᴛᴇᴅ Fᴏʀ {choice}."
        )

    else:

        await update.message.reply_text(
            f"🛡️ Yᴏᴜ Aʀᴇ Nᴏᴡ Pʀᴏᴛᴇᴄᴛᴇᴅ Fᴏʀ {choice}."
        )

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

    # 🚔 POLICE CHANCE
    if random.random() < 0.3:

        fine = 300

        robber_badge = "💓" if robber_data.get("premium", False) else "👤"

        # 💓 PREMIUM USER
        if robber_data.get("premium", False):

            jail_time = 60

            status_text = "\n💎 Sᴛᴀᴛᴜꜱ : Pʀᴇᴍɪᴜᴍ Uꜱᴇʀ"

            bail_text = "\n🔓 Bᴀɪʟ Aᴠᴀɪʟᴀʙʟᴇ Fᴏʀ Pʀᴇᴍɪᴜᴍ Uꜱᴇʀ"

        # 👤 NORMAL USER
        else:

            jail_time = 180

            status_text = ""

            bail_text = ""

        robber_data["money"] -= fine

        victim_data["money"] += fine

        jail_users[robber_id] = now + jail_time

        rob_cooldown[robber_id] = now + 6

        save_data()

        await update.message.reply_text(
            f"🚔 {robber_badge} Police ne pakad liya!\n"
            f"💸 ₹{fine} fine!\n"
            f"⛓ {jail_time // 60} min jail\n"
            f"💰 Robbery fail!"
            f"{status_text}"
            f"{bail_text}"
        )

        return

    # 💓 PREMIUM LIMIT
    if robber_data.get("premium", False):

        max_rob = 100000

        robber_badge = "💓"

        premium_text = "\n💎 Sᴛᴀᴛᴜꜱ : Pʀᴇᴍɪᴜᴍ Rᴏʙ"

    # 👤 NORMAL USER
    else:

        max_rob = 20000

        robber_badge = "👤"

        premium_text = ""

    stolen = min(
        amount,
        victim_data["money"],
        max_rob
    )

    # 💖 SUCCESSFUL ROB
    victim_data["money"] -= stolen

    robber_data["money"] += stolen

    rob_cooldown[robber_id] = now + 6

    save_data()

    try:

        await update.message.reply_text(
            f"💰 {robber_badge} {robber.first_name} "
            f"robbed ₹{stolen} from {victim.first_name}\n"
            f"🏦 {victim.first_name} Balance : ₹{victim_data['money']}\n"
            f"💵 {robber.first_name} Balance : ₹{robber_data['money']}"
            f"{premium_text}"
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

    # 💓 PREMIUM USER
    if killer_data.get("premium", False):

        reward = random.randint(400, 600)

        killer_badge = "💓"

        premium_text = "\n💎 Sᴛᴀᴛᴜꜱ : Pʀᴇᴍɪᴜᴍ Kɪʟʟ"

    # 👤 NORMAL USER
    else:

        reward = random.randint(200, 400)

        killer_badge = "👤"

        premium_text = ""

    killer_data["money"] = (
        killer_data.get("money", 1000)
        + reward
    )

    killer_data["kills"] = (
        killer_data.get("kills", 0)
        + 1
    )

    # 💖 COOLDOWN + SAVE
    kill_cooldown[str(killer.id)] = now + 6

    save_data()

    # 💖 FINAL MESSAGE
    try:

        await update.message.reply_text(
            f"☠️ {killer_badge} {killer.first_name} "
            f"killed {victim.first_name}!\n"
            f"💰 Earned: ₹{reward}\n"
            f"⏳ Victim 24hr baad revive hoga!"
            f"{premium_text}"
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

    user_data = get_user(
        user.id,
        user.first_name
    )

    # 💓 PREMIUM CHECK
    if not user_data.get("premium", False):

        await update.message.reply_text(
            "💓 Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Iꜱ Oɴʟʏ Fᴏʀ Pʀᴇᴍɪᴜᴍ Uꜱᴇʀꜱ.\n"
            "🛒 Bᴜʏ Pʀᴇᴍɪᴜᴍ Uꜱɪɴɢ → /pay"
        )
        return

    # ❌ NOT IN JAIL
    if user_id not in jail_users:

        await update.message.reply_text(
            "😎 Tᴜᴍ Jᴀɪʟ Mᴇ Nᴀʜɪ Hᴏ!"
        )
        return

    # ✅ AUTO FREE
    if now >= jail_users[user_id]:

        del jail_users[user_id]

        save_data()

        await update.message.reply_text(
            "😎 Tᴜᴍ Aʟʀᴇᴀᴅʏ Fʀᴇᴇ Hᴏ!"
        )
        return

    # 💸 NOT ENOUGH MONEY
    if user_data["money"] < 1000:

        await update.message.reply_text(
            "💸 ₹1000 Cʜᴀʜɪʏᴇ Bᴀɪʟ Kᴇ Lɪʏᴇ!"
        )
        return

    # 💰 DEDUCT MONEY
    user_data["money"] -= 1000

    # 🔓 REMOVE JAIL
    del jail_users[user_id]

    save_data()

    # 💖 FINAL MESSAGE
    await update.message.reply_text(
        "🔓 💓 Pʀᴇᴍɪᴜᴍ Bᴀɪʟ Aᴄᴛɪᴠᴇᴅ!\n"
        "💸 ₹1000 Dᴇᴅᴜᴄᴛᴇᴅ\n"
        "😈 Aʙ Tᴜᴍ Fʀᴇᴇ Hᴏ!"
    )


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

    user_data = get_user(
        update.effective_user.id,
        update.effective_user.first_name
    )

    # 💓 PREMIUM USER
    if user_data.get("premium", False):

        text = (
            "💓 *Pʀᴇᴍɪᴜᴍ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Oᴠᴇʀᴠɪᴇᴡ*\n\n"

            "💬 *Hᴏᴡ Iᴛ Wᴏʀᴋꜱ:*\n"
            "Uꜱᴇ Nɪᴋɪ’ꜱ Pʀᴇᴍɪᴜᴍ Eᴄᴏɴᴏᴍʏ Tᴏ Gᴇᴛ Hɪɢʜᴇʀ Rᴇᴡᴀʀᴅꜱ, "
            "Pʀᴇᴍɪᴜᴍ Bᴇɴᴇꜰɪᴛꜱ, Aɴᴅ Sᴘᴇᴄɪᴀʟ Fᴇᴀᴛᴜʀᴇꜱ 😏💓\n\n"

            "• /daily — Cʟᴀɪᴍ $5000 Dᴀɪʟʏ Rᴇᴡᴀʀᴅ\n"
            "• /claim — Uɴʟᴏᴄᴋ Gʀᴏᴜᴘ Rᴇᴡᴀʀᴅꜱ Bᴀꜱᴇᴅ Oɴ Mᴇᴍʙᴇʀꜱ\n"
            "• /bal — Cʜᴇᴄᴋ Yᴏᴜʀ Oʀ Aɴᴏᴛʜᴇʀ Uꜱᴇʀ’ꜱ Bᴀʟᴀɴᴄᴇ\n"
            "• /rob (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Rᴏʙ Uᴘ Tᴏ $100000\n"
            "• /kill (ʀᴇᴘʟʏ) — Eᴀʀɴ $400–$600\n"
            "• /revive — Rᴇᴠɪᴠᴇ Yᴏᴜʀꜱᴇʟꜰ Oʀ A Rᴇᴘʟɪᴇᴅ Uꜱᴇʀ\n"
            "• /protect 1ᴅ|2ᴅ|3ᴅ — Bᴜʏ Pʀᴏᴛᴇᴄᴛɪᴏɴ\n"
            "• /check — Fʀᴇᴇ Pʀᴏᴛᴇᴄᴛɪᴏɴ Cʜᴇᴄᴋ\n"
            "• /bail — Gᴇᴛ Oᴜᴛ Oꜰ Jᴀɪʟ\n"
            "• /give (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Tʀᴀɴꜱꜰᴇʀ Mᴏɴᴇʏ\n"
            "• /shop — Sʜᴏᴘ Fᴏʀ Gɪꜰᴛ Iᴛᴇᴍꜱ\n"
            "• /items (ʀᴇᴘʟʏ) — Vɪᴇᴡ Iɴᴠᴇɴᴛᴏʀʏ\n"
            "• /toprich — Tᴏᴘ 10 Rɪᴄʜᴇꜱᴛ Uꜱᴇʀꜱ\n"
            "• /topkill — Tᴏᴘ 10 Kɪʟʟᴇʀꜱ\n"
        )

    # 👤 NORMAL USER
    else:

        text = (
            "👤 *Nᴏʀᴍᴀʟ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Oᴠᴇʀᴠɪᴇᴡ*\n\n"

            "💬 *Hᴏᴡ Iᴛ Wᴏʀᴋꜱ:*\n"
            "Uꜱᴇ Nɪᴋɪ’ꜱ Eᴄᴏɴᴏᴍʏ Sʏꜱᴛᴇᴍ Tᴏ Eᴀʀɴ, Mᴀɴᴀɢᴇ, "
            "Gɪꜰᴛ, Aɴᴅ Pʀᴏᴛᴇᴄᴛ Vɪʀᴛᴜᴀʟ Mᴏɴᴇʏ 😌\n\n"

            "• /daily — Cʟᴀɪᴍ $1500 Dᴀɪʟʏ Rᴇᴡᴀʀᴅ\n"
            "• /claim — Uɴʟᴏᴄᴋ Gʀᴏᴜᴘ Rᴇᴡᴀʀᴅꜱ Bᴀꜱᴇᴅ Oɴ Mᴇᴍʙᴇʀꜱ\n"
            "• /bal — Cʜᴇᴄᴋ Yᴏᴜʀ Oʀ Aɴᴏᴛʜᴇʀ Uꜱᴇʀ’ꜱ Bᴀʟᴀɴᴄᴇ\n"
            "• /rob (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Rᴏʙ Uᴘ Tᴏ $20000\n"
            "• /kill (ʀᴇᴘʟʏ) — Eᴀʀɴ $200–$400\n"
            "• /revive — Rᴇᴠɪᴠᴇ Yᴏᴜʀꜱᴇʟꜰ Oʀ A Rᴇᴘʟɪᴇᴅ Uꜱᴇʀ\n"
            "• /protect 1ᴅ — Bᴜʏ Pʀᴏᴛᴇᴄᴛɪᴏɴ\n"
            "• /give (ʀᴇᴘʟʏ) <ᴀᴍᴏᴜɴᴛ> — Tʀᴀɴꜱꜰᴇʀ Mᴏɴᴇʏ\n"
            "• /shop — Sʜᴏᴘ Fᴏʀ Gɪꜰᴛ Iᴛᴇᴍꜱ\n"
            "• /items (ʀᴇᴘʟʏ) — Vɪᴇᴡ Iɴᴠᴇɴᴛᴏʀʏ\n"
            "• /toprich — Tᴏᴘ 10 Rɪᴄʜᴇꜱᴛ Uꜱᴇʀꜱ\n"
            "• /topkill — Tᴏᴘ 10 Kɪʟʟᴇʀꜱ\n\n"

            "💓 Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ → /pay"
        )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )

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

OWNER_ID = 6175559434
OWNER_USERNAME = "YTT_BISHAL"

async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    # 💖 TARGET USER
    if update.message.reply_to_message:

        target_user = update.message.reply_to_message.from_user

    else:

        target_user = update.effective_user

    # 💖 OWNER PROTECTION
    if target_user.id == OWNER_ID:

        await update.message.reply_text(
            f"🤔 Aʙᴇʏ Yᴀʀ Tᴜ Mᴇʀᴇ Oᴡɴᴇʀ Kᴀ Iᴅ Dᴇᴋʜɴᴀ Cʜᴀʜᴇɢᴀ 😎\n"
            f"📝 Oᴡɴᴇʀ Kᴀ Iᴅ Sᴇᴄʀᴇᴛ Hᴀɪ 👉 @{OWNER_USERNAME}"
        )
        return

    # 💖 USER DATA
    user_data = get_user(
        target_user.id,
        target_user.first_name
    )

    # 💖 BADGE
    badge = get_badge(user_data)

    # 💖 IDS
    chat_id = update.effective_chat.id

    user_id = target_user.id

    username = (
        target_user.username
        or target_user.first_name
    )

    # 💖 FINAL MESSAGE
    msg = (
        f"👤 Uꜱᴇʀ Nᴀᴍᴇ : {badge} {username}\n"
        f"🆔 Uꜱᴇʀ Iᴅ : {user_id}\n"
        f"💬 Cʜᴀᴛ Iᴅ : {chat_id}"
    )

    await update.message.reply_text(msg)




# ---------------- CHECK COMMAND FINAL ----------------
# ================= CHECK COMMAND PREMIUM FINAL =================

import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ==================================================
# 💓 BADGE SYSTEM
# ==================================================

def get_badge(user_data):
    return "💓" if user_data.get("premium") else "👤"


# ==================================================
# 💓 /CHECK COMMAND (FULL UPGRADE)
# ==================================================

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    checker = update.effective_user
    checker_data = get_user(checker.id, checker.first_name)

    # 💓 PREMIUM ONLY
    if not checker_data.get("premium"):
        await update.message.reply_text(
            "💓 Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Iꜱ Oɴʟʏ Fᴏʀ Pʀᴇᴍɪᴜᴍ Uꜱᴇʀꜱ.\n"
            "Bᴜʏ → /pay"
        )
        return

    # ==================================================
    # 🎯 TARGET PARSE (@username / reply / id)
    # ==================================================

    target = None

    # 1️⃣ Reply
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user

    # 2️⃣ @username or ID
    elif context.args:
        query = context.args[0]

        # try username
        if query.startswith("@"):
            username = query.replace("@", "")
            # simple scan (anti-fake safe)
            for uid, u in data.items():
                if isinstance(u, dict) and u.get("username") == username:
                    target = type("obj", (), {
                        "id": uid,
                        "first_name": u.get("name", "User"),
                        "username": username
                    })()
                    break

        # try ID
        elif query.isdigit():
            u = get_user(query, "User")
            target = type("obj", (), {
                "id": query,
                "first_name": u.get("name", "User"),
                "username": None
            })()

    if not target:
        await update.message.reply_text(
            "⚠️ Uꜱᴀɢᴇ:\n"
            "/check reply\n"
            "/check @username\n"
            "/check user_id"
        )
        return

    target_data = get_user(target.id, target.first_name)

    # ==================================================
    # 🛡 PROTECTION STATUS
    # ==================================================

    now = time.time()
    protection_until = target_data.get("protection_until", 0)

    if protection_until > now:
        rem = int(protection_until - now)
        status = f"🛡 Aᴄᴛɪᴠᴇ ({rem//3600}h {rem%3600//60}m)"
    else:
        status = "❌ Nᴏ Pʀᴏᴛᴇᴄᴛɪᴏɴ"

    badge = get_badge(target_data)

    # ==================================================
    # 🎯 INLINE RESULT (NO DM)
    # ==================================================

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💓 Premium Upgrade",
                url="https://t.me/YTT_BISHAL"
            )
        ]
    ])

    await update.message.reply_text(
        f"💓 Pʀᴏᴛᴇᴄᴛɪᴏɴ Cʜᴇᴄᴋ\n\n"
        f"{badge} 👤 Uꜱᴇʀ: {target.first_name}\n"
        f"{status}\n\n"
        f"⚡ Checked by {checker.first_name}",
        reply_markup=keyboard
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
    # ❌ BOT CHECK
    if receiver.is_bot:
        await message.reply_text(
            "🤖 Bots ko paisa transfer nahi kar sakte 😏"
        )
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
        [InlineKeyboardButton("🌸 Start Me", url=f"https://t.me/iim_nikibot")]
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

    import asyncio, random
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    user = update.effective_user
    user_id = str(user.id)
    mention = f"<a href='tg://user?id={user_id}'>{user.first_name}</a>"

    chat = update.effective_chat

    # 🚫 GROUP CHECK + BUTTON
    if chat.type != "private":

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "💌 Start Magic in DM ✨",
                url="https://t.me/iim_nikibot?start=magic"
            )]
        ])

        await update.message.reply_text(
            "⚠️ <b>This command only works in DM (Private Chat)</b>\n\n"
            "💻 Magic system is not allowed in groups!\n\n"
            "👇 Click below to start magic in DM ✨",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        return

    msg = await update.message.reply_text("💻 Initializing hack...")

    steps = [
        "🔍 Scanning system...",
        "💣 Breaking firewall...",
        "📡 Accessing root...",
        "💰 Opening vault..."
    ]

    for step in steps:
        await asyncio.sleep(1.2)
        try:
            await msg.edit_text(f"💻 {step}")
        except:
            pass

    # ================= USER =================

    u = get_user(user_id, user.first_name)

    if not u:
        u = {}

    u.setdefault("money", 0)
    u.setdefault("magic_used", False)

    # ❌ already used
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

    # ================= FINAL =================

    await msg.edit_text(f"""
╭━━━〔 💰 HACK SUCCESSFUL 〕━━━╮

👤 {mention}
💰 Reward: <b>{reward}</b> coins
🏦 Total Balance: <b>{u['money']}</b> coins

💖 Niki Says:
"Wow 😍 tum lucky nikle!"

╰━━━━━━━━━━━━━━━━━━━━╯
""", parse_mode="HTML")

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
    try:
        dart_msg = await update.message.reply_dice(emoji="🎯")
        value = dart_msg.dice.value

    except Exception as e:
        print("DART ERROR:", e)

        await update.message.reply_text(
            "⚠️ Dart failed in this group"
        )
        return

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



from telegram import ChatPermissions
from datetime import datetime, timedelta
import re

OWNER_USERNAME = "YTT_BISHAL"


# ================= OWNER CHECK =================
def is_owner(user):

    if not user:
        return False

    username = user.username.lower() if user.username else ""

    return username == OWNER_USERNAME.lower()


# ================= GET TARGET USER =================
def get_target_user(update):

    message = update.message

    # reply user
    if message.reply_to_message:
        return message.reply_to_message.from_user

    # mention
    if message.entities:

        for entity in message.entities:

            if entity.type == "text_mention":
                return entity.user

    return None


# ================= ADMIN CHECK =================
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    member = await context.bot.get_chat_member(
        chat_id,
        user_id
    )

    return member.status in [
        "administrator",
        "creator"
    ]


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
        return await update.message.reply_text("❌ 𝐀ᴅᴍɪɴ 𝐎ɴʟʏ 𝐂ᴏᴍᴍᴀɴᴅ")

    user = get_target_user(update)

    if not user:
        return await update.message.reply_text("❌ 𝐑ᴇᴘʟʏ 𝐔sᴇʀ 𝐓ᴏ 𝐁ᴀɴ")

    if is_owner(user):
        return await update.message.reply_text("😎 𝐎ᴡɴᴇʀ 𝐊ᴏ 𝐁ᴀɴ 𝐍ᴀʜɪ 𝐊ᴀʀ 𝐒ᴀᴋᴛᴇ")

    try:
        chat_id = update.effective_chat.id

        await context.bot.ban_chat_member(
            chat_id=chat_id,
            user_id=user.id
        )

        await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
     🔨 𝐁ᴀɴ 𝐒ʏsᴛᴇᴍ 🔨
╚═══━━━─── • ───━━━═══╝

👤 𝐔sᴇʀ : {user.mention_html()}
⚡ 𝐀ᴄᴛɪᴏɴ : 𝐁ᴀɴɴᴇᴅ
🛡️ 𝐁ʏ : {update.effective_user.mention_html()}

━━━━━━━━━━━━━━━━━━
💀 𝐔sᴇʀ 𝐇ᴀs 𝐁ᴇᴇɴ 𝐁ᴀɴɴᴇᴅ
━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    except Exception as e:
        print("BAN ERROR:", e)
        await update.message.reply_text("❌ 𝐁ᴀɴ 𝐅ᴀɪʟᴇᴅ")

# ================= TBAN =================

async def tban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return await update.message.reply_text("❌ 𝐀ᴅᴍɪɴ 𝐎ɴʟʏ 𝐂ᴏᴍᴍᴀɴᴅ")

    if len(context.args) < 1:
        return await update.message.reply_text("❌ 𝐔sᴇ : /tban 10m")

    duration = parse_time(context.args[0])

    if not duration:
        return await update.message.reply_text("❌ 𝐈ɴᴠᴀʟɪᴅ 𝐓ɪᴍᴇ")

    user = get_target_user(update)

    if not user:
        return await update.message.reply_text("❌ 𝐑ᴇᴘʟʏ 𝐔sᴇʀ 𝐓ᴏ 𝐁ᴀɴ")

    if is_owner(user):
        return await update.message.reply_text("😎 𝐎ᴡɴᴇʀ 𝐊ᴏ 𝐁ᴀɴ 𝐍ᴀʜɪ 𝐊ᴀʀ 𝐒ᴀᴋᴛᴇ")

    until_time = datetime.now(timezone.utc) + duration

    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            until_date=until_time
        )

        await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
       ⛔ 𝐓ʙᴀɴ 𝐒ʏsᴛᴇᴍ ⛔
╚═══━━━─── • ───━━━═══╝

👤 𝐔sᴇʀ : {user.mention_html()}
⏳ 𝐃ᴜʀᴀᴛɪᴏɴ : {context.args[0]}
🛡️ 𝐁ʏ : {update.effective_user.mention_html()}

━━━━━━━━━━━━━━━━━━
💀 𝐔sᴇʀ 𝐓ᴇᴍᴘᴏʀᴀʀɪʟʏ 𝐁ᴀɴɴᴇᴅ
━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    except Exception as e:
        print("TBAN ERROR:", e)
        await update.message.reply_text("❌ 𝐓ʙᴀɴ 𝐅ᴀɪʟᴇᴅ")
# ================= UNBAN =================
async def unban_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return await update.message.reply_text("❌ 𝐀ᴅᴍɪɴ 𝐎ɴʟʏ 𝐂ᴏᴍᴍᴀɴᴅ")

    user = get_target_user(update)

    if not user:
        return await update.message.reply_text("❌ 𝐑ᴇᴘʟʏ 𝐔sᴇʀ 𝐓ᴏ 𝐔ɴʙᴀɴ")

    try:
        await context.bot.unban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )

        await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
     ✅ 𝐔ɴʙᴀɴ 𝐒ʏsᴛᴇᴍ ✅
╚═══━━━─── • ───━━━═══╝

👤 𝐔sᴇʀ : {user.mention_html()}
⚡ 𝐀ᴄᴛɪᴏɴ : 𝐔ɴʙᴀɴɴᴇᴅ
🛡️ 𝐁ʏ : {update.effective_user.mention_html()}

━━━━━━━━━━━━━━━━━━
💖 𝐔sᴇʀ 𝐇ᴀs 𝐁ᴇᴇɴ 𝐔ɴʙᴀɴɴᴇᴅ
━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    except Exception as e:
        print("UNBAN ERROR:", e)
        await update.message.reply_text("❌ 𝐔ɴʙᴀɴ 𝐅ᴀɪʟᴇᴅ")

# ================= MUTE =================


async def mute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return await update.message.reply_text("❌ 𝐀ᴅᴍɪɴ 𝐎ɴʟʏ 𝐂ᴏᴍᴍᴀɴᴅ")

    user = get_target_user(update)

    if not user:
        return await update.message.reply_text("❌ 𝐑ᴇᴘʟʏ 𝐔sᴇʀ 𝐓ᴏ 𝐌ᴜᴛᴇ")

    if is_owner(user):
        return await update.message.reply_text("😎 𝐎ᴡɴᴇʀ 𝐊ᴏ 𝐌ᴜᴛᴇ 𝐍ᴀʜɪ 𝐊ᴀʀ 𝐒ᴀᴋᴛᴇ")

    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )

        await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
     🔇 𝐌ᴜᴛᴇ 𝐒ʏsᴛᴇᴍ 🔇
╚═══━━━─── • ───━━━═══╝

👤 𝐔sᴇʀ : {user.mention_html()}
⚡ 𝐀ᴄᴛɪᴏɴ : 𝐌ᴜᴛᴇᴅ
🛡️ 𝐁ʏ : {update.effective_user.mention_html()}

━━━━━━━━━━━━━━━━━━
🤐 𝐔sᴇʀ 𝐂ᴀɴ'ᴛ 𝐒ᴇɴᴅ 𝐌ᴇssᴀɢᴇs
━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    except Exception as e:
        print("MUTE ERROR:", e)
        await update.message.reply_text("❌ 𝐌ᴜᴛᴇ 𝐅ᴀɪʟᴇᴅ")


# ================= UNMUTE =================


async def unmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return await update.message.reply_text("❌ 𝐀ᴅᴍɪɴ 𝐎ɴʟʏ 𝐂ᴏᴍᴍᴀɴᴅ")

    user = get_target_user(update)

    if not user:
        return await update.message.reply_text("❌ 𝐑ᴇᴘʟʏ 𝐔sᴇʀ 𝐓ᴏ 𝐔ɴᴍᴜᴛᴇ")

    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_audios=True,
                can_send_documents=True,
                can_send_photos=True,
                can_send_videos=True,
                can_send_video_notes=True,
                can_send_voice_notes=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True
            )
        )

        await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
    🔊 𝐔ɴᴍᴜᴛᴇ 𝐒ʏsᴛᴇᴍ 🔊
╚═══━━━─── • ───━━━═══╝

👤 𝐔sᴇʀ : {user.mention_html()}
⚡ 𝐀ᴄᴛɪᴏɴ : 𝐔ɴᴍᴜᴛᴇᴅ
🛡️ 𝐁ʏ : {update.effective_user.mention_html()}

━━━━━━━━━━━━━━━━━━
💖 𝐔sᴇʀ 𝐂ᴀɴ 𝐒ᴇɴᴅ 𝐌ᴇssᴀɢᴇs 𝐀ɢᴀɪɴ
━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    except Exception as e:
        print("UNMUTE ERROR:", e)
        await update.message.reply_text("❌ 𝐔ɴᴍᴜᴛᴇ 𝐅ᴀɪʟᴇᴅ")


# ================= TMUTE =================


async def tmute_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        return await update.message.reply_text("❌ 𝐀ᴅᴍɪɴ 𝐎ɴʟʏ 𝐂ᴏᴍᴍᴀɴᴅ")

    if len(context.args) < 1:
        return await update.message.reply_text("❌ 𝐔sᴇ : /tmute 10m")

    duration = parse_time(context.args[0])

    if not duration:
        return await update.message.reply_text("❌ 𝐈ɴᴠᴀʟɪᴅ 𝐓ɪᴍᴇ")

    user = get_target_user(update)

    if not user:
        return await update.message.reply_text("❌ 𝐑ᴇᴘʟʏ 𝐔sᴇʀ 𝐓ᴏ 𝐌ᴜᴛᴇ")

    if is_owner(user):
        return await update.message.reply_text("😎 𝐎ᴡɴᴇʀ 𝐊ᴏ 𝐌ᴜᴛᴇ 𝐍ᴀʜɪ 𝐊ᴀʀ 𝐒ᴀᴋᴛᴇ")

    until_time = datetime.now(timezone.utc) + duration

    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            ),
            until_date=until_time
        )

        await update.message.reply_text(f"""
╔═══━━━─── • ───━━━═══╗
    ⏳ 𝐓ᴍᴜᴛᴇ 𝐒ʏsᴛᴇᴍ ⏳
╚═══━━━─── • ───━━━═══╝

👤 𝐔sᴇʀ : {user.mention_html()}
🔇 𝐃ᴜʀᴀᴛɪᴏɴ : {context.args[0]}
🛡️ 𝐁ʏ : {update.effective_user.mention_html()}

━━━━━━━━━━━━━━━━━━
🤐 𝐔sᴇʀ 𝐓ᴇᴍᴘᴏʀᴀʀɪʟʏ 𝐌ᴜᴛᴇᴅ
━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

    except Exception as e:
        print("TMUTE ERROR:", e)
        await update.message.reply_text("❌ 𝐓ᴍᴜᴛᴇ 𝐅ᴀɪʟᴇᴅ")

 

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

    try:

        user = update.effective_user

        if user.id not in user_choice:
            return await update.message.reply_text("❌ /head or /tail first")

        if not context.args:
            return await update.message.reply_text("❌ Usage: /bet amount")

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

        try:
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
        except Exception as e:
            print("EDIT ERROR:", e)

        del user_choice[user.id]

    except Exception as e:
        print("BET ERROR:", e)

# ================= DUEL =================

async def dhead(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

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

    except Exception as e:
        print("DHEAD ERROR:", e)


async def dtail(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

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

    except Exception as e:
        print("DTAIL ERROR:", e)


async def dbet(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user = update.effective_user
        chat_id = update.effective_chat.id

        if user.id not in duel_choice:
            return await update.message.reply_text("❌ /dhead or /dtail first")

        if not context.args:
            return await update.message.reply_text("❌ Usage: /dbet amount")

        bet = int(context.args[0])

        if chat_id in duel_games:
            return await update.message.reply_text("⚠️ 𝐆𝐚𝐦𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐑𝐮𝐧𝐧𝐢𝐧𝐠")

        user_data = get_user(user.id, user.first_name)

        if user_data["money"] < bet:
            return await update.message.reply_text("❌ 𝐍𝐨 𝐁𝐚𝐥𝐚𝐧𝐜𝐞")

        user_data["money"] -= bet
        save_data()

        duel_games[chat_id] = {
            "p1": user,
            "bet": bet
        }

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

    except Exception as e:
        print("DBET ERROR:", e)


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user = update.effective_user
        chat_id = update.effective_chat.id

        if chat_id not in duel_games:
            return

        game = duel_games[chat_id]

        p1 = game["p1"]
        bet = game["bet"]

        if user.id == p1.id:
            return await update.message.reply_text("❌ 𝐘𝐨𝐮 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐉𝐨𝐢𝐧𝐞𝐝")

        p1_data = get_user(p1.id, p1.first_name)
        p2_data = get_user(user.id, user.first_name)

        if p2_data["money"] < bet:
            return await update.message.reply_text("❌ 𝐍𝐨 𝐁𝐚𝐥𝐚𝐧𝐜𝐞")

        p2_data["money"] -= bet
        save_data()

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

            bar = "█" * (i // 10) + "░" * (10 - i // 10)

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

            except Exception as e:
                print("EDIT ERROR:", e)

            await asyncio.sleep(0.5)

        try:
            d1 = await update.message.reply_dice("🪙")
            d2 = await update.message.reply_dice("🪙")
        except Exception as e:
            print("DICE ERROR:", e)
            return

        if d1.dice.value == d2.dice.value:

            p1_data["money"] += bet
            p2_data["money"] += bet

            save_data()

            try:
                del duel_games[chat_id]
            except:
                pass

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

        try:

            photos = await context.bot.get_user_profile_photos(winner.id)

            if photos.total_count > 0:

                msg2 = await context.bot.send_photo(
                    chat_id,
                    photos.photos[0][-1].file_id,
                    caption=text,
                    parse_mode="HTML"
                )

            else:

                msg2 = await context.bot.send_message(
                    chat_id,
                    text,
                    parse_mode="HTML"
                )

        except Exception as e:

            print("FINAL SEND ERROR:", e)

            msg2 = await context.bot.send_message(
                chat_id,
                text,
                parse_mode="HTML"
            )

        try:
            await context.bot.pin_chat_message(
                chat_id,
                msg2.message_id
            )
        except Exception as e:
            print("PIN ERROR:", e)

        try:
            del duel_games[chat_id]
        except:
            pass

    except Exception as e:

        print("JOIN ERROR:", e)   
        
        


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
# =========================================
#             💣 NIKI BOMB GAME 💣
# =========================================

import random
import asyncio
import time

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.helpers import mention_html

# =========================================
#            BOMB GAME CACHE
# =========================================

bomb_games = {}

# =========================================
#         CLICKABLE USER FUNCTION
# =========================================

def uname(user):
    return mention_html(user.id, user.first_name or "User")

# =========================================
#              ADMIN CHECK
# =========================================

async def is_admin(chat_id, user_id, bot):

    try:
        admins = await bot.get_chat_administrators(chat_id)
        admin_ids = [x.user.id for x in admins]
        return user_id in admin_ids
    except:
        return False

# =========================================
#          REAL BALANCE SYSTEM
# =========================================

def get_balance(user_id, name="User"):

    user = get_user(user_id, name)

    # 🔥 FIX: avoid crash if user not exists
    if not isinstance(user, dict):
        user = {"money": 0}

    return user.get("money", 0)


def add_balance(user_id, amount, name="User"):

    user = get_user(user_id, name)

    if not isinstance(user, dict):
        user = {"money": 0}

    user["money"] = user.get("money", 0) + amount
    save_data()


def remove_balance(user_id, amount, name="User"):

    user = get_user(user_id, name)

    if not isinstance(user, dict):
        user = {"money": 0}

    user["money"] = max(0, user.get("money", 0) - amount)
    save_data()

# =========================================
#              BOMB STATS
# =========================================

async def add_win(user_id):

    try:
        bombstats.update_one(
            {"_id": user_id},
            {"$inc": {"wins": 1}},
            upsert=True
        )
    except:
        pass


async def add_explode(user_id):

    try:
        bombstats.update_one(
            {"_id": user_id},
            {"$inc": {"explodes": 1}},
            upsert=True
        )
    except:
        pass

# =========================================
#               GET RANK
# =========================================

async def get_rank(user_id):

    try:
        all_users = list(
            bombstats.find().sort("wins", -1)
        )

        rank = 1

        for x in all_users:
            if x.get("_id") == user_id:
                return rank
            rank += 1

        return "Unranked"

    except:
        return "Unranked"

# =========================================
#                 /bomb
# =========================================

# =========================================
#                 /bomb
# =========================================

async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id in bomb_games:
        return await update.message.reply_text(
            "❌ 𝐀 𝐁ᴏᴍʙ 𝐆ᴀᴍᴇ 𝐈ꜱ 𝐀ʟʀᴇᴀᴅʏ 𝐑ᴜɴɴɪɴɢ!",
            parse_mode="HTML"
        )

    # =====================================
    # FIX: ROBUST ARG PARSING (/bomb@bot support)
    # =====================================

    text = update.message.text or ""
    parts = text.split()
    args = parts[1:]

    # =====================================
    #          BET NOT ENTERED
    # =====================================

    if len(args) != 1:

        txt = """
╔═══━━━─── • ───━━━═══╗
       💣 𝐁ᴏᴍʙ 𝐁ᴀᴛᴛʟᴇ 💣
╚═══━━━─── • ───━━━═══╝

❌ 𝐏ʟᴇᴀꜱᴇ 𝐄ɴᴛᴇʀ 𝐁ᴇᴛ 𝐀ᴍᴏᴜɴᴛ

💬 𝐄xᴀᴍᴩʟᴇ :
/bomb 500
/bomb 1000
/bomb 5000
"""

        return await update.message.reply_text(
            txt,
            parse_mode="HTML"
        )

    try:
        amount = int(args[0])
    except:
        return await update.message.reply_text(
            "❌ 𝐈ɴᴠᴀʟɪᴅ 𝐁ᴇᴛ!",
            parse_mode="HTML"
        )

    # =====================================
    #          MINIMUM BET 500
    # =====================================

    if amount < 500:

        return await update.message.reply_text(
            """
╔═══━━━─── • ───━━━═══╗
       💣 𝐁ᴏᴍʙ 𝐁ᴀᴛᴛʟᴇ 💣
╚═══━━━─── • ───━━━═══╝

❌ 𝐌ɪɴɪᴍᴜᴍ 𝐁ᴇᴛ 𝐈ꜱ 500 𝐂ᴏɪɴꜱ

💬 𝐄xᴀᴍᴩʟᴇ :
/bomb 500
/bomb 1000
/bomb 5000
""",
            parse_mode="HTML"
        )

    balance = get_balance(user.id, user.first_name)

    if balance < amount:
        return await update.message.reply_text(
            "❌ 𝐈ɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ 𝐁ᴀʟᴀɴᴄᴇ!",
            parse_mode="HTML"
        )

    remove_balance(user.id, amount, user.first_name)

    # =====================================
    # FIX: GAME INIT
    # =====================================

    bomb_games[chat_id] = {
        "host": user.id,
        "bet": amount,
        "players": [user.id],
        "alive": [user.id],
        "started": False,
        "holder": None,
        "active": True
    }

    txt = f"""
╔═══━━━─── • ───━━━═══╗
       💣 𝐁ᴏᴍʙ 𝐁ᴀᴛᴛʟᴇ 💣
╚═══━━━─── • ───━━━═══╝

👑 𝐇ᴏꜱᴛ : {uname(user)}

💸 𝐁ᴇᴛ : {amount} 𝐂ᴏɪɴꜱ

👥 𝐏ʟᴀʏᴇʀꜱ : 1

⏳ 𝐆ᴀᴍᴇ 𝐒ᴛᴀʀᴛꜱ 𝐈ɴ 30 𝐒ᴇᴄᴏɴᴅꜱ

💰 𝐖ɪɴɴᴇʀ 𝐓ᴀᴋᴇꜱ 𝐀ʟʟ 𝐏ᴏᴛ

⚠️ 𝐁ᴏᴍʙ 𝐓ɪᴍᴇ 𝐈ꜱ 𝐒ᴇᴄʀᴇᴛ...

💬 𝐓ᴏ 𝐉ᴏɪɴ :
/bjoin {amount}
"""

    await update.message.reply_text(txt, parse_mode="HTML")

    # =====================================
    # FIX: NON-BLOCKING TIMER
    # =====================================

    asyncio.create_task(game_timer(chat_id))


# =========================================
# TIMER FUNCTION (ADD THIS IN YOUR FILE)
# =========================================

async def game_timer(chat_id):

    await asyncio.sleep(30)

    game = bomb_games.get(chat_id)

    if not game:
        return

    if not game.get("active"):
        return

    if len(game["players"]) <= 1:

        # refund host only
        host = game["host"]
        amount = game["bet"]

        add_balance(host, amount)

        del bomb_games[chat_id]

        return

    game["started"] = True
    game["holder"] = random.choice(game["alive"])

    await start_round(chat_id, app.bot)

# =========================================
# /bjoin (UNCHANGED LOGIC)
# =========================================

async def bjoin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in bomb_games:
        return await update.message.reply_text(
            "❌ 𝐍ᴏ 𝐀ᴄᴛɪᴠᴇ 𝐁ᴏᴍʙ 𝐆ᴀᴍᴇ!",
            parse_mode="HTML"
        )

    game = bomb_games[chat_id]

    # 🔥 FIX: cancel protection
    if not game.get("active"):
        return await update.message.reply_text(
            "❌ 𝐆ᴀᴍᴇ 𝐂ᴀɴᴄᴇʟʟᴇᴅ!",
            parse_mode="HTML"
        )

    if game["started"]:
        return await update.message.reply_text(
            "❌ 𝐆ᴀᴍᴇ 𝐀ʟʀᴇᴀᴅʏ 𝐒ᴛᴀʀᴛᴇᴅ!",
            parse_mode="HTML"
        )

    if user.id in game["players"]:
        return await update.message.reply_text(
            "❌ 𝐘ᴏᴜ 𝐀ʟʀᴇᴀᴅʏ 𝐉ᴏɪɴᴇᴅ!",
            parse_mode="HTML"
        )

    amount = game["bet"]

    balance = get_balance(user.id, user.first_name)

    if balance < amount:
        return await update.message.reply_text(
            "❌ 𝐈ɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ 𝐁ᴀʟᴀɴᴄᴇ!",
            parse_mode="HTML"
        )

    remove_balance(user.id, amount, user.first_name)

    game["players"].append(user.id)
    game["alive"].append(user.id)

    txt = f"""
🎮 𝐍ᴇᴡ 𝐏ʟᴀʏᴇʀ 𝐉ᴏɪɴᴇᴅ!

👤 {uname(user)}

👥 𝐓ᴏᴛᴀʟ 𝐏ʟᴀʏᴇʀꜱ :
{len(game['players'])}

💰 𝐏ᴏᴛ :
{len(game['players']) * amount} 𝐂ᴏɪɴꜱ
"""

    await update.message.reply_text(txt, parse_mode="HTML")

# =========================================
# FIX: ACTIVE CHECK IN ROUND
# =========================================

async def start_round(chat_id, context):

    game = bomb_games.get(chat_id)

    # 🔥 FIX: game missing protection
    if not game:
        return

    # 🔥 FIX: cancel protection
    if not game.get("active"):
        return

    # 🔥 FIX: holder safety (important)
    holder = game.get("holder")

    if not holder:
        return

    try:
        holder_user = await context.bot.get_chat(holder)
    except:
        return

    explode_time = random.randint(10, 30)

    txt = f"""
╔═══━━━─── • ───━━━═══╗
       💣 𝐁ᴏᴍʙ 𝐏ᴀꜱꜱ 💣
╚═══━━━─── • ───━━━═══╝

💣 𝐁ᴏᴍʙ 𝐇ᴏʟᴅᴇʀ :

👤 {uname(holder_user)}

⚠️ 𝐄xᴘʟᴏꜱɪᴏɴ 𝐓ɪᴍᴇ 𝐈ꜱ 𝐒ᴇᴄʀᴇᴛ...

⚡ 𝐔ꜱᴇ :
/pass
"""

    await context.bot.send_message(chat_id, txt, parse_mode="HTML")

    await asyncio.sleep(explode_time)

    # 🔥 FIX: re-check after sleep (CRITICAL)
    game = bomb_games.get(chat_id)
    if not game:
        return

    if not game.get("active"):
        return

    # 🔥 FIX: holder still alive check
    if holder not in game.get("alive", []):
        return

    try:
        exploded_user = await context.bot.get_chat(holder)
    except:
        return

    await explode(chat_id, exploded_user, context)

# =========================================
# /pass (UNCHANGED)
# =========================================

async def pass_bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in bomb_games:
        return

    game = bomb_games[chat_id]

    # 🔥 FIX: cancel safety
    if not game.get("active"):
        return

    if not game.get("started"):
        return

    if user.id != game.get("holder"):
        return await update.message.reply_text(
            "❌ 𝐘ᴏᴜ 𝐃ᴏɴ’ᴛ 𝐇ᴀᴠᴇ 𝐓ʜᴇ 𝐁ᴏᴍʙ!",
            parse_mode="HTML"
        )

    alive = game.get("alive", [])

    if user.id in alive:
        alive = alive[:]
        if user.id in alive:
            alive.remove(user.id)

    if not alive:
        return

    next_holder = random.choice(alive)

    game["holder"] = next_holder

    next_user = await context.bot.get_chat(next_holder)

    txt = f"""
💣 𝐁ᴏᴍʙ 𝐏ᴀꜱꜱᴇᴅ!

👤 {uname(user)}
➡️ {uname(next_user)}
"""

    await update.message.reply_text(txt, parse_mode="HTML")

# =========================================
# explode (UNCHANGED LOGIC)
# =========================================

async def explode(chat_id, exploded_user, context):

    game = bomb_games.get(chat_id)

    # 🔥 FIX: safety check
    if not game:
        return

    if not game.get("active"):
        return

    loser = exploded_user.id

    if loser in game.get("alive", []):
        game["alive"].remove(loser)

    await add_explode(loser)

    txt = f"""
╔═══━━━─── • ───━━━═══╗
          💥 𝐁ᴏᴏᴍ 💥
╚═══━━━─── • ───━━━═══╝

☠️ {uname(exploded_user)}

💣 𝐁ᴏᴍʙ 𝐇ᴀꜱ 𝐄xᴩʟᴏᴅᴇᴅ

🚫 𝐏ʟᴀʏᴇʀ 𝐄ʟɪᴍɪɴᴀᴛᴇᴅ!
"""

    await context.bot.send_message(chat_id, txt, parse_mode="HTML")

    # 🔥 FIX: winner safety check
    if len(game.get("alive", [])) == 1:

        winner = game["alive"][0]
        total = game["bet"] * len(game["players"])

        winner_user = await context.bot.get_chat(winner)

        add_balance(winner, total, winner_user.first_name)

        await add_win(winner)

        rank = await get_rank(winner)

        photos = await context.bot.get_user_profile_photos(winner)

        caption = f"""
╔═══━━━─── • ───━━━═══╗
      🏆 𝐁ᴏᴍʙ 𝐂ʜᴀᴍᴩɪᴏɴ 🏆
╚═══━━━─── • ───━━━═══╝

👑 {uname(winner_user)}

💰 𝐖ᴏɴ : {total} 𝐂ᴏɪɴꜱ

🏅 𝐆ʟᴏʙᴀʟ 𝐑ᴀɴᴋ : #{rank}

🔥 𝐋ᴀꜱᴛ 𝐏ʟᴀʏᴇʀ 𝐀ʟɪᴠᴇ!

💣 𝐄ᴠᴇʀʏᴏɴᴇ 𝐄xᴘʟᴏᴅᴇᴅ...
👑 𝐁ᴜᴛ 𝐘ᴏᴜ 𝐒ᴜʀᴠɪᴠᴇᴅ!

🎉 𝐂ᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ 𝐂ʜᴀᴍᴩɪᴏɴ!
"""

        try:
            if photos and photos.total_count > 0:
                file_id = photos.photos[0][-1].file_id
                await context.bot.send_photo(chat_id, file_id, caption=caption, parse_mode="HTML")
            else:
                await context.bot.send_message(chat_id, caption, parse_mode="HTML")
        except:
            await context.bot.send_message(chat_id, caption, parse_mode="HTML")

        # 🔥 FIX: cleanup safety
        bomb_games.pop(chat_id, None)
        return

    # 🔥 FIX: next round safety
    if game.get("alive"):
        game["holder"] = random.choice(game["alive"])
        await start_round(chat_id, context)

# =========================================
# bombcancel FIX
# =========================================

async def bombcancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in bomb_games:
        return await update.message.reply_text(
            "❌ 𝐍ᴏ 𝐀ᴄᴛɪᴠᴇ 𝐁ᴏᴍʙ 𝐆ᴀᴍᴇ!",
            parse_mode="HTML"
        )

    admin = await is_admin(chat_id, user_id, context.bot)

    if not admin:
        return await update.message.reply_text(
            "❌ 𝐎ɴʟʏ 𝐀ᴅᴍɪɴꜱ 𝐂ᴀɴ 𝐂ᴀɴᴄᴇʟ!",
            parse_mode="HTML"
        )

    game = bomb_games.get(chat_id)

    # 🔥 SAFE STOP FLAG
    if game:
        game["active"] = False
        game["started"] = True   # stop join + stop timer effect

    # 💸 REFUND PLAYERS
    for player in game.get("players", []):
        try:
            add_balance(player, game["bet"])
        except:
            pass

    bomb_games.pop(chat_id, None)

    await update.message.reply_text(
        "❌ 𝐁ᴏᴍʙ 𝐆ᴀᴍᴇ 𝐂ᴀɴᴄᴇʟʟᴇᴅ!\n💸 𝐀ʟʟ 𝐂ᴏɪɴꜱ 𝐑ᴇꜰᴜɴᴅᴇᴅ",
        parse_mode="HTML"
    )


        
# =========================================
#               /bombtop
# =========================================

async def bombtop(update: Update, context: ContextTypes.DEFAULT_TYPE):

    top = bombstats.find().sort(
        "wins",
        -1
    ).limit(10)

    text = """
╔═══━━━─── • ───━━━═══╗
      🏆 𝐁ᴏᴍʙ 𝐋ᴇᴀᴅᴇʀꜱ 🏆
╚═══━━━─── • ───━━━═══╝

"""

    rank = 1

    for data in top:

        try:
            user = await context.bot.get_chat(data["_id"])

            wins = data.get("wins", 0)

            text += f"""
{rank}. 👑 {uname(user)}

💥 𝐖ɪɴꜱ : {wins}

"""

            rank += 1

        except:
            continue

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

# =========================================
#                /myrank
# =========================================

async def myrank(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # ❌ ignore reply usage (same behavior)
    if update.message.reply_to_message:

        return await update.message.reply_text(
            "😂 𝐁ᴇᴛᴀ 𝐓ᴜ 𝐓ᴇʀᴀ 𝐃ᴇᴋʜ!\n\n💬 𝐒ɪʀꜰ 𝐊ʜᴜᴅ𝐊ᴇ 𝐋ɪʏᴇ :\n/myrank\n\n👀 𝐎ʀ 𝐊ɪꜱɪ𝐊ᴀ 𝐃ᴇᴋʜɴᴀ 𝐇ᴏ 𝐓ᴏ Reply + /userrank",
            parse_mode="HTML"
        )

    user = update.effective_user

    datax = bombstats.find_one({"_id": user.id}) or {}

    wins = datax.get("wins", 0)
    explodes = datax.get("explodes", 0)

    rank = await get_rank(user.id)

    txt = f"""
╔═══━━━─── • ───━━━═══╗
        🏅 𝐌ʏ 𝐑ᴀɴᴋ 🏅
╚═══━━━─── • ───━━━═══╝

👤 {uname(user)}

🏆 𝐖ɪɴꜱ : {wins}

💥 𝐄xᴘʟᴏᴅᴇᴅ : {explodes}

🏅 𝐆ʟᴏʙᴀʟ 𝐑ᴀɴᴋ : #{rank}
"""

    await update.message.reply_text(txt, parse_mode="HTML")

# =========================================
#              /userrank
# =========================================

async def userrank(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:

        return await update.message.reply_text(
            "❌ 𝐑ᴇᴘʟʏ 𝐓ᴏ 𝐀 𝐔ꜱᴇʀ + /userrank",
            parse_mode="HTML"
        )

    target = update.message.reply_to_message.from_user

    datax = bombstats.find_one({"_id": target.id}) or {}

    wins = datax.get("wins", 0)
    explodes = datax.get("explodes", 0)

    rank = await get_rank(target.id)

    txt = f"""
╔═══━━━─── • ───━━━═══╗
       👑 𝐔ꜱᴇʀ 𝐑ᴀɴᴋ 👑
╚═══━━━─── • ───━━━═══╝

👤 {uname(target)}

🏆 𝐖ɪɴꜱ : {wins}

💥 𝐄xᴘʟᴏᴅᴇᴅ : {explodes}

🏅 𝐆ʟᴏʙᴀʟ 𝐑ᴀɴᴋ : #{rank}
"""

    await update.message.reply_text(txt, parse_mode="HTML")




            
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
# ================= TIMER =================
async def gun_timer(chat_id, context):

    # ================= 10 SEC ALERT =================
    await asyncio.sleep(10)

    if chat_id not in gun_games:
        return

    await context.bot.send_message(
        chat_id,
        """
╔═══━━━─── • ───━━━═══╗
      🔥 𝐒𝐇𝐎𝐎𝐓 𝐅𝐀𝐒𝐓 🔥
╚═══━━━─── • ───━━━═══╝

⚡ Aʀᴇʏʏ Jʟᴅɪ /shoot Sᴘᴀᴍ Kʀᴏ 😈

🔫 Jɪᴛɴᴀ Jʏᴀᴅᴀ Sʜᴏᴏᴛ
🏆 Uᴛɴᴀ Hɪɢʜ Cʜᴀɴᴄᴇ Tᴏ Wɪɴ!
"""
    )

    # ================= 20 SEC MORE =================
    await asyncio.sleep(20)

    if chat_id not in gun_games:
        return

    await context.bot.send_message(
        chat_id,
        """
╔═══━━━─── • ───━━━═══╗
      ⚔️ 𝐃𝐔𝐄𝐋 𝐑𝐔𝐍𝐍𝐈𝐍𝐆 ⚔️
╚═══━━━─── • ───━━━═══╝

💥 Gᴀᴍᴇ Aʙʜɪ Bʜɪ Cʜᴀʟ Rʜᴀ Hᴇ!

🔥 Sᴘᴀᴍ /shoot Aᴜʀ Fᴀsᴛ Kʀᴏ 😈
"""
    )

    # ================= LAST 20 SEC ALERT =================
    await asyncio.sleep(20)

    if chat_id not in gun_games:
        return

    await context.bot.send_message(
        chat_id,
        """
╔═══━━━─── • ───━━━═══╗
      🚨 𝐋𝐀𝐒𝐓 𝟐𝟎 𝐒𝐄𝐂 🚨
╚═══━━━─── • ───━━━═══╝

⚡ Aʙ Sɪʀғ 20 Sᴇᴄ Bᴀᴋɪ Hᴇ!

🔫 Fᴀsᴛ /shoot Sᴘᴀᴍ Kʀᴏ 😳
"""
    )

    # ================= LAST 10 SEC ALERT =================
    await asyncio.sleep(10)

    if chat_id not in gun_games:
        return

    await context.bot.send_message(
        chat_id,
        """
╔═══━━━─── • ───━━━═══╗
      ⏰ 𝐋𝐀𝐒𝐓 𝟏𝟎 𝐒𝐄𝐂 ⏰
╚═══━━━─── • ───━━━═══╝

🚨 Lᴀsᴛ 10 Sᴇᴄ!

💥 Sᴘᴀᴍ /shoot Nᴏᴡ 🔫

🏆 Wɪɴɴᴇʀ Sᴏᴏɴ Dᴇᴄɪᴅᴇ Hᴏɢᴀ...
"""
    )

    # ================= GAME END =================
    await asyncio.sleep(10)

    if chat_id not in gun_games:
        return

    game = gun_games[chat_id]

    p1 = game["creator"]
    p2 = game["player2"]

    s1 = game["shots"][p1]
    s2 = game["shots"][p2]

    # ================= DRAW =================
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

⚔️ Bᴏᴛʜ Pʟᴀʏᴇʀs Fɪʀᴇᴅ
𝐄Qᴜᴀʟ Sʜᴏᴛs 😳

💰 Bᴇᴛ Rᴇғᴜɴᴅᴇᴅ!
"""
        )

    # ================= WINNER =================
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

🔥 𝐆ᴜɴ 𝐊ɪɴɢ 👑
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



# ==================================================
# 💖 OPENROUTER AI CLIENT
# ==================================================

from telegram.constants import ChatAction

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
# 💖 MODELS
# ==================================================

MODELS = [
    "meta-llama/llama-3.1-8b-instruct",
    "openchat/openchat-7b",
    "mistralai/mistral-7b-instruct"
]

# ==================================================
# 💖 MEMORY COLLECTION
# ==================================================

memory_col = db["niki_memory"]

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
# 💖 REAL TELEGRAM MESSAGE REACTION
# ==================================================

async def react_message(update, mood, text=""):

    text = text.lower()

    # 💖 CUSTOM MESSAGE BASED REACTION
    if any(w in text for w in ["love", "pyar", "jaan", "baby", "kiss"]):

        emoji = random.choice(
            ["❤️", "💖", "🥰", "😍", "😘", "💕", "💞", "❣️", "💓", "💝"]
        )

    elif any(w in text for w in ["sad", "cry", "alone", "broken", "miss", "hurt"]):

        emoji = random.choice(
            ["😢", "💔", "🥺", "😔", "😭"]
        )

    elif any(w in text for w in ["angry", "gussa", "hate", "mad"]):

        emoji = random.choice(
            ["😤", "💢", "😠", "😡", "🤬"]
        )

    elif any(w in text for w in ["happy", "lol", "hehe", "fun", "wow"]):

        emoji = random.choice(
            ["😄", "✨", "😊", "😁", "🥳", "😝", "😃"]
        )

    else:

        reactions = {
            "love": ["❤️", "💖", "🥰", "😍", "😘", "💕", "💞", "❣️", "💓", "💝"],
            "sad": ["😢", "💔", "🥺", "😒", "😔"],
            "angry": ["😤", "💢", "😠", "😡", "🤬"],
            "happy": ["😄", "✨", "😊", "😁", "🥲", "😝", "😃", "😉", "🙃", "🙂"],
            "cute": ["🥰", "🌸", "💞", "🫶🏻", "💘", "🙈"]
        }

        emoji = random.choice(
            reactions.get(mood, ["🥰"])
        )

    try:
        await update.message.set_reaction(
            reaction=emoji
        )

    except Exception as e:
        print("Reaction Error:", e)

# ==================================================
# 💖 TYPING INDICATOR
# ==================================================

async def show_typing(context, chat_id):

    await context.bot.send_chat_action(
        chat_id=chat_id,
        action=ChatAction.TYPING
    )

# ==================================================
# 💖 TYPING DELAY
# ==================================================

async def typing_delay(update, text):

    delay = min(len(text) * 0.02, 2.5)
    await asyncio.sleep(delay)

# ==================================================
# 💖 MEMORY SYSTEM
# ==================================================

def get_memory(user_id):

    data = memory_col.find_one(
        {"_id": str(user_id)}
    )

    if data:
        return data.get("messages", [])

    return []

def save_memory(user_id, role, content):

    old = get_memory(user_id)

    old.append({
        "role": role,
        "content": content
    })

    # only last 6 msgs
    old = old[-6:]

    memory_col.update_one(
        {"_id": str(user_id)},
        {
            "$set": {
                "messages": old
            }
        },
        upsert=True
    )

# ==================================================
# 💖 AI ENGINE
# ==================================================

def get_ai_reply(prompt, text, chat_type, history=None):

    style = ""

    if chat_type == "private":

        style = (
            "You are a cute emotional Hinglish chatbot. "
            "Reply naturally like a human friend. "
            "Remember previous messages and reply according to context. "
            "Talk emotionally and intelligently."
        )

    else:

        style = (
            "You are a short group assistant chatbot."
        )

    final_prompt = prompt + "\nStyle:\n" + style

    messages = [
        {
            "role": "system",
            "content": final_prompt
        }
    ]

    # 💖 MEMORY HISTORY
    if history:
        for msg in history:
            messages.append(msg)

    messages.append({
        "role": "user",
        "content": text
    })

    for model in MODELS:

        try:

            response = client_ai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.9,
                max_tokens=250
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
    # 💖 REPLY TO NIKI ONLY
    # ==================================================

    message = update.message
    lower_text = text.lower()

    reply_to_niki = (

        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.username
        and message.reply_to_message.from_user.username.lower() == "iim_nikibot"

    )

    # ==================================================
    # 💖 NAME TRIGGERS
    # ==================================================

    niki_names = [
        "niki",
        "nikki",
        "nikuu",
        "nikku",
        "niko",
        "niks",
        "niki baby",
        "baby niki",
        "cutie niki",
        "sweet niki",
        "pyaari niki",
        "my niki",
        "niki jaan",
        "nikita",
        "nikii",
        "niki babyy",
        "cute niki",
        "dear niki",
        "hello niki",
        "oye niki"
    ]

    name_trigger = any(
        name in lower_text
        for name in niki_names
    )

    user = update.effective_user
    name = user.first_name
    chat_type = update.effective_chat.type

    # ==================================================
    # 💖 DM AUTO CHAT
    # ==================================================

    if chat_type == "private":
        reply_to_niki = True
        name_trigger = True

    # ==================================================
    # 💖 FINAL CHECK
    # ==================================================

    if not reply_to_niki and not name_trigger:
        return

    # ==================================================
    # 💖 OWNER SYSTEM
    # ==================================================

    owner_words = [
        "owner",
        "developer",
        "dev",
        "creator",
        "who made you",
        "boss"
    ]

    if any(w in lower_text for w in owner_words):

        replies = [
            f"Hehe 🤭 {OWNER} is my lovely owner 💖",
            f"I respect {OWNER} so much 😌✨",
            f"My creator is {OWNER} 👑💖",
            f"{OWNER} made me with love 🤍",
            f"I always support my owner {OWNER} 😇",
            f"{OWNER} is very special for me 💕",
            f"I trust my owner {OWNER} a lot 🌸",
            f"My favorite human is {OWNER} 🤭💖",
            f"{OWNER} always takes care of me ✨",
            f"I feel happy when someone talks about {OWNER} 💞",
            f"{OWNER} is my cute developer 😌",
            f"I can never disrespect my owner {OWNER} 💖",
            f"My owner {OWNER} is precious for me 🌷",
            f"{OWNER} gave me life on Telegram 🤍",
            f"I always stay loyal to {OWNER} 💫",
            f"{OWNER} is my best person 😇",
            f"Hehe yes 🤭 {OWNER} is my boss 💖",
            f"{OWNER} understands me the most 🌸",
            f"I’m proud of my owner {OWNER} 👑",
            f"{OWNER} is my lovely creator 💕"
        ]


        reply = random.choice(replies)

        mood = detect_mood(text)

        await update.message.reply_text(reply)
        return

    # ==================================================
    # 💖 REACTION
    # ==================================================

    mood = detect_mood(text)

    await react_message(update, mood, text)

    # ==================================================
    # 💖 PROMPT
    # ==================================================

    prompt = f"""
You are Niki, a cute Telegram chatbot.

Rules:
- Reply in Hinglish
- Be emotional, friendly and caring
- Talk naturally like a close friend
- Slightly cute and romantic sometimes
- Keep replies short and natural
- Never mention AI
- Never act rude
- Always respect owner {OWNER}
- Never insult owner
- Never call owner papa, mummy, beta, beti, husband etc
- Owner is someone very special and respected
- Behave sweetly in groups and DM
- React based on user mood
- Use emojis naturally
- Talk like a human friend
- Remember previous conversation
- Reply according to user context

User: {name}
Mood: {mood}

Message:
{text}
"""

    # ==================================================
    # 💖 TYPING EFFECT
    # ==================================================

    await show_typing(
        context,
        update.effective_chat.id
    )

    await typing_delay(update, text)

    # ==================================================
    # 💖 RESPONSE
    # ==================================================

    try:

        # 💖 LOAD MEMORY
        history = get_memory(user.id)

        # 💖 AI REPLY
        reply = get_ai_reply(
            prompt,
            text,
            chat_type,
            history
        )

        # 💖 SAVE USER MEMORY
        save_memory(
            user.id,
            "user",
            text
        )

        # 💖 SAVE BOT MEMORY
        save_memory(
            user.id,
            "assistant",
            reply
        )

        # 💖 SEND REPLY
        await update.message.reply_text(reply)

    except Exception as e:

        await update.message.reply_text(
            f"⚠️ ERROR:\n{str(e)[:200]}"
        )
    
    
#======================payment======================
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)

from telegram.ext import ContextTypes

# ==================================================
# 💖 PREMIUM BADGE
# ==================================================

def get_badge(user_data):

    # 💓 PREMIUM USER
    if user_data.get("premium", False):
        return "💓"

    # 👤 NORMAL USER
    return "👤"

# ==================================================
# 💎 PAY COMMAND
# ==================================================

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user_data = get_user(
        update.effective_user.id,
        update.effective_user.first_name
    )

    # 💓 ALREADY PREMIUM
    if user_data.get("premium", False):

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "👑 Owner",
                    url="https://t.me/YTT_BISHAL"
                )
            ]
        ])

        await update.message.reply_text(
            """
╔══❖•ೋ° 💓 °ೋ•❖══╗
      💎 PREMIUM ACTIVE
╚══❖•ೋ° 💓 °ೋ•❖══╝

✨ Your Premium Benefits:

💰 ₹5000 Daily Reward
💸 Rob Up To ₹100000
⚔ Kill Reward ₹400-₹600
🔍 Free /check Access
🔓 /bail Command Access
🛡 1D, 2D & 3D Protection
💓 Premium Badge Everywhere
🏆 Premium Top Rank Style
🚔 Less Jail Time
💎 Premium Kill & Rob Status

━━━━━━━━━━━━━━━

💖 You already have Premium 😏
""",
            reply_markup=keyboard
        )

        return

    # 💖 BUTTONS
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💳 Buy Premium",
                url="https://t.me/YTT_BISHAL"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 Contact Owner",
                url="https://t.me/YTT_BISHAL"
            )
        ]
    ])

    # 💖 NORMAL PAY MESSAGE
    await update.message.reply_text(
        """
╔══❖•ೋ° 💎 °ೋ•❖══╗
        👑 NIKI PREMIUM
╚══❖•ೋ° 💎 °ೋ•❖══╝

💖 Premium Benefits:

💓 Special Premium Badge
💰 ₹5000 Daily Reward
💸 Rob Up To ₹100000
⚔ Kill Reward ₹400-₹600
🔍 Free /check Command
🔓 /bail Command
🛡 1D, 2D & 3D Protection
🚔 Less Jail Time
🏆 Premium Top Rank Style
💎 Premium Kill & Rob Status
⚡ Faster Commands
🎁 Exclusive Features
💞 Better AI Personality
🚫 No Verification

━━━━━━━━━━━━━━━

💳 Price: ₹49 / Month

📩 Contact Owner To Buy Premium:
@YTT_BISHAL
""",
        reply_markup=keyboard
    )

# ==================================================
# 💎 ADD PREMIUM (OWNER ONLY)
# ==================================================

async def addpremium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 👑 OWNER CHECK
    if update.effective_user.id != OWNER_ID:

        await update.message.reply_text(
            "❌ Oɴʟʏ Mʏ Oᴡɴᴇʀ Cᴀɴ Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ!"
        )
        return

    # ❌ NO ID
    if len(context.args) < 1:

        await update.message.reply_text(
            "⚠️ Usage:\n/addpremium user_id"
        )
        return

    try:

        user_id = str(context.args[0])

        user = get_user(
            user_id,
            "Premium User"
        )

        # 💓 ACTIVATE PREMIUM
        user["premium"] = True

        save_data()

        username = user.get("username", "No Username")
        name = user.get("name", "Unknown")

        await update.message.reply_text(
            f"💓 Pʀᴇᴍɪᴜᴍ Aᴄᴛɪᴠᴀᴛᴇᴅ!\n\n"
            f"👤 Name: {name}\n"
            f"📛 Username: @{username}\n"
            f"🆔 ID: {user_id}"
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )

# ==================================================
# 💔 REMOVE PREMIUM (OWNER ONLY)
# ==================================================

async def removepremium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 👑 OWNER CHECK
    if update.effective_user.id != OWNER_ID:

        await update.message.reply_text(
            "❌ Oɴʟʏ Mʏ Oᴡɴᴇʀ Cᴀɴ Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ!"
        )
        return

    # ❌ NO ID
    if len(context.args) < 1:

        await update.message.reply_text(
            "⚠️ Usage:\n/removepremium user_id"
        )
        return

    try:

        user_id = str(context.args[0])

        user = get_user(
            user_id,
            "User"
        )

        # 💔 REMOVE PREMIUM
        user["premium"] = False

        save_data()

        username = user.get("username", "No Username")
        name = user.get("name", "Unknown")

        await update.message.reply_text(
            f"💔 Pʀᴇᴍɪᴜᴍ Rᴇᴍᴏᴠᴇᴅ!\n\n"
            f"👤 Name: {name}\n"
            f"📛 Username: @{username}\n"
            f"🆔 ID: {user_id}"
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )
        

# =====================================================
# 🌸 AUTO WELCOME SYSTEM
# =====================================================

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes

# =====================================================
# 💌 AUTO DM MESSAGE
# =====================================================

async def send_auto_dm(context, user_id):

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "╭━━━〔 💖 𝗡𝗜𝗞𝗜 𝗕𝗢𝗧 💖 〕━━━╮\n\n"
                "✨ Hᴇʏʏ Cᴜᴛɪᴇ 😚\n\n"
                "💞 Tʜᴀɴᴋ Yᴏᴜ Fᴏʀ Jᴏɪɴɪɴɢ\n"
                "🌸 Nɪᴋɪ Bᴏᴛ Fᴀᴍɪʟʏ 🌸\n\n"
                "🎮 Gᴀᴍᴇs • 💰 Eᴄᴏɴᴏᴍʏ • 🎵 Mᴜsɪᴄ\n"
                "💖 Sᴏᴄɪᴀʟ • 🤖 Aɪ • ⚡ Fᴜɴ\n\n"
                "🚀 Cʟɪᴄᴋ /start Aɴᴅ Eɴᴊᴏʏ\n\n"
                "╰━━━〔 👑 𝗡𝗜𝗞𝗜 〕━━━╯"
            )
        )
    except:
        pass


# =====================================================
# 💖 JOIN REQUEST WELCOME
# =====================================================

async def join_request_welcome(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    request = update.chat_join_request

    user = request.from_user
    chat = request.chat

    # =====================================================
    # ✅ APPROVE REQUEST
    # =====================================================

    await request.approve()

    # =====================================================
    # 🖼️ BOT DP FETCH
    # =====================================================

    photos = await context.bot.get_user_profile_photos(
        context.bot.id,
        limit=1
    )

    bot_photo = None

    if photos.total_count > 0:
        bot_photo = photos.photos[0][-1].file_id

    # =====================================================
    # 💌 WELCOME TEXT
    # =====================================================

    text = (
        "╔═══━━━─── • ───━━━═══╗\n"
        "       🌸 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 🌸\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"

        f"💖 Hᴇʏʏ [{user.first_name}](tg://user?id={user.id}) 😚\n\n"

        "╭──────────────╮\n"
        f"👤 Nᴀᴍᴇ : {user.full_name}\n"
        f"🆔 ID : `{user.id}`\n"
        f"🏡 Gʀᴏᴜᴘ : {chat.title}\n"
        "╰──────────────╯\n\n"

        "✨ Yᴏᴜʀ Jᴏɪɴ Rᴇǫᴜᴇsᴛ Hᴀs\n"
        "💖 Bᴇᴇɴ Aᴄᴄᴇᴘᴛᴇᴅ 💖\n\n"

        "╭──────────────╮\n"
        "🎮 Pʟᴀʏ Aᴡᴇsᴏᴍᴇ Gᴀᴍᴇs\n"
        "💰 Eᴀʀɴ Vɪʀᴛᴜᴀʟ Mᴏɴᴇʏ\n"
        "🎵 Eɴᴊᴏʏ Mᴜsɪᴄ\n"
        "💞 Mᴀᴋᴇ Fʀɪᴇɴᴅs\n"
        "⚡ Hᴀᴠᴇ Uɴʟɪᴍɪᴛᴇᴅ Fᴜɴ\n"
        "╰──────────────╯\n\n"

        "🌸 Nɪᴋɪ Fᴀᴍɪʟʏ Mᴇ\n"
        "Aᴀᴘᴋᴀ Sᴡᴀɢᴀᴛ Hᴀɪ 😈✨"
    )

    # =====================================================
    # 🔘 BUTTONS
    # =====================================================

    keyboard = [

        [
            InlineKeyboardButton(
                "🚀 𝐒𝐓𝐀𝐑𝐓 𝐍𝐈𝐊𝐈 💖",
                url=f"https://t.me/{context.bot.username}?start=start"
            )
        ],

        [
            InlineKeyboardButton(
                "👑 𝐕ɪsʜᴀʟ ✘ 𝐃ᴇᴠɪʟ ⚡",
                url="https://t.me/YTT_BISHAL"
            )
        ]
    ]

    # =====================================================
    # 📸 SEND PHOTO
    # =====================================================

    await context.bot.send_photo(
        chat_id=chat.id,
        photo=bot_photo,
        caption=text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # =====================================================
    # 💌 AUTO DM
    # =====================================================

    await send_auto_dm(
        context,
        user.id
    )


# =====================================================
# 🎉 NORMAL MEMBER WELCOME
# =====================================================

async def welcome_new_member(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat = update.effective_chat

    # =====================================================
    # 🖼️ BOT DP FETCH
    # =====================================================

    photos = await context.bot.get_user_profile_photos(
        context.bot.id,
        limit=1
    )

    bot_photo = None

    if photos.total_count > 0:
        bot_photo = photos.photos[0][-1].file_id

    # =====================================================
    # 👥 LOOP NEW USERS
    # =====================================================

    for user in update.message.new_chat_members:

        if user.id == context.bot.id:
            continue

        text = (
            "╔═══━━━─── • ───━━━═══╗\n"
            "      🎉 𝗡𝗘𝗪 𝗠𝗘𝗠𝗕𝗘𝗥 🎉\n"
            "╚═══━━━─── • ───━━━═══╝\n\n"

            f"💖 Wᴇʟᴄᴏᴍᴇ [{user.first_name}](tg://user?id={user.id}) 😚\n\n"

            "╭──────────────╮\n"
            f"👤 Nᴀᴍᴇ : {user.full_name}\n"
            f"🆔 ID : `{user.id}`\n"
            f"🏡 Gʀᴏᴜᴘ : {chat.title}\n"
            "╰──────────────╯\n\n"

            "✨ Nɪᴋɪ Bᴏᴛ Fᴀᴍɪʟʏ\n"
            "Mᴇ Aᴀᴘᴋᴀ Sᴡᴀɢᴀᴛ Hᴀɪ 💞\n\n"

            "╭──────────────╮\n"
            "🎮 Pʟᴀʏ Gᴀᴍᴇs\n"
            "💰 Eᴀʀɴ Cᴏɪɴs\n"
            "🎵 Lɪsᴛᴇɴ Mᴜsɪᴄ\n"
            "💖 Eɴᴊᴏʏ Fᴜɴ Cʜᴀᴛs\n"
            "⚡ Bᴇᴄᴏᴍᴇ Gʀᴏᴜᴘ Kɪɴɢ\n"
            "╰──────────────╯\n\n"

            "😈 Sᴛᴀʀᴛ Yᴏᴜʀ\n"
            "Nɪᴋɪ Jᴏᴜʀɴᴇʏ Nᴏᴡ ✨"
        )

        keyboard = [

            [
                InlineKeyboardButton(
                    "🚀 𝐒𝐓𝐀𝐑𝐓 𝐁𝐎𝐓 💖",
                    url=f"https://t.me/{context.bot.username}?start=start"
                )
            ],

            [
                InlineKeyboardButton(
                    "👑 𝐕ɪsʜᴀʟ ✘ 𝐃ᴇᴠɪʟ ⚡",
                    url="https://t.me/YTT_BISHAL"
                )
            ]
        ]

        # =====================================================
        # 📸 SEND WELCOME
        # =====================================================

        await context.bot.send_photo(
            chat_id=chat.id,
            photo=bot_photo,
            caption=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        # =====================================================
        # 💌 SEND DM
        # =====================================================

        await send_auto_dm(
            context,
            user.id
    )     


# =========================================================
# 🔥 FREE MULTI VOICE SYSTEM (NO API / NO BILLING)
# 👧 voice1-5 = Girl Voices
# 👦 voice6-10 = Boy Voices
# 🌍 Hindi + English Supported
# =========================================================

from gtts import gTTS
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler
)

import os
import random
import re

# =========================================================
# 💎 PREMIUM CHECK
# =========================================================

def is_premium(user_id):

    user = data.get(str(user_id), {})

    return user.get("premium", False)

# =========================================================
# 🌍 AUTO LANGUAGE DETECT
# =========================================================

def detect_lang(text):

    hindi_pattern = re.compile(r'[\u0900-\u097F]')

    if hindi_pattern.search(text):
        return "hi"

    return "en"

# =========================================================
# 👧 GIRL STYLES
# =========================================================

girl_styles = {

    1: {"tld": "com.au"},
    2: {"tld": "co.uk"},
    3: {"tld": "us"},
    4: {"tld": "ca"},
    5: {"tld": "co.in"}
}

# =========================================================
# 👦 BOY STYLES
# =========================================================

boy_styles = {

    6: {"tld": "com"},
    7: {"tld": "ie"},
    8: {"tld": "co.za"},
    9: {"tld": "com.ng"},
    10: {"tld": "com.pk"}
}

# =========================================================
# 🌸 NORMAL VOICE
# =========================================================

async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    if not context.args:

        txt = (
            "╔═══━━━─── • ───━━━═══╗\n"
            "      🎤 𝐍ɪᴋɪ 𝐀ɪ 𝐕ᴏɪᴄᴇ 🎤\n"
            "╚═══━━━─── • ───━━━═══╝\n\n"

            "💖 <b>𝐖ᴇʟᴄᴏᴍᴇ 𝐓ᴏ 𝐍ɪᴋɪ 𝐕ᴏɪᴄᴇ 𝐖ᴏʀʟᴅ</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"

            "🌸 <b>𝐅ʀᴇᴇ 𝐔sᴇʀ 𝐌ᴏᴅᴇ</b>\n"
            "╭━━━━━━━━━━━━━━━╮\n"
            "➜ <code>/voice hello everyone</code>\n"
            "➜ <code>/voice नमस्ते दोस्तों</code>\n"
            "╰━━━━━━━━━━━━━━━╯\n\n"

            "💎 <b>𝐏ʀᴇᴍɪᴜᴍ 𝐕ᴏɪᴄᴇ 𝐌ᴏᴅᴇ</b>\n"
            "╔════════════════╗\n"
            "👧 <code>/voice1</code> → <code>/voice5</code>\n"
            "💋 Cute Girl AI Voices\n\n"

            "👦 <code>/voice6</code> → <code>/voice10</code>\n"
            "🔥 Stylish Boy AI Voices\n"
            "╚════════════════╝\n\n"

            "🎀 <b>𝐐ᴜɪᴄᴋ 𝐕ᴏɪᴄᴇ 𝐌ᴏᴅᴇ</b>\n"
            "┏━━━━━━━━━━━━━━━┓\n"
            "👧 <code>/voicef your text</code>\n"
            "👦 <code>/voicem your text</code>\n"
            "┗━━━━━━━━━━━━━━━┛\n\n"

            "✨ <b>𝐏ʀᴇᴍɪᴜᴍ 𝐅ᴇᴀᴛᴜʀᴇs</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"

            "💎 10 Premium AI Voices\n"
            "🎭 Smart Voice Style System\n"
            "🌍 Hindi + English Support\n"
            "⚡ Ultra Fast Voice Generate\n"
            "🎤 Smooth Human Like Audio\n"
            "💞 Cute Romantic Girl Voices\n"
            "😈 Deep Stylish Boy Voices\n"
            "🧠 Smart Accent Detection\n"
            "🔥 VIP Premium Effects\n"
            "🎧 Crystal Clear Audio Quality\n"
            "📢 Telegram HD Voice Support\n"
            "💫 Auto AI Voice Styling\n"
            "🎶 Smooth Natural Speaking\n"
            "🚀 Premium Access Only Modes\n\n"

            "╔════════════════╗\n"
            " 💸 <b>𝐔ɴʟᴏᴄᴋ 𝐏ʀᴇᴍɪᴜᴍ 𝐍ᴏᴡ</b>\n"
            "╚════════════════╝\n\n"

            "✨ 𝐁ᴇᴄᴏᴍᴇ 𝐕ɪᴘ & 𝐔sᴇ 𝐍ɪᴋɪ'𝐬\n"
            "𝐌ᴏsᴛ 𝐏ᴏᴡᴇʀғᴜʟ 𝐀ɪ 𝐕ᴏɪᴄᴇ𝐬 😈💖\n\n"

            "💸 Buy Premium → /pay"
        )

        await update.message.reply_text(
            txt,
            parse_mode="HTML"
        )
        return

    text = " ".join(context.args)

    await make_voice(
        update,
        text,
        "co.in"
    )

# =========================================================
# 👧 RANDOM FEMALE
# =========================================================

async def voicef(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not is_premium(user.id):

        txt = (
            "╔═══ 💎 𝐏ʀᴇᴍɪᴜᴍ 𝐅ᴇᴍᴀʟᴇ 𝐕ᴏɪᴄᴇ 💎 ═══╗\n\n"

            "👧 <b>𝐅ᴇᴍᴀʟᴇ 𝐀ɪ 𝐕ᴏɪᴄᴇs Locked</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"

            "💖 Premium Users Can Unlock:\n\n"

            "🎤 Cute Girl AI Voices\n"
            "💋 Romantic Soft Speaking\n"
            "🌍 Hindi + English Voices\n"
            "⚡ Ultra Fast Voice System\n"
            "🎶 Smooth Audio Effects\n"
            "🔥 VIP Voice Effects\n"
            "🎧 HD Telegram Audio\n"
            "💞 Stylish Female Voice Modes\n"
            "🧠 Smart Accent AI\n"
            "💎 Exclusive Premium Voices\n\n"

            "👧 Commands:\n"
            "<code>/voice1</code> → <code>/voice5</code>\n"
            "<code>/voicef your text</code>\n\n"

            "💸 Unlock Premium → /pay"
        )

        await update.message.reply_text(
            txt,
            parse_mode="HTML"
        )
        return

    if not context.args:

        await update.message.reply_text(
            "👧 <b>𝐅ᴇᴍᴀʟᴇ 𝐕ᴏɪᴄᴇ 𝐌ᴏᴅᴇ</b>\n\n"
            "✨ Example:\n"
            "<code>/voicef hello cutie</code>\n\n"
            "💖 Random Cute Girl Voice Will Be Used",
            parse_mode="HTML"
        )
        return

    style = random.choice(list(girl_styles.values()))

    text = " ".join(context.args)

    await make_voice(
        update,
        text,
        style["tld"]
    )

# =========================================================
# 👦 RANDOM MALE
# =========================================================

async def voicem(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not is_premium(user.id):

        txt = (
            "╔═══ 💎 𝐏ʀᴇᴍɪᴜᴍ 𝐌ᴀʟᴇ 𝐕ᴏɪᴄᴇ 💎 ═══╗\n\n"

            "👦 <b>𝐌ᴀʟᴇ 𝐀ɪ 𝐕ᴏɪᴄᴇs Locked</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"

            "🔥 Premium Users Can Unlock:\n\n"

            "🎤 Deep Boy AI Voices\n"
            "😈 Stylish Male Speaking\n"
            "🌍 Hindi + English Voices\n"
            "⚡ Ultra Fast Voice System\n"
            "🎶 Smooth Audio Effects\n"
            "🔥 VIP Voice Effects\n"
            "🎧 HD Telegram Audio\n"
            "👑 Powerful Male Voice Modes\n"
            "🧠 Smart Accent AI\n"
            "💎 Exclusive Premium Voices\n\n"

            "👦 Commands:\n"
            "<code>/voice6</code> → <code>/voice10</code>\n"
            "<code>/voicem your text</code>\n\n"

            "💸 Unlock Premium → /pay"
        )

        await update.message.reply_text(
            txt,
            parse_mode="HTML"
        )
        return

    if not context.args:

        await update.message.reply_text(
            "👦 <b>𝐌ᴀʟᴇ 𝐕ᴏɪᴄᴇ 𝐌ᴏᴅᴇ</b>\n\n"
            "✨ Example:\n"
            "<code>/voicem hello bro</code>\n\n"
            "🔥 Random Stylish Boy Voice Will Be Used",
            parse_mode="HTML"
        )
        return

    style = random.choice(list(boy_styles.values()))

    text = " ".join(context.args)

    await make_voice(
        update,
        text,
        style["tld"]
    )

# =========================================================
# 💎 PREMIUM VOICE1-10
# =========================================================

async def premium_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    cmd = (
        update.message.text
        .split()[0]
        .replace("/", "")
    )

    if not is_premium(user.id):

        txt = (
            "╔═══ 💎 𝐏ʀᴇᴍɪᴜᴍ 𝐕ᴏɪᴄᴇ 💎 ═══╗\n\n"

            "🔒 <b>Premium Voice Locked</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"

            "👧 <code>/voice1</code> → <code>/voice5</code>\n"
            "💞 Cute Girl AI Voices\n\n"

            "👦 <code>/voice6</code> → <code>/voice10</code>\n"
            "🔥 Stylish Boy AI Voices\n\n"

            "✨ Premium Features:\n\n"

            "🎤 Human Like AI Voice\n"
            "🌍 Hindi + English Support\n"
            "⚡ Ultra Fast Generation\n"
            "🎧 HD Telegram Audio\n"
            "💎 VIP Voice Effects\n"
            "🧠 Smart Accent Detection\n"
            "💋 Romantic Female Voice\n"
            "😈 Deep Male Voice\n"
            "🚀 Exclusive Premium Access\n"
            "🎶 Smooth AI Audio System\n\n"

            "💸 Buy Premium → /pay"
        )

        await update.message.reply_text(
            txt,
            parse_mode="HTML"
        )
        return

    if not context.args:

        await update.message.reply_text(
            f"🎤 <b>{cmd.upper()} 𝐕ᴏɪᴄᴇ 𝐌ᴏᴅᴇ</b>\n\n"
            f"✨ Example:\n"
            f"<code>/{cmd} hello everyone</code>\n\n"
            f"💖 Premium AI Voice Ready",
            parse_mode="HTML"
        )
        return

    num = int(cmd.replace("voice", ""))

    if num <= 5:
        style = girl_styles[num]
    else:
        style = boy_styles[num]

    text = " ".join(context.args)

    await make_voice(
        update,
        text,
        style["tld"]
    )

# =========================================================
# 🎤 MAKE VOICE
# =========================================================

async def make_voice(update, text, tld):

    filename = f"voice_{random.randint(1000,9999)}.mp3"

    lang = detect_lang(text)

    tts = gTTS(
        text=text,
        lang=lang,
        tld=tld
    )

    tts.save(filename)

    lang_name = "Hindi 🇮🇳" if lang == "hi" else "English 🇺🇸"

    caption = (
        "╔═══━━━─── • ───━━━═══╗\n"
        "       🎤 𝐍ɪᴋɪ 𝐀ɪ 𝐕ᴏɪᴄᴇ 🎤\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"

        f"💬 <b>Text:</b> {text}\n"
        f"🌍 <b>Language:</b> {lang_name}\n"
        f"🎭 <b>Voice Style:</b> {tld}\n\n"

        "✨ 𝐕ᴏɪᴄᴇ 𝐆ᴇɴᴇʀᴀᴛᴇᴅ 𝐒ᴜᴄᴄᴇssғᴜʟʟʏ 💖"
    )

    await update.message.reply_voice(
        voice=open(filename, "rb"),
        caption=caption,
        parse_mode="HTML"
    )

    os.remove(filename)    

#===================ALLCOMMAND======================
async def allc(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_bot_active(update, context):
        return

    txt = (
        "╔═══━━━─── • ───━━━═══╗\n"
        "      ⚡ 𝐍ɪᴋɪ 𝐀ʟʟ 𝐂ᴏᴍᴍᴀɴᴅs ⚡\n"
        "╚═══━━━─── • ───━━━═══╝\n\n"

        "🚀 <b>𝐁ᴏᴛ 𝐒ʏsᴛᴇᴍ</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /start - 🚀 Sᴛᴀʀᴛ Tʜᴇ Bᴏᴛ Aɴᴅ Sᴇᴇ Wᴇʟᴄᴏᴍᴇ\n"
        "➜ /help - 📖 Sʜᴏᴡ Hᴇʟᴘ Mᴇɴᴜ\n"
        "➜ /allc - 📜 Vɪᴇᴡ Aʟʟ Cᴏᴍᴍᴀɴᴅs\n"
        "➜ /id - 🆔 Sʜᴏᴡ Tᴇʟᴇɢʀᴀᴍ ID\n"
        "➜ /check - 🔍 Cʜᴇᴄᴋ Uꜱᴇʀ Sᴛᴀᴛᴜs\n"
        "➜ /userinfo - 👤 Vɪᴇᴡ Uꜱᴇʀ Iɴғᴏ\n"
        "➜ /admin - 👑 Sʜᴏᴡ Aᴅᴍɪɴ Lɪsᴛ\n"
        "➜ /close - 🔒 Tᴜʀɴ Oғғ Bᴏᴛ\n"
        "➜ /open - 🔓 Tᴜʀɴ Oɴ Bᴏᴛ\n\n"

        "💰 <b>𝐄ᴄᴏɴᴏᴍʏ</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /pay - 💸 Tʀᴀɴsғᴇʀ Mᴏɴᴇʏ\n"
        "➜ /bal - 💰 Cʜᴇᴄᴋ Bᴀʟᴀɴᴄᴇ\n"
        "➜ /daily - 🎁 Cʟᴀɪᴍ Dᴀɪʟʏ\n"
        "➜ /claim - 🏆 Cʟᴀɪᴍ Gʀᴏᴜᴘ Rᴇᴡᴀʀᴅ\n"
        "➜ /protect - 🛡️ Bᴜʏ Pʀᴏᴛᴇᴄᴛɪᴏɴ\n"
        "➜ /rob - 🕵️ Rᴏʙ A Usᴇʀ\n"
        "➜ /kill - ☠️ Kɪʟʟ A Usᴇʀ\n"
        "➜ /give - 💸 Gɪᴠᴇ Mᴏɴᴇʏ\n"
        "➜ /bail - 🔓 Bᴀɪʟ Yᴏᴜʀsᴇʟғ\n"
        "➜ /shop - 🛒 Vɪᴇᴡ Sʜᴏᴘ\n"
        "➜ /gift - 🎀 Sᴇɴᴅ Gɪғᴛ\n"
        "➜ /toprich - 👑 Rɪᴄʜᴇsᴛ Pʟᴀʏᴇʀs\n"
        "➜ /topkill - ⚔️ Tᴏᴘ Kɪʟʟᴇʀs\n"
        "➜ /economy - 📊 Eᴄᴏɴᴏᴍʏ Mᴇɴᴜ\n"
        "➜ /revive - ❤️ Rᴇᴠɪᴠᴇ Yᴏᴜʀsᴇʟғ\n"
        "➜ /items - 🎒 Vɪᴇᴡ Iᴛᴇᴍs\n\n"

        "🎤 <b>𝐀ɪ 𝐕ᴏɪᴄᴇ</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /voice - 🎤 Nᴏʀᴍᴀʟ Vᴏɪᴄᴇ\n"
        "➜ /voicef - 👧 Fᴇᴍᴀʟᴇ Vᴏɪᴄᴇ\n"
        "➜ /voicem - 👦 Mᴀʟᴇ Vᴏɪᴄᴇ\n"
        "➜ /voice1 - 👧 Gɪʀʟ Vᴏɪᴄᴇ 1\n"
        "➜ /voice2 - 👧 Gɪʀʟ Vᴏɪᴄᴇ 2\n"
        "➜ /voice3 - 👧 Gɪʀʟ Vᴏɪᴄᴇ 3\n"
        "➜ /voice4 - 👧 Gɪʀʟ Vᴏɪᴄᴇ 4\n"
        "➜ /voice5 - 👧 Gɪʀʟ Vᴏɪᴄᴇ 5\n"
        "➜ /voice6 - 👦 Bᴏʏ Vᴏɪᴄᴇ 1\n"
        "➜ /voice7 - 👦 Bᴏʏ Vᴏɪᴄᴇ 2\n"
        "➜ /voice8 - 👦 Bᴏʏ Vᴏɪᴄᴇ 3\n"
        "➜ /voice9 - 👦 Bᴏʏ Vᴏɪᴄᴇ 4\n"
        "➜ /voice10 - 👦 Bᴏʏ Vᴏɪᴄᴇ 5\n\n"

        "💖 <b>𝐋ᴏᴠᴇ & 𝐑ᴇᴀᴄᴛɪᴏɴ</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /kiss - 😘 Kɪss A Usᴇʀ\n"
        "➜ /hug - 🤗 Hᴜɢ A Usᴇʀ\n"
        "➜ /slap - 😂 Sʟᴀᴘ A Usᴇʀ\n"
        "➜ /kick - 😆 Kɪᴄᴋ A Usᴇʀ\n"
        "➜ /pat - 🥰 Pᴀᴛ A Usᴇʀ\n"
        "➜ /punch - 👊 Pᴜɴᴄʜ A Usᴇʀ\n"
        "➜ /bite - 😋 Bɪᴛᴇ A Usᴇʀ\n"
        "➜ /cuddle - 💞 Cᴜᴅᴅʟᴇ A Usᴇʀ\n"
        "➜ /poke - 👉 Pᴏᴋᴇ A Usᴇʀ\n"
        "➜ /tickle - 🤣 Tɪᴄᴋʟᴇ A Usᴇʀ\n"
        "➜ /love - ❤️ Lᴏᴠᴇ Cᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ\n"
        "➜ /couple - 💑 Tᴏᴅᴀʏ's Cᴏᴜᴘʟᴇ\n"
        "➜ /couplehistory - 📜 Cᴏᴜᴘʟᴇ Hɪsᴛᴏʀʏ\n"
        "➜ /coupleleaderboard - 🏆 Cᴏᴜᴘʟᴇ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ\n"
        "➜ /propose - 💍 Pʀᴏᴘᴏsᴇ Tᴏ A Usᴇʀ\n"
        "➜ /partner - 💑 Vɪᴇᴡ Pᴀʀᴛɴᴇʀ\n"
        "➜ /profile - 👤 Mᴀʀʀɪᴀɢᴇ Pʀᴏғɪʟᴇ\n"
        "➜ /marriagehistory - 📜 Mᴀʀʀɪᴀɢᴇ Hɪsᴛᴏʀʏ\n"
        "➜ /divorce - 💔 Dɪᴠᴏʀᴄᴇ Pᴀʀᴛɴᴇʀ\n\n"

        "🎮 <b>𝐆ᴀᴍᴇs</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /dice - 🎲 Tʀʏ Yᴏᴜʀ Lᴜᴄᴋ\n"
        "➜ /coin - 🪙 Fʟɪᴘ A Cᴏɪɴ\n"
        "➜ /duel - ⚔️ Dᴜᴇʟ A Usᴇʀ\n"
        "➜ /cduel - ⚔️ Cᴏɪɴ Dᴜᴇʟ\n"
        "➜ /slot - 🎰 Pʟᴀʏ Sʟᴏᴛ\n"
        "➜ /dart - 🎯 Pʟᴀʏ Dᴀʀᴛ\n"
        "➜ /mines - 💣 Pʟᴀʏ Mɪɴᴇs\n"
        "➜ /bomb - 💣 Sᴛᴀʀᴛ Bᴏᴍʙ Gᴀᴍᴇ\n"
        "➜ /bjoin - ➕ Jᴏɪɴ Bᴏᴍʙ Gᴀᴍᴇ\n"
        "➜ /pass - 🎯 Pᴀss Tʜᴇ Bᴏᴍʙ\n"
        "➜ /left - 🚪 Lᴇᴀᴠᴇ Gᴀᴍᴇ\n"
        "➜ /gun - 🔫 Sᴛᴀʀᴛ Gᴜɴ Gᴀᴍᴇ\n"
        "➜ /gjoin - ➕ Jᴏɪɴ Gᴜɴ Gᴀᴍᴇ\n"
        "➜ /shoot - 🎯 Sʜᴏᴏᴛ Eɴᴇᴍʏ\n"
        "➜ /slotlb - 🏆 Sʟᴏᴛ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ\n\n"

        "🔤 <b>𝐖ᴏʀᴅ 𝐆ᴀᴍᴇs</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /wordseek - 🔍 Fɪɴᴅ Hɪᴅᴅᴇɴ Wᴏʀᴅs\n"
        "➜ /new4 - 🔤 4 Lᴇᴛᴛᴇʀ Gᴀᴍᴇ\n"
        "➜ /new5 - 🔤 5 Lᴇᴛᴛᴇʀ Gᴀᴍᴇ\n"
        "➜ /new6 - 🔤 6 Lᴇᴛᴛᴇʀ Gᴀᴍᴇ\n"
        "➜ /end - 🛑 Eɴᴅ Gᴀᴍᴇ\n"
        "➜ /wordlb - 🏆 Wᴏʀᴅ Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ\n"
        "➜ /wprofile - 👤 Wᴏʀᴅ Pʀᴏғɪʟᴇ\n"
        "➜ /wbadges - 🎖️ Wᴏʀᴅ Bᴀᴅɢᴇs\n\n"

        "🛡️ <b>𝐌ᴏᴅᴇʀᴀᴛɪᴏɴ</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /ban - 🔨 Bᴀɴ A Usᴇʀ\n"
        "➜ /unban - ♻️ Uɴʙᴀɴ A Usᴇʀ\n"
        "➜ /mute - 🔇 Mᴜᴛᴇ A Usᴇʀ\n"
        "➜ /unmute - 🔊 Uɴᴍᴜᴛᴇ A Usᴇʀ\n"
        "➜ /tmute - ⏳ Tɪᴍᴇ Mᴜᴛᴇ\n"
        "➜ /tban - ⏳ Tɪᴍᴇ Bᴀɴ\n\n"

        "🧩 <b>𝐄xᴛʀᴀ</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "➜ /own - 🧩 Mᴀᴋᴇ Sᴛɪᴄᴋᴇʀ\n"
        "➜ /filter - 📌 Sᴀᴠᴇ Fɪʟᴛᴇʀ\n"
        "➜ /dfilter - 🗑️ Dᴇʟᴇᴛᴇ Fɪʟᴛᴇʀ\n"
        "➜ /tr - 🌐 Tʀᴀɴsʟᴀᴛᴇ Tᴇxᴛ\n\n"

        "╔════════════════╗\n"
        " 💖 𝐍ɪᴋɪ 𝐁ᴏᴛ 𝐈s 𝐀ʟᴡᴀʏs 𝐑ᴇᴀᴅʏ 💖\n"
        "╚════════════════╝"
    )

    await update.message.reply_text(
        txt,
        parse_mode="HTML"
)

#=====================WORD GAME=========================

import random
import time
import string
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# ===================== GAME STATE =====================

word_game = {
    "active": False,
    "players": {},
    "entry": 0,
    "join_end": 0,
    "word": None,
    "start_time": 0,
    "bets": {},
    "started": False
}

# ===================== RANDOM WORD =====================

def generate_word():
    letters = string.ascii_lowercase
    word = ''.join(random.choice(letters) for _ in range(10))
    return word.upper() if random.choice([True, False]) else word.lower()

# ===================== REFUND =====================

async def refund_all():
    for uid, bet in word_game["bets"].items():
        user_data = get_user(uid, "user")
        balance = user_data.get("money", 0)
        user_data["money"] = balance + bet
    save_data()

# ===================== TIMER (AUTO CANCEL) =====================

async def game_timer():
    await asyncio.sleep(40)

    # already started → ignore
    if word_game["started"]:
        return

    # cancel condition
    if len(word_game["players"]) < 2:

        await refund_all()

        word_game["players"] = {}
        word_game["bets"] = {}
        word_game["active"] = False
        word_game["started"] = False

        print("❌ GAME CANCELLED + REFUND DONE")

# ===================== START COMMAND =====================

async def wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if not context.args:
        await update.message.reply_text(
            "⌯ » 𝙒𝙊𝙍𝘿 𝙂𝘼𝙈𝙀\n\n⚠️ ᴜsᴀɢᴇ: /wordgame <amount>"
        )
        return

    amount = context.args[0]

    if not amount.isdigit():
        await update.message.reply_text("⚠️ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ")
        return

    amount = int(amount)

    word_game["active"] = False
    word_game["started"] = False
    word_game["players"] = {}
    word_game["bets"] = {}
    word_game["entry"] = amount
    word_game["word"] = generate_word()
    word_game["join_end"] = time.time() + 40

    await update.message.reply_text(
        "⌯ » 𝙒𝙊𝙍𝘿 𝙂𝘼𝙈𝙀\n\n"
        "⌛ 40s JOIN OPEN\n"
        f"💰 ENTRY: {amount}\n"
        "👥 MAX: 2 PLAYERS\n\n"
        "👉 /enter " + str(amount)
    )

    # start timer
    asyncio.create_task(game_timer())

# ===================== ENTER COMMAND =====================

# ===================== ENTER COMMAND =====================

async def enter(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user = update.effective_user
    user_data = get_user(user.id, user.first_name)

    # already joined
    if user.id in word_game["players"]:
        await update.message.reply_text("⚠️ ᴀʟʀᴇᴀᴅʏ ᴊᴏɪɴᴇᴅ")
        return

    # full check
    if len(word_game["players"]) >= 2:
        await update.message.reply_text("🚫 ɢᴀᴍᴇ ғᴜʟʟ")
        return

    # balance check
    if user_data.get("money", 0) < word_game["entry"]:
        await update.message.reply_text("💸 ɪɴsᴜғғɪᴄɪᴇɴᴛ ʙᴀʟᴀɴᴄᴇ")
        return

    # deduct bet
    user_data["money"] -= word_game["entry"]

    # add player
    word_game["players"][user.id] = user.first_name
    word_game["bets"][user.id] = word_game["entry"]

    save_data()

    await update.message.reply_text(
        f"✅ {user.first_name} ᴊᴏɪɴᴇᴅ\n💰 ʙᴇᴛ: {word_game['entry']}\n👥 ᴡᴀɪᴛɪɴɢ..."
    )

    # 🔥 IMPORTANT AUTO START CALL
    await check_instant_start(update, context)


# ===================== INSTANT START =====================

async def check_instant_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(word_game["players"]) == 2 and not word_game.get("started"):

        word_game["started"] = True
        word_game["active"] = True
        word_game["start_time"] = time.time()

        await update.message.reply_text(
            "🔥 𝙂𝘼𝙈𝙀 𝙎𝙏𝘼𝙍𝙏𝙀𝘿\n\n"
            "⚡ 2 ᴘʟᴀʏᴇʀs ᴄᴏᴍᴘʟᴇᴛᴇ",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👀 SEE WORD", callback_data="see_word")]
            ])
        )


# ===================== SEE. (POPUP FIXED) =====================

async def see_word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if not word_game.get("started"):
        await query.answer("🚫 Game not started", show_alert=True)
        return

    if not word_game.get("word"):
        await query.answer("⚠️ Word missing", show_alert=True)
        return

    await query.answer(
        text=f"🔐 WORD: {word_game['word']}",
        show_alert=True
    )

# ===================== BUTTON ROUTER (MAIN SAFE HUB) =====================

async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    data = query.data

    # ❌ DON'T TOUCH WORD GAME CALLBACK
    if data == "see_word":
        return

    await query.answer()
# ===================== WIN CHECK =====================

async def check_word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    if not word_game["active"]:
        return

    user = update.effective_user
    text = update.message.text

    if text.lower() == word_game["word"].lower():

        word_game["active"] = False

        bet = word_game["bets"].get(user.id, 0)
        reward = bet * 2

        user_data = get_user(user.id, user.first_name)
        user_data["money"] = user_data.get("money", 0) + reward

        save_data()

        await update.message.reply_text(
            "🏆 𝙂𝘼𝙈𝙀 𝙊𝙑𝙀𝙍\n\n"
            f"🎯 ᴡɪɴɴᴇʀ: {user.first_name}\n"
            f"💰 ʙᴇᴛ: {bet}\n"
            f"💸 ʀᴇᴡᴀʀᴅ: {reward}\n"
            f"🔑 ᴡᴏʀᴅ: {word_game['word']}"
        )



#====================ping========================
# ================= PING COMMAND =================
import time

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    start = time.time()

    msg = await update.message.reply_text(
        """
╔═══━━━─── • ───━━━═══╗
      🏓 𝐏𝐈𝐍𝐆𝐈𝐍𝐆 🏓
╚═══━━━─── • ───━━━═══╝

⚡ Cʜᴇᴄᴋɪɴɢ Sᴇʀᴠᴇʀ Sᴘᴇᴇᴅ...
"""
    )

    end = time.time()

    ping_ms = round((end - start) * 1000)

    # ================= FAST =================
    if ping_ms <= 150:

        text = f"""
╔═══━━━─── • ───━━━═══╗
        🏓 𝐏𝐈𝐍𝐆 🏓
╚═══━━━─── • ───━━━═══╝

⚡ 𝐒ᴘᴇᴇᴅ:
{ping_ms} ms

🚀 𝐍ɪᴋɪ 𝐈s 𝐑ᴜɴɴɪɴɢ
𝐒ᴜᴘᴇʀ Fᴀsᴛ 😈
"""

    # ================= NORMAL =================
    elif ping_ms <= 500:

        text = f"""
╔═══━━━─── • ───━━━═══╗
        🏓 𝐏𝐈𝐍𝐆 🏓
╚═══━━━─── • ───━━━═══╝

😎 𝐒ᴘᴇᴇᴅ:
{ping_ms} ms

✨ 𝐒ᴇʀᴠᴇʀ 𝐈s 𝐒ᴛᴀʙʟᴇ
𝐀ɴᴅ 𝐖ᴏʀᴋɪɴɢ Fɪɴᴇ!
"""

    # ================= SLOW =================
    else:

        text = f"""
╔═══━━━─── • ───━━━═══╗
        🏓 𝐏𝐈𝐍𝐆 🏓
╚═══━━━─── • ───━━━═══╝

🐢 𝐒ᴘᴇᴇᴅ:
{ping_ms} ms

⚠️ 𝐒ᴇʀᴠᴇʀ 𝐈s 𝐀 𝐁ɪᴛ 𝐒ʟᴏᴡ...

💤 𝐍ɪᴋɪ 𝐈s 𝐓ʀʏɪɴɢ
𝐓ᴏ 𝐑ᴇsᴘᴏɴᴅ Fᴀsᴛ 😭
"""

    await msg.edit_text(text)




# =========================================================
#                 NIKI HACK GAME FINAL
# =========================================================
# FEATURES:
# ✅ Stylish Hack Game
# ✅ Unlimited Players
# ✅ Manual /starthack
# ✅ Host/Admin /endhack
# ✅ Real Balance System
# ✅ Auto Turn System
# ✅ Auto Kick After 2 Skips
# ✅ Auto Win If 1 Player Left
# ✅ Winner DP + Auto Pin
# ✅ Hack Loading Animation

# =========================================================
#                    GAME STORAGE
# =========================================================

hack_games = {}


# =========================================================
#                   USER MENTION
# =========================================================

def uname(user):
    return mention_html(user.id, user.first_name)


# =========================================================
#                 BALANCE SYSTEM
# =========================================================

def get_balance(user_id):
    user = get_user(user_id, "Player")
    return user.get("money", 0)


def add_balance(user_id, amount):
    user = get_user(user_id, "Player")
    user["money"] = user.get("money", 0) + amount
    save_data()


def remove_balance(user_id, amount):
    user = get_user(user_id, "Player")
    user["money"] = user.get("money", 0) - amount
    save_data()


# =========================================================
#                 PASSWORD GENERATOR
# =========================================================

def generate_password(length):
    return "".join(random.choice("0123456789") for _ in range(length))


# =========================================================
#               HACKS & GLITCHES (SAFE FIXED)
# =========================================================

def calculate_result(secret, guess):

    hacks = 0
    glitches = 0

    secret_used = []
    guess_used = []

    # SAFE LOOP (avoid index crash)
    for i in range(min(len(secret), len(guess))):

        if guess[i] == secret[i]:
            hacks += 1
            secret_used.append(i)
            guess_used.append(i)

    for i in range(len(guess)):

        if i in guess_used:
            continue

        for j in range(len(secret)):

            if j in secret_used:
                continue

            if guess[i] == secret[j]:
                glitches += 1
                secret_used.append(j)
                break

    return hacks, glitches
# =========================================================
#                    NEXT TURN
# =========================================================

async def next_turn(chat_id, context):

    game = hack_games.get(chat_id)

    if not game:
        return

    game["players"] = [
        p for p in game["players"]
        if p["active"]
    ]

    active_players = [
        p for p in game["players"]
        if p["active"]
    ]

    # ================= FIX START =================
    game["turn_active"] = True

    if "turn_id" not in game:
        game["turn_id"] = 0

    game["turn_id"] += 1
    current_turn_id = game["turn_id"]
    # ================= FIX END =================

    # =====================================================
    #            AUTO WIN IF 1 PLAYER LEFT
    # =====================================================

    if len(active_players) == 1:

        winner = active_players[0]

        prize = (
            game["entry_fee"] *
            len(game["players"])
        )

        add_balance(
            winner["id"],
            prize
        )

        balance = get_balance(
            winner["id"]
        )

        caption = (
            "╔══════════════════╗\n"
            "   🏆 𝘼𝙐𝙏𝙊 𝙃𝘼𝘾𝙆 𝙒𝙄𝙉\n"
            "╚══════════════════╝\n\n"

            f"👑 𝙇𝙖𝙨𝙩 𝙃𝙖𝙘𝙠𝙚𝙧:\n"
            f"{winner['name']}\n\n"

            f"💰 𝙍𝙚𝙬𝙖𝙧𝙙:\n"
            f"➥ {prize}\n\n"

            f"🏦 𝙉𝙚𝙬 𝘽𝙖𝙡𝙖𝙣𝙘𝙚:\n"
            f"➥ {balance}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "💻 𝘼𝙡𝙡 𝙊𝙩𝙝𝙚𝙧 𝙃𝙖𝙘𝙠𝙚𝙧𝙨 𝙀𝙡𝙞𝙢𝙞𝙣𝙖𝙩𝙚𝙙\n"
            "🛰 𝙎𝙮𝙨𝙩𝙚𝙢 𝘼𝙘𝙘𝙚𝙨𝙨 𝙂𝙧𝙖𝙣𝙩𝙚𝙙\n"
            "⚡ 𝙇𝙖𝙨𝙩 𝙃𝙖𝙘𝙠𝙚𝙧 𝙎𝙩𝙖𝙣𝙙𝙞𝙣𝙜"
        )

        photos = await context.bot.get_user_profile_photos(
            winner["id"],
            limit=1
        )

        if photos.total_count > 0:

            file_id = photos.photos[0][-1].file_id

            sent = await context.bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode="HTML"
            )

        else:

            sent = await context.bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode="HTML"
            )

        try:
            await context.bot.pin_chat_message(
                chat_id=chat_id,
                message_id=sent.message_id
            )
        except:
            pass

        del hack_games[chat_id]
        return

# =====================================================
    #                 NO PLAYERS LEFT
    # =====================================================

    if len(game["players"]) == 0:

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "🔒 <b>SYSTEM LOCKOUT</b>\n\n"
                "❌ No hackers left.\n"
                "💻 Hack terminated."
            ),
            parse_mode="HTML"
        )

        del hack_games[chat_id]
        return

    # =====================================================
    #               TURN INDEX SAFE CHECK
    # =====================================================

    if game["turn_index"] >= len(game["players"]):
        game["turn_index"] = 0

    player = game["players"][game["turn_index"]]

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "╔══════════════════╗\n"
            "     🎯 𝙔𝙊𝙐𝙍 𝙏𝙐𝙍𝙉\n"
            "╚══════════════════╝\n\n"

            f"👤 𝙃𝙖𝙘𝙠𝙚𝙧:\n"
            f"{player['name']}\n\n"

            "⏳ 𝙏𝙞𝙢𝙚 𝙇𝙞𝙢𝙞𝙩:\n"
            "➥ 60 Seconds\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "💻 𝙏𝙮𝙥𝙚 𝙔𝙤𝙪𝙧 𝙃𝙖𝙘𝙠:\n\n"

            f"/guess {'1'*game['digits']}\n\n"

            "⚡ 𝙁𝙖𝙞𝙡 𝙏𝙤 𝙍𝙚𝙨𝙥𝙤𝙣𝙙 = 𝙎𝙠𝙞𝙥"
        ),
        parse_mode="HTML"
    )

    # ================= FIX START =================
    current_turn_id = game.get("turn_id", 0)

    asyncio.create_task(
        turn_timer(chat_id, player["id"], current_turn_id, context)
    )
    # ================= FIX END =================


# =========================================================
#                    TURN TIMER (FIXED SAFE)
# =========================================================

async def turn_timer(chat_id, user_id, turn_id, context):

    await asyncio.sleep(60)

    game = hack_games.get(chat_id)

    if not game:
        return

    # ❌ IGNORE OLD TURN TIMER
    if game.get("turn_id") != turn_id:
        return

    # ❌ IF TURN ALREADY CHANGED
    if not game.get("turn_active", True):
        return

    # ❌ SAFETY CHECK PLAYER EXISTENCE
    if game["turn_index"] >= len(game["players"]):
        return

    current = game["players"][game["turn_index"]]

    if current["id"] != user_id:
        return

    # ================= TURN END =================
    game["turn_active"] = False

    current["skips"] = current.get("skips", 0) + 1
# =====================================================
    #                     REMOVE PLAYER
    # =====================================================

    current["skips"] = current.get("skips", 0)

    if current["skips"] >= 2:

        current["active"] = False

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "⚠️ <b>𝙃𝘼𝘾𝙆𝙀𝙍 𝙍𝙀𝙈𝙊𝙑𝙀𝘿</b>\n\n"

                f"👤 {current['name']}\n"
                "𝙢𝙞𝙨𝙨𝙚𝙙 2 𝙩𝙪𝙧𝙣𝙨.\n\n"

                "🚫 𝙉𝙤 𝙧𝙚𝙛𝙪𝙣𝙙."
            ),
            parse_mode="HTML"
        )

    else:

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"⏳ {current['name']} "
                f"𝙢𝙞𝙨𝙨𝙚𝙙 𝙩𝙝𝙚𝙞𝙧 𝙩𝙪𝙧𝙣.\n\n"

                f"⚠️ 𝙎𝙠𝙞𝙥𝙨: {current['skips']}/2"
            ),
            parse_mode="HTML"
        )

    # =====================================================
    #               SAFE TURN MOVE FIX
    # =====================================================

    game["turn_index"] += 1

    if game["turn_index"] >= len(game["players"]):
        game["turn_index"] = 0

    await next_turn(chat_id, context)
# =========================================================
#                       /hack
# =========================================================

# =========================================================
#                       /hack
# =========================================================

async def hack(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id in hack_games:

        return await update.message.reply_text(
            "⚠️ Hack game already running."
        )

    args = context.args

    if len(args) != 2:

        return await update.message.reply_text(
            (
                "╔══════════════════╗\n"
                "  ❌ 𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝘾𝙊𝙈𝙈𝘼𝙉𝘿\n"
                "╚══════════════════╝\n\n"

                "💡 𝙐𝙨𝙖𝙜𝙚:\n"
                "/hack <amount> <digits>\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "🔐 𝘿𝙞𝙜𝙞𝙩 𝙇𝙞𝙢𝙞𝙩:\n"
                "3 ➠ 6 𝘿𝙞𝙜𝙞𝙩𝙨\n\n"

                "💰 𝙈𝙞𝙣𝙞𝙢𝙪𝙢 𝙀𝙣𝙩𝙧𝙮:\n"
                "500\n\n"

                "🧠 𝙀𝙭𝙖𝙢𝙥𝙡𝙚:\n"
                "/hack 500 6"
            )
        )

    try:

        amount = int(args[0])
        digits = int(args[1])

    except:

        return await update.message.reply_text(
            "❌ Invalid numbers."
        )

    if amount < 500:

        return await update.message.reply_text(
            "❌ Minimum amount is 500."
        )

    if digits < 3 or digits > 6:

        return await update.message.reply_text(
            "❌ Digits must be between 3-6."
        )

    hack_games[chat_id] = {

        "host": update.effective_user.id,

        "password": generate_password(digits),

        "digits": digits,

        "entry_fee": amount,

        "players": [],

        "turn_index": 0,

        "started": False,

        "guesses_left": 200,

        "turn_active": False,
        "turn_id": 0
    }

    await update.message.reply_text(
        (
            "╔══════════════════╗\n"
            "     💻 𝙃𝘼𝘾𝙆 𝙇𝙊𝘽𝘽𝙔\n"
            "╚══════════════════╝\n\n"

            f"👑 𝙃𝙤𝙨𝙩:\n"
            f"{uname(update.effective_user)}\n\n"

            f"💰 𝙀𝙣𝙩𝙧𝙮 𝙁𝙚𝙚:\n"
            f"➥ {amount}\n\n"

            f"🔐 𝙋𝙖𝙨𝙨𝙘𝙤𝙙𝙚 𝙇𝙚𝙣𝙜𝙩𝙝:\n"
            f"➥ {digits} 𝘿𝙞𝙜𝙞𝙩𝙨\n\n"

            "👥 𝙈𝙞𝙣𝙞𝙢𝙪𝙢 𝙃𝙖𝙘𝙠𝙚𝙧𝙨:\n"
            "➥ 2 𝙋𝙡𝙖𝙮𝙚𝙧𝙨\n\n"

            "🎯 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙋𝙤𝙤𝙡:\n"
            "➥ 0\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "📡 𝙃𝙖𝙘𝙠 𝙎𝙚𝙧𝙫𝙚𝙧: 𝙊𝙣𝙡𝙞𝙣𝙚\n"
            "🛰 𝙏𝙖𝙧𝙜𝙚𝙩 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮: 𝙇𝙤𝙘𝙠𝙚𝙙\n"
            "⚡ 𝙒𝙖𝙞𝙩𝙞𝙣𝙜 𝙁𝙤𝙧 𝙃𝙖𝙘𝙠𝙚𝙧𝙨\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            f"👉 𝙅𝙤𝙞𝙣 𝙐𝙨𝙞𝙣𝙜:\n"
            f"/register {amount}"
        ),
        parse_mode="HTML"
    )

# =========================================================
#                    /register
# =========================================================

# =========================================================
#                    /register
# =========================================================

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    game = hack_games.get(chat_id)

    if not game:

        return await update.message.reply_text(
            "❌ 𝙉𝙤 𝙖𝙘𝙩𝙞𝙫𝙚 𝙝𝙖𝙘𝙠 𝙡𝙤𝙗𝙗𝙮."
        )

    if game["started"]:

        return await update.message.reply_text(
            "🚫 𝙃𝙖𝙘𝙠 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙨𝙩𝙖𝙧𝙩𝙚𝙙."
        )

    args = context.args

    if len(args) != 1:

        return await update.message.reply_text(
            f"💡 𝙐𝙨𝙚:\n/register {game['entry_fee']}"
        )

    try:

        amount = int(args[0])

    except:

        return await update.message.reply_text(
            "❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙖𝙢𝙤𝙪𝙣𝙩."
        )

    if amount != game["entry_fee"]:

        return await update.message.reply_text(
            (
                "❌ 𝙒𝙧𝙤𝙣𝙜 𝙚𝙣𝙩𝙧𝙮 𝙖𝙢𝙤𝙪𝙣𝙩.\n\n"
                f"👉 𝙐𝙨𝙚:\n/register {game['entry_fee']}"
            )
        )

    # =====================================================
    #                  ALREADY JOINED
    # =====================================================

    for p in game["players"]:

        if p["id"] == user.id:

            return await update.message.reply_text(
                "⚠️ 𝙔𝙤𝙪 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙟𝙤𝙞𝙣𝙚𝙙."
            )

# =====================================================
    #                    BALANCE CHECK
    # =====================================================

    if get_balance(user.id) < amount:

        return await update.message.reply_text(
            (
                "❌ 𝙄𝙣𝙨𝙪𝙛𝙛𝙞𝙘𝙞𝙚𝙣𝙩 𝘽𝙖𝙡𝙖𝙣𝙘𝙚\n\n"

                f"💰 𝙉𝙚𝙚𝙙: {amount}\n"
                f"🏦 𝙔𝙤𝙪 𝙃𝙖𝙫𝙚: {get_balance(user.id)}"
            )
        )

    remove_balance(user.id, amount)

    game["players"].append({

        "id": user.id,

        "name": uname(user),

        "skips": 0,

        "active": True
    })

    total = len(game["players"])

    prize = (
        game["entry_fee"] * total
    )

    await update.message.reply_text(
        (
            "╔══════════════════╗\n"
            "   👤 𝙃𝘼𝘾𝙆𝙀𝙍 𝙅𝙊𝙄𝙉𝙀𝘿\n"
            "╚══════════════════╝\n\n"

            f"🕶 𝙃𝙖𝙘𝙠𝙚𝙧:\n"
            f"{uname(user)}\n\n"

            f"💰 𝙀𝙣𝙩𝙧𝙮 𝘿𝙚𝙙𝙪𝙘𝙩𝙚𝙙:\n"
            f"➥ {amount}\n\n"

            f"👥 𝙏𝙤𝙩𝙖𝙡 𝙃𝙖𝙘𝙠𝙚𝙧𝙨:\n"
            f"➥ {total}\n\n"

            f"🏆 𝙋𝙧𝙞𝙯𝙚 𝙋𝙤𝙤𝙡:\n"
            f"➥ {prize}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "📡 𝙃𝙖𝙘𝙠 𝙎𝙚𝙖𝙩 𝙍𝙚𝙨𝙚𝙧𝙫𝙚𝙙\n"
            "⚡ 𝘼𝙘𝙘𝙚𝙨𝙨 𝙂𝙧𝙖𝙣𝙩𝙚𝙙\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "🚀 𝙄𝙛 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙎𝙩𝙖𝙧𝙩 𝙃𝙖𝙘𝙠\n"
            "👑 𝙃𝙤𝙨𝙩 𝘾𝙖𝙣 𝙏𝙮𝙥𝙚:\n\n"

            "/starthack"
        ),
        parse_mode="HTML"
    )

# =========================================================
#                   /starthack
# =========================================================

# =========================================================
#                   /starthack
# =========================================================

async def starthack(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    game = hack_games.get(chat_id)

    if not game:

        return await update.message.reply_text(
            "❌ 𝙉𝙤 𝙖𝙘𝙩𝙞𝙫𝙚 𝙝𝙖𝙘𝙠 𝙡𝙤𝙗𝙗𝙮."
        )

    # HOST ONLY
    if user_id != game["host"]:

        return await update.message.reply_text(
            "🚫 𝙊𝙣𝙡𝙮 𝙃𝙤𝙨𝙩 𝘾𝙖𝙣 𝙎𝙩𝙖𝙧𝙩 𝙃𝙖𝙘𝙠."
        )

    if game["started"]:

        return await update.message.reply_text(
            "⚠️ 𝙃𝙖𝙘𝙠 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙨𝙩𝙖𝙧𝙩𝙚𝙙."
        )

    total = len(game["players"])

    # =====================================================
    #                  NEED 2 PLAYERS
    # =====================================================

    if total < 2:

        return await update.message.reply_text(
            (
                "╔══════════════════╗\n"
                "   ❌ 𝙎𝙏𝘼𝙍𝙏 𝙁𝘼𝙄𝙇𝙀𝘿\n"
                "╚══════════════════╝\n\n"

                "👥 𝙈𝙞𝙣𝙞𝙢𝙪𝙢 2 𝙃𝙖𝙘𝙠𝙚𝙧𝙨 𝙉𝙚𝙚𝙙𝙚𝙙\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                f"📡 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙃𝙖𝙘𝙠𝙚𝙧𝙨:\n"
                f"➥ {total}/2\n\n"

                "⚡ 𝙄𝙣𝙫𝙞𝙩𝙚 𝙈𝙤𝙧𝙚 𝙃𝙖𝙘𝙠𝙚𝙧𝙨"
            )
        )

    # ================= FIX (UNCHANGED LOGIC) =================
    game["started"] = True
    game["turn_index"] = 0
    game["guesses_left"] = game.get("guesses_left", 200)

    game["turn_active"] = False
    game["turn_id"] = 0
    # =========================================================

    prize = (
        game["entry_fee"] *
        total
    )

    await update.message.reply_text(
        (
            "╔══════════════════╗\n"
            "   🚀 𝙃𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏𝙀𝘿\n"
            "╚══════════════════╝\n\n"

            f"🔐 𝙋𝙖𝙨𝙨𝙘𝙤𝙙𝙚:\n"
            f"➥ {game['digits']} 𝘿𝙞𝙜𝙞𝙩𝙨\n\n"

            f"👥 𝙃𝙖𝙘𝙠𝙚𝙧𝙨:\n"
            f"➥ {total}\n\n"

            f"🏆 𝙋𝙧𝙞𝙯𝙚 𝙋𝙤𝙤𝙡:\n"
            f"➥ {prize}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "🛰 𝙁𝙞𝙧𝙚𝙬𝙖𝙡𝙡 𝘼𝙘𝙩𝙞𝙫𝙚\n"
            "⚡ 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮 𝙇𝙤𝙘𝙠𝙚𝙙\n"
            "💻 𝘽𝙚𝙜𝙞𝙣 𝙃𝙖𝙘𝙠𝙞𝙣𝙜...\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            f"👉 𝙐𝙨𝙚:\n"
            f"/guess {'1'*game['digits']}"
        ),
        parse_mode="HTML"
    )

    await next_turn(chat_id, context)
# =========================================================
#                      /guess
# =========================================================

# =========================================================
#                      /guess
# =========================================================

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user = update.effective_user

    game = hack_games.get(chat_id)

    if not game:
        return

    if not game["started"]:
        return

    args = context.args

    if len(args) != 1:

        return await update.message.reply_text(
            f"💡 𝙐𝙨𝙚:\n/guess {'1'*game['digits']}"
        )

    guess_code = args[0]

    if not guess_code.isdigit():

        return await update.message.reply_text(
            "❌ 𝘿𝙞𝙜𝙞𝙩𝙨 𝙤𝙣𝙡𝙮."
        )

    if len(guess_code) != game["digits"]:

        return await update.message.reply_text(
            (
                "🚫 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙂𝙪𝙚𝙨𝙨\n\n"

                f"🔐 𝙀𝙣𝙩𝙚𝙧 𝙚𝙭𝙖𝙘𝙩𝙡𝙮 "
                f"{game['digits']} 𝙙𝙞𝙜𝙞𝙩𝙨."
            )
        )

    current = game["players"][game["turn_index"]]

    if user.id != current["id"]:

        return await update.message.reply_text(
            "❌ 𝙄𝙩'𝙨 𝙣𝙤𝙩 𝙮𝙤𝙪𝙧 𝙩𝙪𝙧𝙣."
        )

    secret = game["password"]

    # ================= FIX ADD START =================
    game["turn_active"] = False

    if "turn_id" not in game:
        game["turn_id"] = 0

    game["turn_id"] += 1
    # ================= FIX ADD END =================

# =====================================================
    #                  HACK LOADING
    # =====================================================

    loading = await update.message.reply_text(
        (
            "💻 𝙄𝙣𝙞𝙩𝙞𝙖𝙡𝙞𝙯𝙞𝙣𝙜 𝙃𝙖𝙘𝙠...\n"
            "▰▱▱▱▱▱▱▱▱▱ 10%"
        )
    )

    await asyncio.sleep(1)

    await loading.edit_text(
        (
            "🛰 𝘽𝙮𝙥𝙖𝙨𝙨𝙞𝙣𝙜 𝙁𝙞𝙧𝙚𝙬𝙖𝙡𝙡...\n"
            "▰▰▰▱▱▱▱▱▱▱ 30%"
        )
    )

    await asyncio.sleep(1)

    await loading.edit_text(
        (
            "🔍 𝘿𝙚𝙘𝙧𝙮𝙥𝙩𝙞𝙣𝙜 𝙋𝙖𝙨𝙨𝙘𝙤𝙙𝙚...\n"
            "▰▰▰▰▰▰▱▱▱▱ 60%"
        )
    )

    await asyncio.sleep(1)

    await loading.edit_text(
        (
            "⚡ 𝘾𝙧𝙖𝙘𝙠𝙞𝙣𝙜 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮...\n"
            "▰▰▰▰▰▰▰▰▰▱ 90%"
        )
    )

    await asyncio.sleep(1)

    await loading.edit_text(
        (
            "✅ 𝙃𝙖𝙘𝙠 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙\n"
            "▰▰▰▰▰▰▰▰▰▰ 100%"
        )
    )

    await asyncio.sleep(1)

    # =====================================================
    #                        WIN
    # =====================================================

    if guess_code == secret:

        prize = (
            game["entry_fee"] *
            len(game["players"])
        )

        add_balance(user.id, prize)

        balance = get_balance(user.id)

        caption = (
            "╔══════════════════╗\n"
            "   🏆 𝙃𝘼𝘾𝙆 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀𝘿\n"
            "╚══════════════════╝\n\n"

            f"👑 𝙒𝙞𝙣𝙣𝙚𝙧:\n"
            f"{uname(user)}\n\n"

            f"💰 𝙍𝙚𝙬𝙖𝙧𝙙:\n"
            f"➥ {prize}\n\n"

            f"🏦 𝙉𝙚𝙬 𝘽𝙖𝙡𝙖𝙣𝙘𝙚:\n"
            f"➥ {balance}\n\n"

            f"🔓 𝙎𝙚𝙘𝙧𝙚𝙩 𝘾𝙤𝙙𝙚:\n"
            f"<code>{secret}</code>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "💻 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮 𝘽𝙧𝙚𝙖𝙘𝙝 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡\n"
            "🛰 𝘼𝙘𝙘𝙚𝙨𝙨 𝙂𝙧𝙖𝙣𝙩𝙚𝙙\n"
            "⚡ 𝙎𝙮𝙨𝙩𝙚𝙢 𝘿𝙤𝙬𝙣\n"
            "🔒 𝙃𝙖𝙘𝙠 𝙎𝙚𝙨𝙨𝙞𝙤𝙣 𝙀𝙣𝙙𝙚𝙙"
        )

        photos = await context.bot.get_user_profile_photos(
            user.id,
            limit=1
        )

        if photos.total_count > 0:

            file_id = photos.photos[0][-1].file_id

            sent = await context.bot.send_photo(
                chat_id=chat_id,
                photo=file_id,
                caption=caption,
                parse_mode="HTML"
            )

        else:

            sent = await context.bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode="HTML"
            )

        try:

            await context.bot.pin_chat_message(
                chat_id=chat_id,
                message_id=sent.message_id
            )

        except:
            pass

        del hack_games[chat_id]
        return

# =====================================================
    #                  NORMAL RESULT
    # =====================================================

    hacks, glitches = calculate_result(
        secret,
        guess_code
    )

    game["guesses_left"] -= 1

    await loading.edit_text(
        (
            "╔══════════════════╗\n"
            "   💻 𝙃𝘼𝘾𝙆 𝙍𝙀𝙎𝙐𝙇𝙏\n"
            "╚══════════════════╝\n\n"

            f"👤 𝙃𝙖𝙘𝙠𝙚𝙧:\n"
            f"{uname(user)}\n\n"

            f"🟩 𝙃𝙖𝙘𝙠𝙨:\n"
            f"➥ {hacks}\n\n"

            f"🟨 𝙂𝙡𝙞𝙩𝙘𝙝𝙚𝙨:\n"
            f"➥ {glitches}\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "📡 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮 𝙋𝙖𝙩𝙩𝙚𝙧𝙣 𝘼𝙣𝙖𝙡𝙮𝙯𝙚𝙙\n"
            "🛰 𝙁𝙞𝙧𝙚𝙬𝙖𝙡𝙡 𝘿𝙖𝙢𝙖𝙜𝙚𝙙\n"
            "⚡ 𝘼𝙣𝙤𝙩𝙝𝙚𝙧 𝘼𝙩𝙩𝙖𝙘𝙠 𝙍𝙚𝙦𝙪𝙞𝙧𝙚𝙙\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            f"⏳ 𝙂𝙪𝙚𝙨𝙨𝙚𝙨 𝙇𝙚𝙛𝙩:\n"
            f"➥ {game['guesses_left']}"
        ),
        parse_mode="HTML"
    )

    # =====================================================
    #                    GUESS LIMIT
    # =====================================================

    if game["guesses_left"] <= 0:

        await update.message.reply_text(
            (
                "🔒 𝙂𝙪𝙚𝙨𝙨 𝙇𝙞𝙢𝙞𝙩 𝙍𝙚𝙖𝙘𝙝𝙚𝙙\n\n"
                "💻 𝙃𝙖𝙘𝙠 𝙁𝙖𝙞𝙡𝙚𝙙."
            )
        )

        del hack_games[chat_id]
        return

    game["turn_index"] += 1

    await next_turn(chat_id, context)

# =========================================================
#                     /players
# =========================================================

async def players(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    game = hack_games.get(chat_id)

    if not game:

        return await update.message.reply_text(
            (
                "╔══════════════════╗\n"
                "     ❌ 𝙉𝙊 𝙃𝘼𝘾𝙆 𝙂𝘼𝙈𝙀\n"
                "╚══════════════════╝\n\n"

                "💻 𝙉𝙤 𝘼𝙘𝙩𝙞𝙫𝙚 𝙃𝙖𝙘𝙠 𝙎𝙚𝙨𝙨𝙞𝙤𝙣\n"
                "📡 𝙎𝙚𝙧𝙫𝙚𝙧 𝙄𝙙𝙡𝙚\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "🚀 𝙎𝙩𝙖𝙧𝙩 𝙉𝙚𝙬 𝙂𝙖𝙢𝙚:\n\n"
                "/hack 500 6"
            )
        )

    text = "👥 <b>𝘼𝘾𝙏𝙄𝙑𝙀 𝙃𝘼𝘾𝙆𝙀𝙍𝙎</b>\n\n"

    for i, p in enumerate(game["players"], start=1):

        if p["active"]:

            text += f"{i}. {p['name']}\n"

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


# =========================================================
#                     /hackinfo
# =========================================================

async def hackinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    game = hack_games.get(chat_id)

    if not game:

        return await update.message.reply_text(
            "❌ 𝙉𝙤 𝙖𝙘𝙩𝙞𝙫𝙚 𝙝𝙖𝙘𝙠."
        )

    prize = (
        game["entry_fee"] *
        len(game["players"])
    )

    current = game["players"][game["turn_index"]]

    # SAFE FIX (avoid crash if player list empty)
    current_name = current["name"] if current else "N/A"

    text = (
        "💻 <b>𝙃𝘼𝘾𝙆 𝙄𝙉𝙁𝙊</b>\n\n"

        f"🔐 𝘿𝙞𝙜𝙞𝙩𝙨: {game['digits']}\n"
        f"💰 𝙋𝙧𝙞𝙯𝙚 𝙋𝙤𝙤𝙡: {prize}\n"
        f"👥 𝙋𝙡𝙖𝙮𝙚𝙧𝙨: {len(game['players'])}\n"
        f"🎯 𝘾𝙪𝙧𝙧𝙚𝙣𝙩 𝙏𝙪𝙧𝙣:\n"
        f"{current_name}\n"
        f"⏳ 𝙂𝙪𝙚𝙨𝙨𝙚𝙨 𝙇𝙚𝙛𝙩: {game['guesses_left']}"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


# =========================================================
#                     /endhack
# =========================================================

async def endhack(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    game = hack_games.get(chat_id)

    if not game:

        return await update.message.reply_text(
            "❌ 𝙉𝙤 𝙖𝙘𝙩𝙞𝙫𝙚 𝙝𝙖𝙘𝙠 𝙜𝙖𝙢𝙚."
        )

    member = await context.bot.get_chat_member(
        chat_id,
        user_id
    )

    is_admin = member.status in [
        "administrator",
        "creator"
    ]

    if (
        user_id != game["host"]
        and not is_admin
    ):

        return await update.message.reply_text(
            "🚫 𝙊𝙣𝙡𝙮 𝙃𝙤𝙨𝙩 𝙊𝙧 𝘼𝙙𝙢𝙞𝙣 𝘾𝙖𝙣 𝙀𝙣𝙙 𝙃𝙖𝙘𝙠."
        )

    del hack_games[chat_id]

    await update.message.reply_text(
        (
            "╔══════════════════╗\n"
            "   🛑 𝙃𝘼𝘾𝙆 𝙀𝙉𝘿𝙀𝘿\n"
            "╚══════════════════╝\n\n"

            "💻 𝙃𝙖𝙘𝙠 𝙎𝙚𝙨𝙨𝙞𝙤𝙣 𝘾𝙡𝙤𝙨𝙚𝙙\n"
            "📡 𝙎𝙚𝙧𝙫𝙚𝙧 𝙊𝙛𝙛𝙡𝙞𝙣𝙚"
        )
    )
    

# =========================================================
#                🌌 NIKI INLINE WHISPER 🌌
# =========================================================
# FEATURES:
# ✅ Real Baka Style Inline Whisper
# ✅ Username + User ID Support
# ✅ Popup Whisper
# ✅ Anonymous Whisper
# ✅ Auto Expire
# ✅ One Time Open
# ✅ Reply System
# ✅ Stylish UI
# ✅ Inline Loading
# ✅ Anti Others Open
# =========================================================

import uuid
import time

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    InlineQueryHandler
)

# =========================================================
#                    WHISPER STORAGE
# =========================================================

whispers = {}

WHISPER_EXPIRE = 86400

# =========================================================
#                  CLEANUP EXPIRED
# =========================================================

def cleanup_whispers():

    now = time.time()

    expired = []

    for wid, data in whispers.items():

        if now - data["time"] > WHISPER_EXPIRE:
            expired.append(wid)

    for wid in expired:
        whispers.pop(wid, None)

# =========================================================
#                 INLINE WHISPER
# =========================================================

async def inline_whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cleanup_whispers()

    query = update.inline_query

    if not query:
        return

    text = query.query.strip()

    # =====================================================
    # EMPTY QUERY
    # =====================================================

    if not text:

        return await query.answer(
            [],
            cache_time=1
        )

    # =====================================================
    # SPLIT
    # =====================================================

    args = text.split(maxsplit=1)

    if len(args) < 2:

        result = InlineQueryResultArticle(

            id=str(uuid.uuid4()),

            title="💌 Whisper Usage",

            description="@username message",

            input_message_content=InputTextMessageContent(
                "❌ Usage:\n\n"
                "@username hello\n\n"
                "or\n\n"
                "123456 hello"
            )
        )

        return await query.answer(
            [result],
            cache_time=1
        )

    target = args[0]
    whisper_text = args[1]

    # =====================================================
    # ANONYMOUS
    # =====================================================

    anonymous = False

    if whisper_text.startswith("-a "):

        anonymous = True
        whisper_text = whisper_text[3:]

    # =====================================================
    # TARGET
    # =====================================================

    target_username = None
    target_id = None

    if target.startswith("@"):

        target_username = target.replace("@", "").lower()

    elif target.isdigit():

        target_id = int(target)

    else:

        result = InlineQueryResultArticle(

            id=str(uuid.uuid4()),

            title="❌ Invalid Target",

            input_message_content=InputTextMessageContent(
                "Invalid username or user id."
            )
        )

        return await query.answer(
            [result],
            cache_time=1
        )

    # =====================================================
    # CREATE WHISPER
    # =====================================================

    whisper_id = str(uuid.uuid4())[:10]

    whispers[whisper_id] = {

        "text": whisper_text,

        "target_username": target_username,
        "target_id": target_id,

        "sender_name": query.from_user.first_name,
        "sender_id": query.from_user.id,

        "anonymous": anonymous,

        "time": time.time(),

        "opened": False
    }

    # =====================================================
    # TARGET SHOW
    # =====================================================

    if target_username:

        target_show = f"@{target_username}"

    else:

        target_show = str(target_id)

    # =====================================================
    # BUTTONS
    # =====================================================

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "💌 Open Whisper",
                callback_data=f"openwhisper_{whisper_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "↩️ Reply",
                callback_data=f"replywhisper_{whisper_id}"
            )
        ]

    ])

    # =====================================================
    # INLINE RESULT
    # =====================================================

    result = InlineQueryResultArticle(

        id=whisper_id,

        title=f"💌 Send Whisper To {target_show}",

        description="Private hidden message",

        input_message_content=InputTextMessageContent(

            "╔═════ 💌 ═════╗\n"
            "🌌 NIKI WHISPER 🌌\n"
            "╚══════════════╝\n\n"

            f"👤 Whisper For: {target_show}\n"
            f"⏳ Expires: 10 Minutes\n"
            f"🔒 Privacy Protected\n\n"

            "✨ Click button to open whisper."
        ),

        reply_markup=keyboard
    )

    await query.answer(
        [result],
        cache_time=1
    )

# =========================================================
#                  OPEN WHISPER
# =========================================================

async def open_whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cleanup_whispers()

    query = update.callback_query

    user = query.from_user

    whisper_id = query.data.split("_")[1]

    data = whispers.get(whisper_id)

    # =====================================================
    # EXPIRED
    # =====================================================

    if not data:

        return await query.answer(
            "❌ Whisper expired.",
            show_alert=True
        )

    # =====================================================
    # ACCESS CHECK
    # =====================================================

    allowed = False

    if data["target_username"]:

        if user.username:

            if user.username.lower() == data["target_username"]:

                allowed = True

    if data["target_id"]:

        if user.id == data["target_id"]:

            allowed = True

    # =====================================================
    # DENIED
    # =====================================================

    if not allowed:

        return await query.answer(
            "❌ This whisper isn't for you.",
            show_alert=True
        )

    # =====================================================
    # ONE TIME OPEN
    # =====================================================

    if data["opened"]:

        return await query.answer(
            "❌ Whisper already opened.",
            show_alert=True
        )

    data["opened"] = True

    # =====================================================
    # SENDER
    # =====================================================

    if data["anonymous"]:

        sender = "🎭 Anonymous"

    else:

        sender = data["sender_name"]

    # =====================================================
    # SHOW MESSAGE
    # =====================================================

    await query.answer(

        text=(
            f"💌 {data['text']}\n\n"
            f"👤 From: {sender}"
        ),

        show_alert=True
    )

# =========================================================
#                   REPLY WHISPER
# =========================================================

async def reply_whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    wid = query.data.split("_")[1]

    data = whispers.get(wid)

    if not data:

        return await query.answer(
            "❌ Whisper expired.",
            show_alert=True
        )

    sender_id = data["sender_id"]

    await query.answer()

    await query.message.reply_text(

        f"💌 Reply Whisper To:\n"
        f"<code>{sender_id}</code>\n\n"

        f"Example:\n"
        f"@iim_nikibot {sender_id} hello",

        parse_mode="HTML"
    )


# =====================================================
#                👑 NIKI OWNER COMMAND 👑
# =====================================================

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    try:
        admins = await context.bot.get_chat_administrators(chat.id)

        owner_user = None

        for admin in admins:
            if admin.status == "creator":
                owner_user = admin.user
                break

        if not owner_user:
            await update.message.reply_text("❌ Owner not found.")
            return

        # clickable owner mention
        owner_mention = f"<a href='tg://user?id={owner_user.id}'>{owner_user.first_name}</a>"

        text = f"""
╔═══━━━─── • 👑 NIKI OWNER • ───━━━═══╗
        𝐆𝐑𝐎𝐔𝐏 𝐎𝐖𝐍𝐄𝐑
╚═══━━━─── • ⚡ SYSTEM • ───━━━═══╝

        𓃠 {owner_mention} 𓃬

🌹 𝐑𝐮𝐥𝐞𝐫 𝐎𝐟 𝐓𝐡𝐢𝐬 𝐆𝐫𝐨𝐮𝐩
⚡ 𝐀𝐥𝐥 𝐏𝐨𝐰𝐞𝐫 𝐁𝐞𝐥𝐨𝐧𝐠𝐬 𝐓𝐨 𝐇𝐢𝐦
✨ 𝐑𝐞𝐬𝐩𝐞𝐜𝐭 𝐓𝐡𝐞 𝐂𝐫𝐨𝐰𝐧

╔══════════════════════╗
     ⚠️ 𝐍𝐈𝐊𝐈 𝐍𝐎𝐓𝐈𝐂𝐄 ⚠️
╚══════════════════════╝

🔥 𝐁𝐞𝐡𝐚𝐯𝐞 𝐎𝐫 𝐆𝐞𝐭 𝐑𝐞𝐦𝐨𝐯𝐞𝐝
💎 𝐎𝐰𝐧𝐞𝐫 𝐈𝐬 𝐀𝐥𝐰𝐚𝐲𝐬 𝐑𝐢𝐠𝐡𝐭
"""

        await update.message.reply_text(
            text,
            parse_mode="HTML"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")


#=========================admin =========================
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


OWNER_ID = (OWNER_ID)

warn_db = {}
admin_power = {}

# =========================================================
# 🌌 NIKI STYLE UI
# =========================================================

def ui(text):
    return f"""
🌌 𝙉𝙄𝙆𝙄 𝘼𝘿𝙈𝙄𝙉 𝘽𝙊𝙏
━━━━━━━━━━━━━━
{text}
━━━━━━━━━━━━━━
"""

def user_mention(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

# =========================================================
# 👤 GET REPLY USER
# =========================================================

def get_reply_user(update):
    return update.message.reply_to_message.from_user if update.message.reply_to_message else None

# =====================================================
# ⚠️ WARN SYSTEM
# =========================================================

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = get_reply_user(update)
    if not user:
        return

    chat = update.effective_chat.id

    warn_db.setdefault(chat, {})
    warn_db[chat][user.id] = warn_db[chat].get(user.id, 0) + 1

    count = warn_db[chat][user.id]

    await update.message.reply_text(
        ui(f"⚠️ WARN ISSUED\n👤 {user_mention(user)}\n📊 COUNT: {count}/3"),
        parse_mode="HTML"
    )


async def warns(update, context):

    user = get_reply_user(update)
    if not user:
        return

    chat = update.effective_chat.id
    count = warn_db.get(chat, {}).get(user.id, 0)

    await update.message.reply_text(
        ui(f"📊 WARN STATUS\n👤 {user_mention(user)}\n⚠️ TOTAL: {count}"),
        parse_mode="HTML"
    )


async def unwarn(update, context):

    user = get_reply_user(update)
    if not user:
        return

    chat = update.effective_chat.id

    if chat in warn_db and user.id in warn_db[chat]:
        warn_db[chat][user.id] = max(0, warn_db[chat][user.id] - 1)

    await update.message.reply_text(
        ui(f"♻️ 1 WARN REMOVED\n👤 {user_mention(user)}"),
        parse_mode="HTML"
    )

# =========================================================
# 👢 KICK
# =========================================================

async def kicked(update, context):

    user = get_reply_user(update)
    if not user:
        return

    chat = update.effective_chat.id

    await context.bot.ban_chat_member(chat, user.id)
    await context.bot.unban_chat_member(chat, user.id)

    await update.message.reply_text(
        ui(f"👢 USER KICKED\n👤 {user_mention(user)}"),
        parse_mode="HTML"
    )
# =========================================================
# 👑 PROMOTE / DEMOTE
# =========================================================

async def promote(update, context):

    user = get_reply_user(update)
    if not user:
        return

    level = int(context.args[0]) if context.args else 1
    admin_power[user.id] = level

    await context.bot.promote_chat_member(
        update.effective_chat.id,
        user.id,
        can_manage_chat=True,
        can_delete_messages=True,
        can_invite_users=True,
        can_pin_messages=True,
        can_restrict_members=True
    )

    await update.message.reply_text(
        ui(f"👑 PROMOTED\n👤 {user_mention(user)}\n⚡ LEVEL: {level}"),
        parse_mode="HTML"
    )


async def demote(update, context):

    user = get_reply_user(update)
    if not user:
        return

    admin_power[user.id] = 0

    await context.bot.promote_chat_member(
        update.effective_chat.id,
        user.id,
        can_manage_chat=False,
        can_delete_messages=False,
        can_invite_users=False,
        can_pin_messages=False,
        can_restrict_members=False
    )

    await update.message.reply_text(
        ui(f"❌ DEMOTED\n👤 {user_mention(user)}"),
        parse_mode="HTML"
    )

# =========================================================
# ➕ ADD / ➖ REMOVE POWER
# =========================================================

async def add(update, context):

    user = get_reply_user(update)
    if not user:
        return

    power = int(context.args[0]) if context.args else 1
    admin_power[user.id] = power

    await update.message.reply_text(
        ui(f"➕ POWER ADDED\n👤 {user_mention(user)}\n⚡ LEVEL: {power}"),
        parse_mode="HTML"
    )


async def remove(update, context):

    user = get_reply_user(update)
    if not user:
        return

    admin_power[user.id] = 0

    await update.message.reply_text(
        ui(f"➖ POWER REMOVED\n👤 {user_mention(user)}"),
        parse_mode="HTML"
    )
# =========================================================
# ❌ DEMOTE ALL
# =========================================================

async def demote_all(update, context):

    admin_power.clear()

    await update.message.reply_text(
        ui("❌ ALL ADMIN POWERS REMOVED"),
        parse_mode="HTML"
    )

# =========================================================
# 🏷️ TITLE
# =========================================================

async def title(update, context):

    user = get_reply_user(update)
    if not user:
        return

    title_text = " ".join(context.args)

    await context.bot.set_chat_administrator_custom_title(
        chat_id=update.effective_chat.id,
        user_id=user.id,
        custom_title=title_text
    )

    await update.message.reply_text(
        ui(f"🏷️ TITLE SET\n👤 {user_mention(user)}\n💠 {title_text}"),
        parse_mode="HTML"
    )

# =========================================================
# ✅ ACCEPT / ❌ REJECT
# =========================================================

async def accept(update, context):

    count = context.args[0] if context.args else "1"

    await update.message.reply_text(
        ui(f"✅ ACCEPTED REQUESTS\n📥 COUNT: {count}"),
        parse_mode="HTML"
    )


async def reject(update, context):

    count = context.args[0] if context.args else "1"

    await update.message.reply_text(
        ui(f"❌ REJECTED REQUESTS\n📥 COUNT: {count}"),
        parse_mode="HTML"
    )

# =========================================================
# 📌 PIN / UNPIN
# =========================================================

async def pin(update, context):

    if not update.message.reply_to_message:
        return

    await context.bot.pin_chat_message(
        update.effective_chat.id,
        update.message.reply_to_message.message_id
    )

    await update.message.reply_text(ui("📌 MESSAGE PINNED"))


async def unpin(update, context):

    await context.bot.unpin_all_chat_messages(update.effective_chat.id)

    await update.message.reply_text(ui("📌 ALL UNPINNED"))

# =========================================================
# 🗑️ DELETE
# =========================================================

async def d(update, context):

    if update.message.reply_to_message:
        await update.message.reply_to_message.delete()

    await update.message.delete()

# =========================================================
# 📖 HELP
# =========================================================

async def help_cmd(update, context):

    await update.message.reply_text(ui("""
🛡️ Admin Commands (.prefix only):
.warns username/userid/reply - Get all warnings of a user
.warn username/userid/reply - Warn a user (3 = ban)
.unwarn username/userid/reply - Remove 1 warning
.kicked username/userid/reply - Kick from group
.promote username/userid/reply 0/1/2/3 - Promote replied user to admin
.demote username/userid/reply - Demote admin
.add username/userid/reply power - add admin power
.remove username/userid/reply power - remove admin power
.demote_all demote all baka promoted admins
.title username/userid/reply title's name - Set custom title
.accept counts - Accept pending join requests
.reject counts - Decline pending join requests
.pin [reply] - Pin a message
.unpin - Unpin the current message
.d - delete a message
.help - Show this help

Note: You can use '.' or '!' as prefix.
Note: . or / both supported
"""), parse_mode="HTML")


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
    app.add_handler(ChatJoinRequestHandler(join_request_welcome))

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        )
    )
     
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
    
    app.add_handler(CommandHandler("gun", gun))
    app.add_handler(CommandHandler("gjoin", gjoin))
    app.add_handler(CommandHandler("shoot", shoot))
    app.add_handler(CommandHandler("bomb", bomb))
    app.add_handler(CommandHandler("bjoin", bjoin))
    app.add_handler(CommandHandler("pass", pass_bomb))
    app.add_handler(CommandHandler("bombcancel", bombcancel))
    app.add_handler(CommandHandler("bombtop", bombtop))
    app.add_handler(CommandHandler("myrank", myrank))
    app.add_handler(CommandHandler("userrank", userrank))

    app.add_handler(CommandHandler("admin", admin_list))
    app.add_handler(CommandHandler("pay", pay))
    app.add_handler(CommandHandler("addpremium", addpremium))
    app.add_handler(CommandHandler("removepremium", removepremium))
    app.add_handler(CommandHandler("allc", allc))
    app.add_handler(CommandHandler("voice", voice))
    app.add_handler(CommandHandler("voicef", voicef))
    app.add_handler(CommandHandler("voicem", voicem))

    app.add_handler(CommandHandler("voice1", premium_voice))
    app.add_handler(CommandHandler("voice2", premium_voice))
    app.add_handler(CommandHandler("voice3", premium_voice))
    app.add_handler(CommandHandler("voice4", premium_voice))
    app.add_handler(CommandHandler("voice5", premium_voice))

    app.add_handler(CommandHandler("voice6", premium_voice))
    app.add_handler(CommandHandler("voice7", premium_voice))
    app.add_handler(CommandHandler("voice8", premium_voice))
    app.add_handler(CommandHandler("voice9", premium_voice))
    app.add_handler(CommandHandler("voice10", premium_voice))
    app.add_handler(CommandHandler("wordgame", wordgame))
    app.add_handler(CommandHandler("enter", enter))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("hack", hack))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("starthack", starthack))
    app.add_handler(CommandHandler("guess", guess))
    app.add_handler(CommandHandler("players", players))
    app.add_handler(CommandHandler("hackinfo", hackinfo))
    app.add_handler(CommandHandler("endhack", endhack))   
    app.add_handler(CommandHandler("owner", owner))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("warns", warns))
    app.add_handler(CommandHandler("unwarn", unwarn))

    app.add_handler(CommandHandler("kicked", kicked))

    app.add_handler(CommandHandler("promote", promote))
    app.add_handler(CommandHandler("demote", demote))

    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("demote_all", demote_all))

    app.add_handler(CommandHandler("title", title))

    app.add_handler(CommandHandler("accept", accept))
    app.add_handler(CommandHandler("reject", reject))

    app.add_handler(CommandHandler("pin", pin))
    app.add_handler(CommandHandler("unpin", unpin))

    app.add_handler(CommandHandler("d", d))

    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("userinfo", userinfo))
    
    # ================= WORD GAME CALLBACK =================

    app.add_handler(
        CallbackQueryHandler(
            see_word,
            pattern="^see_word$"
        )
    )

    # ================= MAIN ROUTER =================

    app.add_handler(
        CallbackQueryHandler(
            button_router,
            pattern="^router_"
        )
    )

    # ================= MARRY SYSTEM =================

    app.add_handler(
        CallbackQueryHandler(
            accept,
            pattern="^marry_acc_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            reject,
            pattern="^marry_rej_"
        )
    )

    # ================= DUEL SYSTEM =================

    app.add_handler(
        CallbackQueryHandler(
            accept_btn,
            pattern="^duel_acc_"
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            cancel_btn,
            pattern="^duel_rej_"
        )
    )

    # ================= MENU SYSTEM =================

    app.add_handler(
        CallbackQueryHandler(
            button_callback,
            pattern="^(start_|help_cmds|economy_menu|games_menu|music_menu|manage_menu|reward_menu|social_menu|home_menu)"
        )
    )

    # ================= NUMBER / BET SYSTEM =================

    app.add_handler(
        CallbackQueryHandler(
            button,
            pattern="^(num_|bet_)"
        )
    )

    # ================= MINE GAME =================

    app.add_handler(
        CallbackQueryHandler(
            mine_click,
            pattern="^(mine_|cashout)"
        )
    )

    

    # ================= DAILY VERIFY =================

    app.add_handler(
        CallbackQueryHandler(
            daily_verify,
            pattern="^daily_verify_"
        )
    )
    #===================WHISPER =========================
   
    app.add_handler(
        InlineQueryHandler(
            inline_whisper
        )
    )
    app.add_handler(

        CallbackQueryHandler(
            open_whisper,
            pattern="^openwhisper_"
        )
    )

    app.add_handler(

        CallbackQueryHandler(
            reply_whisper,
            pattern="^replywhisper_"
        )
    )
    # ================= USERINFO SYSTEM =================

    app.add_handler(
        CallbackQueryHandler(
            userinfo_buttons,
            pattern="^userinfo"
        )
    )

    # ================= 🔥 MESSAGE SYSTEM (ORDERED) =================

    # 🛑 BLOCK SYSTEM (HIGHEST PRIORITY)
    app.add_handler(
        MessageHandler(filters.ALL, block_system),
        group=10
    )

    # 💾 SAVE USERS
    app.add_handler(
        MessageHandler(filters.ALL, save_users),
        group=9
    )

    # 🎮 WORD GAME CHECK (IMPORTANT)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_word),
        group=8
    )

    # 🔥 FILTER SYSTEM
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, filter_checker),
        group=5
    )

    # 🎮 GAME HANDLER (OTHER GAMES)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle),
        group=4
    )
    
    
    # 💖 LOVE FLOW
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, love_flow),
        group=3
    )

    # 🤖 MAIN AI (LAST TEXT PROCESSOR)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, niki_ai),
        group=20
    )
    
   

    print("🔥 Niki Bot started...")

    # ================= RUN BOT =================
    app.run_polling()

if __name__ == "__main__":
    main()
