import telebot
import random
from datetime import datetime

TOKEN = "8785022594:AAGrjrL0C2sWpqBlev6ZGPsYf0zsR0ZeWko"
bot = telebot.TeleBot(TOKEN)

captcha_db = {}
users_db = {}
captcha_attempts = {}

# ===== MENU =====
def main_menu():
    markup = telebot.types.InlineKeyboardMarkup()

    markup.row(
        telebot.types.InlineKeyboardButton("🛑 Account", callback_data="account"),
        telebot.types.InlineKeyboardButton("🛒 Buy Panel", callback_data="buy_panel")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("🌎 Global Buy Panel", callback_data="global_buy")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("❓ Help", callback_data="help"),
        telebot.types.InlineKeyboardButton("🗝️ Key History", callback_data="key_history")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("📽️ Tutorial", callback_data="tutorial")
    )

    markup.row(
        telebot.types.InlineKeyboardButton("💰 Deposit", callback_data="deposit")
    )

    return markup

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):

    captcha = random.randint(100000, 999999)
    captcha_db[message.chat.id] = captcha

    bot.send_message(
        message.chat.id,
        f"🤖 Captcha Verification\n\n👉 {captcha}"
    )

# ===== CAPTCHA =====
@bot.message_handler(func=lambda msg: msg.chat.id in captcha_db)
def captcha_check(message):

    user_id = message.chat.id
    user_text = message.text.strip()  # removes spaces

    if user_text.isdigit() and int(user_text) == captcha_db[user_id]:

        del captcha_db[user_id]
        captcha_attempts.pop(user_id, None)

        users_db.setdefault(user_id, {"balance":0,"orders":0})

        bot.send_message(
            user_id,
            "✅ Captcha Verified!\n\n👋 Welcome!\nSelect option below:",
            reply_markup=main_menu()
        )

    else:

        captcha_attempts[user_id] = captcha_attempts.get(user_id, 0) + 1

        if captcha_attempts[user_id] >= 3:

            new_captcha = random.randint(100000, 999999)
            captcha_db[user_id] = new_captcha
            captcha_attempts[user_id] = 0

            bot.send_message(
                user_id,
                f"❌ 3 Wrong Attempts!\n\n🔄 New Captcha:\n👉 {new_captcha}"
            )

        else:

            bot.send_message(
                user_id,
                f"❌ Wrong Captcha!\nAttempts Left: {3 - captcha_attempts[user_id]}"
            )
# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):

    bot.answer_callback_query(call.id, cache_time=0)

    if call.data == "account":

        user_id = call.message.chat.id
        user = users_db.get(user_id, {"balance":0,"orders":0})

        now = datetime.now()

        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%I:%M %p")

        bot.edit_message_text(
            f"👤 {call.from_user.first_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 User ID: {user_id}\n"
            f"💰 Balance: {user['balance']:.2f} INR\n"
            f"📦 Orders: {user['orders']}\n"
            f"📅 Date: {date}\n"
            f"⏰ Time: {time}\n"
            f"━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )

    elif call.data == "buy_panel":

        markup = telebot.types.InlineKeyboardMarkup()

        products = [
            ("🪪 Alpha Regedit", "alpha"),
            ("💻 Br Mode Pc", "br_pc"),
            ("📱 Dript Apk Mode", "dript_apk"),
            ("🖥️ Dript Pc Exe", "dript_pc"),
            ("🔥 Dript Root", "dript_root"),
            ("🧾 Esign Cert", "esign"),
            ("🌐 GBOX CERT", "gbox"),
            ("❄️ Fluorite iOS", "fluorite"),
            ("⚡ Haxx Pro", "haxx"),
            ("🧬 Hg Cheat", "hg"),
            ("⭐ LK Team Root", "lk"),
            ("💥 Pato Team", "pato"),
            ("🌟 Prime Apk", "prime"),
            ("🔒 Br Mode Root", "br_root"),
            ("🧪 Stricks BR Mode", "stricks"),
            ("🎵 Spotify Root", "spotify")
        ]

        for i in range(0, len(products), 2):
            row = []

            row.append(
                telebot.types.InlineKeyboardButton(products[i][0], callback_data=products[i][1])
            )

            if i+1 < len(products):
                row.append(
                    telebot.types.InlineKeyboardButton(products[i+1][0], callback_data=products[i+1][1])
                )

            markup.row(*row)

        markup.row(
            telebot.types.InlineKeyboardButton(
            "📥 All Files Download",
            url="https://t.me/+fOIPDX5ae1A1NTRl"
        )
        )
        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Menu", callback_data="back")
        )

        bot.edit_message_text(
            "🛒 Select Your Product",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "alpha":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 250 INR", callback_data="alpha_1"),
            telebot.types.InlineKeyboardButton("7 Day - 850 INR", callback_data="alpha_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 1700 INR", callback_data="alpha_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🪪 Alpha Regedit iOS\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    
    elif call.data == "br_pc":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 125 INR", callback_data="brpc_1"),
            telebot.types.InlineKeyboardButton("10 Day - 320 INR", callback_data="brpc_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 650 INR", callback_data="brpc_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Menu", callback_data="buy_panel")
        )


        bot.edit_message_text(
            "💻 Br Mods PC\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package from the list below:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "dript_apk":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="driptapk_1"),
            telebot.types.InlineKeyboardButton("7 Day - 300 INR", callback_data="driptapk_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 500 INR", callback_data="driptapk_15"),
            telebot.types.InlineKeyboardButton("30 Day - 800 INR", callback_data="driptapk_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "📱 Dript Apk Mode\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "dript_pc":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 100 INR", callback_data="driptpc_1"),
            telebot.types.InlineKeyboardButton("7 Day - 320 INR", callback_data="driptpc_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 550 INR", callback_data="driptpc_15"),
            telebot.types.InlineKeyboardButton("30 Day - 750 INR", callback_data="driptpc_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🖥️ Dript PC EXE\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "dript_root":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 80 INR", callback_data="driptroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 325 INR", callback_data="driptroot_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 300 INR", callback_data="driptroot_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🔥 Dript Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "esign":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Month - 450 INR", callback_data="esign_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🧾 Esign Cert\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "gbox":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Month - 900 INR", callback_data="gbox_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🌐 GBOX CERT\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "fluorite":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 180 INR", callback_data="fluorite_1"),
            telebot.types.InlineKeyboardButton("7 Day - 1050 INR", callback_data="fluorite_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 2000 INR", callback_data="fluorite_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "❄️ Fluorite iOS\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "haxx":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 450 INR", callback_data="haxx_10"),
            telebot.types.InlineKeyboardButton("20 Day - 850 INR", callback_data="haxx_20")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 1200 INR", callback_data="haxx_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🔥 Haxx Pro\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "hg":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 120 INR", callback_data="hg_1"),
            telebot.types.InlineKeyboardButton("10 Day - 280 INR", callback_data="hg_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 650 INR", callback_data="hg_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🧬 Hg Cheat\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "lk":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 90 INR", callback_data="lk_1"),
            telebot.types.InlineKeyboardButton("5 Day - 175 INR", callback_data="lk_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 260 INR", callback_data="lk_10"),
            telebot.types.InlineKeyboardButton("30 Day - 700 INR", callback_data="lk_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "⭐ LK Team Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "pato":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("3 Day - 200 INR", callback_data="pato_3"),
            telebot.types.InlineKeyboardButton("7 Day - 750 INR", callback_data="pato_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 600 INR", callback_data="pato_15"),
            telebot.types.InlineKeyboardButton("30 Day - 1000 INR", callback_data="pato_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "💥 Pato Team Apk + Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "prime":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("5 Day - 160 INR", callback_data="prime_5"),
            telebot.types.InlineKeyboardButton("10 Day - 300 INR", callback_data="prime_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🌟 Prime Apk\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "br_root":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="brroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="brroot_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 300 INR", callback_data="brroot_15"),
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="brroot_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🔒 Br Mode Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "stricks":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 50 INR", callback_data="stricks_1"),
            telebot.types.InlineKeyboardButton("5 Day - 100 INR", callback_data="stricks_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 160 INR", callback_data="stricks_10"),
            telebot.types.InlineKeyboardButton("15 Day - 240 INR", callback_data="stricks_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="stricks_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🧪 Stricks BR Mode\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )
    elif call.data == "spotify":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="spotify_7"),
            telebot.types.InlineKeyboardButton("15 Day - 300 INR", callback_data="spotify_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="spotify_30"),
            telebot.types.InlineKeyboardButton("60 Day - 750 INR", callback_data="spotify_60")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="buy_panel")
        )

        bot.edit_message_text(
            "🎵 Spotify Root\n━━━━━━━━━━━━━━━━━━━━\n"
            "Choose your package:\n"
            "┝ Status: 🟢 Available\n"
            "┝ Currency: INR\n"
            "━━━━━━━━━━━━━━━━━━━━",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # ===== GLOBAL BUY PANEL =====

    elif call.data == "global_buy":

        markup = telebot.types.InlineKeyboardMarkup()

        buttons = [
            ("🪪 Alpha Regedit iOS", "g_alpha"),
            ("💻 Br Mode Pc", "g_br_pc"),
            ("🔒 Br Mode Root", "g_br_root"),
            ("📱 Dript Apk Mode", "g_dript_apk"),
            ("🖥️ Dript Client Pc", "g_dript_pc"),
            ("🔥 Dript Client Root", "g_dript_root"),
            ("🧾 Esign Cert iOS", "g_esign"),
            ("🌐 GBOX CERT IOS", "g_gbox"),
            ("❄️ Flourties iOS", "g_fluorite"),
            ("⚡ Haxx-cker Pro", "g_haxx"),
            ("🧬 Hg Cheat Apk", "g_hg"),
            ("⭐ Lk Team Root + Pc", "g_lk"),
            ("💥 Pato Team Apk", "g_pato"),
            ("🌟 Prime Apk Mode", "g_prime"),
            ("🧪 Strike BR Mode", "g_strike"),
            ("🎵 Spotify Root", "g_spotify")
        ]

        for i in range(0, len(buttons), 2):
            row = []

            row.append(
                telebot.types.InlineKeyboardButton(
                buttons[i][0], callback_data=buttons[i][1]
            )
        )

            if i + 1 < len(buttons):
                row.append(
                    telebot.types.InlineKeyboardButton(
                    buttons[i+1][0], callback_data=buttons[i+1][1]
                )
        )

            markup.row(*row)   # ✅ LOOP के अंदर

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Menu", callback_data="back")
        )

        bot.edit_message_text(
            "🌎 Global Buy Panel\nSelect Product:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    # ===== GLOBAL PRODUCTS =====

    elif call.data == "g_alpha":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 250 INR", callback_data="g_alpha_1"),
            telebot.types.InlineKeyboardButton("7 Day - 10 INR", callback_data="g_alpha_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_alpha_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Alpha Regedit iOS\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_br_pc":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 140 INR", callback_data="g_brpc_1"),
            telebot.types.InlineKeyboardButton("10 Day - 330 INR", callback_data="g_brpc_10")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_brpc_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Br Mode Pc\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_br_root":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="g_brroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="g_brroot_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 320 INR", callback_data="g_brroot_15"),
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="g_brroot_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Br Mode Root\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_dript_apk":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="g_driptapk_1"),
            telebot.types.InlineKeyboardButton("7 Day - 300 INR", callback_data="g_driptapk_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 500 INR", callback_data="g_driptapk_15"),
            telebot.types.InlineKeyboardButton("30 Day - 800 INR", callback_data="g_driptapk_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Dript Apk Mode\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_dript_pc":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 110 INR", callback_data="g_driptpc_1"),
            telebot.types.InlineKeyboardButton("7 Day - 320 INR", callback_data="g_driptpc_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 600 INR", callback_data="g_driptpc_15"),
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_driptpc_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Dript Client Pc\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_dript_root":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 80 INR", callback_data="g_driptroot_1"),
            telebot.types.InlineKeyboardButton("7 Day - 340 INR", callback_data="g_driptroot_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 700 INR", callback_data="g_driptroot_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Dript Client Root\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_esign":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Buy Certificate - 450 INR", callback_data="g_esign_30"))
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Esign Cert iOS\nChoose option:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_gbox":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton("Buy Certificate - 10 INR", callback_data="g_gbox_30"))
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 GBOX CERT IOS\nChoose option:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_fluorite":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 10 INR", callback_data="g_fluorite_1"),
            telebot.types.InlineKeyboardButton("7 Day - 10 INR", callback_data="g_fluorite_7")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_fluorite_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Flourties iOS\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_haxx":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 450 INR", callback_data="g_haxx_10"),
            telebot.types.InlineKeyboardButton("20 Day - 10 INR", callback_data="g_haxx_20")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_haxx_30")
        )
        markup.row(telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy"))
        bot.edit_message_text("🌎 Haxx-cker Pro\nChoose package:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "g_hg":
        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 120 INR", callback_data="g_hg_1"),
            telebot.types.InlineKeyboardButton("10 Day - 250 INR", callback_data="g_hg_10")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_hg_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🌎 Hg Cheat Apk\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_lk":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 90 INR", callback_data="g_lk_1"),
            telebot.types.InlineKeyboardButton("5 Day - 175 INR", callback_data="g_lk_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 10 INR", callback_data="g_lk_10"),
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_lk_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "⭐ LK Team Root + PC\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_pato":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("3 Day - 200 INR", callback_data="g_pato_3"),
            telebot.types.InlineKeyboardButton("7 Day - 350 INR", callback_data="g_pato_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_pato_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "💥 Pato Team Apk\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_prime":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 75 INR", callback_data="g_prime_1"),
            telebot.types.InlineKeyboardButton("7 Day - 330 INR", callback_data="g_prime_7")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("15 Day - 500 INR", callback_data="g_prime_15"),
            telebot.types.InlineKeyboardButton("30 Day - 800 INR", callback_data="g_prime_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🌟 Prime Apk Mode\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_strike":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("1 Day - 55 INR", callback_data="g_strike_1"),
            telebot.types.InlineKeyboardButton("5 Day - 100 INR", callback_data="g_strike_5")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("10 Day - 10 INR", callback_data="g_strike_10"),
            telebot.types.InlineKeyboardButton("15 Day - 10 INR", callback_data="g_strike_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 10 INR", callback_data="g_strike_30")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🧪 Strike BR Mode\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "g_spotify":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton("7 Day - 180 INR", callback_data="g_spotify_7"),
            telebot.types.InlineKeyboardButton("15 Day - 10 INR", callback_data="g_spotify_15")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("30 Day - 450 INR", callback_data="g_spotify_30"),
            telebot.types.InlineKeyboardButton("60 Day - 10 INR", callback_data="g_spotify_60")
        )

        markup.row(
            telebot.types.InlineKeyboardButton("🔙 Back To Panel", callback_data="global_buy")
        )

        bot.edit_message_text(
            "🎵 Spotify Root\nChoose package:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "help":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton(
            "💬 Contact Support",
            url="https://t.me/avesh_thakur"
        )
    )

        markup.row(
            telebot.types.InlineKeyboardButton(
            "🔙 Back To Menu",
            callback_data="back"
        )
    )

        bot.edit_message_text(
            "❓ Help Section\n\n"
            "👉 Click button below to contact support.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "deposit":

        markup = telebot.types.InlineKeyboardMarkup()

        markup.row(
            telebot.types.InlineKeyboardButton(
            "💬 Contact Support for Deposit",
            url="https://t.me/avesh_thakur"
        )
    )

        markup.row(
            telebot.types.InlineKeyboardButton(
            "🔙 Back To Menu",
            callback_data="back"
        )
    )

        bot.edit_message_text(
            "💰 Deposit Section\n\n"
            "👉 Please contact support for deposit details.\n"
            "👉 Our team will guide you.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "back":

        bot.edit_message_text(
            "👋 Welcome!\nSelect option below:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )
print("Bot started...")
bot.infinity_polling()