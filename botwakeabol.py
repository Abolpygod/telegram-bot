# main.py
# ربات تلگرام ابوالفضل — سازگار با Render
# نکته: قبل از اجرا TOKEN و CHAT_ID را قرار بده یا در متغیرهای محیطی تعریف کن.

import os
import telebot
import datetime
import time
import random
from threading import Thread
from flask import Flask
from zoneinfo import ZoneInfo  # موجود در پایتون 3.9+
from telebot import types

# ---------- تنظیمات (توکن و چت‌آیدی) ----------
TOKEN = os.getenv("TOKEN", "8500598706:AAEkXIdoZh-7kFTdVNkv3bkn2iX0Ig2SrKE")
# اگر می‌خوای عدد را داخل فایل بذاری بجای env، مقدار اینجا هم قرار بده.
CHAT_ID = int(os.getenv("CHAT_ID", "8110203831"))  # عددی؛ پیش‌فرض 0 یعنی ارسال خودکار استارت غیرفعال

bot = telebot.TeleBot(TOKEN)

# ---------- Keep-alive برای Render (Flask) ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    # Render پورت را خودش کنترل می‌کند، اما 8080 امنه
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ---------- زمانبندی و timezone ایران ----------
TEHRAN = ZoneInfo("Asia/Tehran")

def now_tehran():
    return datetime.datetime.now(TEHRAN)

# ---------- تابع ارسال امن پیام ----------
def send(msg):
    try:
        if CHAT_ID and CHAT_ID != 0:
            bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        else:
            print("[send] CHAT_ID not set — skipping send")
    except Exception as e:
        print("[send] error:", e)

# ---------- پیام‌های انگیزشی (شخصی‌شده) ----------
motivations = [
    "🔥 ابوالفضل! تو ساخته شدی برای سختی‌ها، نه فرار ازشون!",
    "💪 هرروز داری قوی‌تر می‌شی قهرمان!",
    "⚡ هیچ‌کس جلو کسی که ادامه می‌ده نمی‌تونه وایسته!",
    "🏆 قهرمان‌ها ساخته می‌شن، به دنیا نمیان!",
    "🥊 تو خیلی قوی‌تری از چیزی که فکر می‌کنی!",
    "🚀 امروز روز توعه! برو نابود کن!",
    "🔥 شکست فقط درس جدیده!",
    "🧠 ذهن قوی همه‌چیو عوض می‌کنه!",
    "⚡ انرژی امروزت آینده‌تو می‌سازه!",
    "🏋️‍♂️ درد امروز قدرت فردا!"
    # در صورت نیاز بقیه جملات رو اضافه کن
]

# ---------- تاریخ تولد (اختیاری) ----------
# اگر می‌خوای تبریک تولد خودکار داشته باشی، متغیرهای ENV رو ست کن:
BIRTHDAY_MONTH = int(os.getenv("BIRTHDAY_MONTH", "0"))  # مثال 9 برای آذر/نوامبر یا 12 و ...
BIRTHDAY_DAY = int(os.getenv("BIRTHDAY_DAY", "0"))      # روز

def check_birthday():
    if BIRTHDAY_MONTH and BIRTHDAY_DAY:
        now = now_tehran()
        if now.month == BIRTHDAY_MONTH and now.day == BIRTHDAY_DAY:
            if now.strftime("%H:%M") == "08:30":
                send("🎉🎂 *ابوالفضل قهرمان! تولدت مبارک!* 🎂🎉\nاین سال سال خیزش بزرگته! 🔥")

# ---------- جدول برنامه (زوج / فرد / جمعه) ----------
FIRST_TASK_TIME = "08:40"  # تغییر نده یا اگر خواستی میتونی ENV بذاری

schedule_zoj = {
    "08:30": "⏰ ابوالفضل بیدار شو قهرمان!",
    "08:40": "🏃‍♂️ وقت دویدنه!",
    "09:00": "🍞 نون بگیر.",
    "09:10": "🍳 صبحانه.",
    "10:00": "📚 درس.",
    "11:00": "🔁 مرور.",
    "12:00": "🏫 مدرسه.",
    "17:30": "🚿 دوش.",
    "18:00": "🍽️ شام.",
    "19:00": "👜 آماده باشگاه.",
    "19:30": "➡️ حرکت به باشگاه.",
    "20:00": "🥊 باشگاه بوکس.",
    "21:45": "🏠 رسیدی خونه.",
    "22:30": "😌 ریلکس.",
    "23:10": "📝 جمع‌بندی.",
    "23:30": "🌙 خواب."
}

schedule_fard = {
    "08:30": "⏰ بیدار شو!",
    "08:40": "🏃‍♂️ دویدن.",
    "09:00": "🍞 نان.",
    "10:00": "📚 درس.",
    "11:00": "🔁 مرور.",
    "12:00": "🏫 مدرسه.",
    "17:30": "🚿 دوش.",
    "18:00": "🍽️ شام.",
    "18:50": "📝 کلاس زبان.",
    "19:00": "🇬🇧 کلاس شروع.",
    "20:30": "📘 مرور زبان.",
    "21:40": "🎒 آماده فردا.",
    "23:00": "🌙 خواب."
}

schedule_jome = {
    "08:30": "⏰ بیدار شو!",
    "09:10": "🍳 صبحانه.",
    "10:00": "📚 درس 1.",
    "11:20": "✏️ تمرین.",
    "12:00": "🍛 ناهار.",
    "14:00": "📖 درس 2.",
    "15:00": "🤸‍♂️ ورزش.",
    "17:00": "📚 درس 3.",
    "20:00": "🧾 جمع‌بندی.",
    "21:00": "🎮 تفریح.",
    "23:00": "🌙 خواب."
}

# ---------- گیم و منطق بازی (فقط در زمان استراحت فعال) ----------
word_game_words = ["boxer", "strong", "energy", "focus", "study", "victory"]

def shuffle_word(word):
    letters = list(word)
    random.shuffle(letters)
    return "".join(letters)

def is_rest_time():
    now = now_tehran().strftime("%H:%M")
    rest_ranges = [
        ("09:15", "09:59"),
        ("11:10", "11:59"),
        ("12:00", "17:29"),
        ("20:01", "21:39"),
        ("22:31", "23:09")
    ]
    return any(start <= now <= end for start, end in rest_ranges)

# ---------- هندلرها (فرامین) ----------
@bot.message_handler(commands=["start"])
def start_cmd(message):
    # دکمه‌های سریع (کاربر با زدن دکمه متن رو ارسال می‌کنه)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("/wake"), types.KeyboardButton("/mot"))
    kb.add(types.KeyboardButton("/game"), types.KeyboardButton("/help"))
    bot.reply_to(message, "سلام ابوالفضل! ربات روشنه — از دکمه‌ها استفاده کن.", reply_markup=kb)

@bot.message_handler(commands=["help"])
def help_msg(message):
    txt = ("📘 *راهنمای ربات ابوالفضل*\n\n"
           "/wake — ثبت بیدار شدن\n"
           "/mot — جمله انگیزشی\n"
           "/game — بازی‌ها (فقط در زمان استراحت)\n"
           "/help — این راهنما\n")
    bot.reply_to(message, txt, parse_mode="Markdown")

@bot.message_handler(commands=["mot"])
def mot_cmd(message):
    bot.reply_to(message, random.choice(motivations))

@bot.message_handler(commands=["wake"])
def wake_cmd(message):
    now = now_tehran()
    # ذخیره زمان بیدار شدن (برای کاربر فعلاً فقط اعلان)
    send(f"🔥 ابوالفضل! ساعت {now.strftime('%H:%M')} بیدار شدی.")
    # فاصله تا اولین کار
    first_task = datetime.datetime.strptime(FIRST_TASK_TIME, "%H:%M").time()
    ft_dt = now.replace(hour=first_task.hour, minute=first_task.minute, second=0, microsecond=0)
    delta = ft_dt - now
    minutes_left = int(delta.total_seconds() / 60)
    if minutes_left > 20:
        send(f"⏳ {minutes_left} دقیقه وقت داری — آروم شروع کن.")
    elif minutes_left > 5:
        send(f"⚡ {minutes_left} دقیقه وقت داری. آماده شو.")
    else:
        send(f"🚨 عجله کن! فقط {minutes_left} دقیقه مونده!")

@bot.message_handler(commands=["game"])
def game_cmd(message):
    if not is_rest_time():
        bot.reply_to(message, "⛔ الان وقت کاره قهرمان! وقت استراحت بازی می‌دم.")
        return
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔢 حدس عدد", callback_data="game_number"),
                 types.InlineKeyboardButton("✊✋✌️ سنگ‌کاغذ-قیچی", callback_data="game_rps"))
    keyboard.add(types.InlineKeyboardButton("🎰 لاتاری", callback_data="game_lottery"),
                 types.InlineKeyboardButton("🧠 کلمه بهم‌ریخته", callback_data="game_word"))
    keyboard.add(types.InlineKeyboardButton("🎯 شانس امروز", callback_data="game_luck"))
    bot.reply_to(message, "🎮 یه بازی انتخاب کن ابوالفضل:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def callback_game(call):
    if not is_rest_time():
        bot.answer_callback_query(call.id, "⛔ الان وقت گیم نیست!")
        return
    if call.data == "game_number":
        n = random.randint(1, 20)
        bot.send_message(call.message.chat.id, f"🔢 عدد مخفی: {n}")
    elif call.data == "game_rps":
        choice = random.choice(["✊ سنگ", "✋ کاغذ", "✌️ قیچی"])
        bot.send_message(call.message.chat.id, f"✊✋✌️ انتخاب من: {choice}")
    elif call.data == "game_lottery":
        nums = random.sample(range(1, 40), 5)
        bot.send_message(call.message.chat.id, f"🎰 اعداد شانس: {nums}")
    elif call.data == "game_word":
        w = random.choice(word_game_words)
        bot.send_message(call.message.chat.id, f"🧠 کلمه‌ی بهم‌ریخته: `{shuffle_word(w)}`\nسعی کن درستش کنی!")
    elif call.data == "game_luck":
        lucks = ["🍀 امروز شانس باهاته!", "🔥 انرژی بالاست!", "😎 روز قوی‌ای در راهه!"]
        bot.send_message(call.message.chat.id, random.choice(lucks))

# ---------- حلقه زمان برای ارسال خودکار ----------

def time_checker():
    # هر 30 ثانیه چک می‌کنیم (دقت دقیقه‌ای)
    while True:
        try:
            now = now_tehran()
            day = now.weekday()  # Monday=0 ... Sunday=6
            current = now.strftime("%H:%M")

            # تبریک تولد (اگر ست شده)
            check_birthday()

            # پیام انگیزشی روزانه
            if current == "08:20":
                send(random.choice(motivations))

            # ارسال برنامه بر اساس روز
            # کاربر از قبل گفته بود روزهای زوج: [5,0,2] و فرد: [6,1,3]؟ — اینجا همان تنظیمات قبلی استفاده شد
            if day in [5, 0, 2] and current in schedule_zoj:
                send(schedule_zoj[current])

            if day in [6, 1, 3] and current in schedule_fard:
                send(schedule_fard[current])

            if day == 4 and current in schedule_jome:
                send(schedule_jome[current])

        except Exception as e:
            print("[time_checker] error:", e)
        time.sleep(30)

# ---------- استارت آپ: حذف webhook (برای جلوگیری از conflict) ----------
def prepare_and_start():
    # حذف webhook (اگه قبلاً ست شده بود) — برای جلوگیری از خطای conflict
    try:
        bot.remove_webhook()
    except Exception as e:
        print("[prepare] remove_webhook:", e)

    # اگر CHAT_ID و TOKEN مقدار درست داشتند، یک پیام استارت بفرست تا مطمئن شی ربات آنلاین شده
    try:
        if TOKEN and TOKEN != "PASTE_YOUR_TOKEN_HERE" and CHAT_ID and CHAT_ID != 0:
            send(f"✅ ربات ابوالفضل روشن شد — زمان فعلی ایران: {now_tehran().strftime('%Y-%m-%d %H:%M')}")
        else:
            print("[prepare] TOKEN or CHAT_ID not set — skipping initial send")
    except Exception as e:
        print("[prepare] sending startup message failed:", e)

    # اجرای حلقه زمان در thread
    t = Thread(target=time_checker)
    t.daemon = True
    t.start()

    # شروع کردن polling
    print("[prepare] starting polling...")
    try:
        # non_stop=True ensures it retries on some errors; timeout sets long polling timeout
        bot.polling(non_stop=True, interval=0, timeout=60)
    except Exception as e:
        print("[prepare] polling terminated with error:", e)
        # در صورت خطا سعی کن مجدداً (می‌توانی لوجیک retry اضافه کنی)
        time.sleep(5)
        prepare_and_start()

if __name__ == "__main__":
    keep_alive()
    prepare_and_start()
