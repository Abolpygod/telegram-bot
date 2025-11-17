import telebot
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask
import random
from threading import Thread

# -------------------------
# 🔵 توکن و چت‌آیدی
# -------------------------
TOKEN = "8500598706:AAEkXIdoZh-7kFTdVNkv3bkn2iX0Ig2SrKE"
CHAT_ID = 8110203831  # عدد چت آیدی خودتو بزار اینجا
bot = telebot.TeleBot(TOKEN)

# -------------------------
# 🔵 سیستم روشن ماندن (Replit/Render)
# -------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------------------------
# 🔥 ذخیره ساعت بیدار شدن
# -------------------------
wake_time = None
FIRST_TASK_TIME = "08:40"

def send(msg):
    try:
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    except:
        pass

# -------------------------
# 🔥 50 جمله انگیزشی قوی
# -------------------------
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
    "🏋️‍♂️ درد امروز قدرت فردا!",
    "🦁 با ترسات رودررو شو!",
    "🥇 نسخه قوی‌ترت تو راهه!",
    "🔥 ادامه بده… موفقیت نزدیکه!",
    "🚀 با قدم شروع میشه، نه رؤیا!",
    "🧨 دیر نیست… وقتی دیر میشه که جا بزنی!",
    "💯 تمرکز کن ابوالفضل!",
    "🔥 تو معمولی نیستی!",
    "💪 هیچ‌وقت تسلیم نشو!",
    "🚀 کارای سخت تو رو می‌سازن!",
    "⚔️ کاری رو بکن که بقیه نمی‌کنن!",
    "🔥 جنگجو وقتی خسته‌ست ادامه میده!",
    "💥 شروع سخت‌ترین بخشه!",
    "⚡ خودتو دست‌کم نگیر!",
    "🏆 فردای قوی نتیجه امروزته!",
    "🧠 نظم = قدرت!",
    "🔥 منتظر انگیزه نمون، شروع کن!",
    "🚀 انجام بده، نه بهونه!",
    "💪 محکم باشد قهرمان!",
    "⚔️ هر روز یک درصد بهتر شو!",
    "🔥 رقیبت خودتی!",
    "🏋️ نایار! ادامه بده!",
    "🦾 سختی بیشتر = نتیجه بیشتر!",
    "🦂 فرار نکن… قوی‌تر شو!",
    "🎯 هدف کوچیک + تکرار!",
    "🔥 تو تنها ناجی خودتی!",
    "💯 کم بهتر از هیچی!",
    "🚀 امروز یه کار سخت انجام بده!",
    "🥊 تو جنگجویی!",
    "🔥 قوی هستی!",
    "💥 آروم ولی ثابت!",
    "🏆 آینده رو می‌سازی!",
    "🦁 زود جا نزن!",
    "🔥 تازه اول راهی!",
    "🚀 موفقیت با ثبات میاد!",
    "💪 افتخار کن حتی به قدم کوچیک!",
    "⚡ هیچ چیز جای تلاش رو نمی‌گیره!",
    "🥊 جنگجو همیشه پا میشه!",
    "🔥 امروز رو نابود کن!"
]

# -------------------------
# 🎂 تبریک تولد ۱ آذر
# -------------------------
def check_birthday():
    now = datetime.datetime.now()
    if now.month == 9 and now.day == 22:  # 1 آذر = 22 نوامبر؟
        if now.strftime("%H:%M") == "08:30":
            send("🎉🎂 *ابوالفضل قهرمان! تولدت مبارک!* 🎂🎉\n"
                 "این سال سال خیزش بزرگته! 🔥")

# -------------------------
# 📅 برنامه روزانه
# -------------------------

# روزهای زوج
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

# فرد
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

# جمعه
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

# -------------------------
# ⚡ دستور انگیزشی
# -------------------------
@bot.message_handler(commands=['mot'])
def random_motivation(message):
    bot.reply_to(message, random.choice(motivations))

# -------------------------
# 🕒 ثبت ساعت بیدار شدن
# -------------------------
@bot.message_handler(commands=['wake'])
def record_wake(message):
    global wake_time

    now = datetime.datetime.now()
    wake_time = now

    send(f"🔥 ابوالفضل! ساعت {now.strftime('%H:%M')} بیدار شدی.")

    first_task = datetime.datetime.strptime(FIRST_TASK_TIME, "%H:%M")
    first_task = now.replace(hour=first_task.hour, minute=first_task.minute)

    delta = first_task - now
    minutes_left = int(delta.total_seconds() / 60)

    if minutes_left > 20:
        send(f"⏳ {minutes_left} دقیقه وقت داری — آروم شروع کن.")
    elif minutes_left > 5:
        send(f"⚡ {minutes_left} دقیقه وقت داری. آماده شو.")
    else:
        send(f"🚨 عجله کن! فقط {minutes_left} دقیقه مونده!")

# -------------------------
# 🎮 گیم‌ها — فقط زمان استراحت
# -------------------------
def is_rest_time():
    now = datetime.datetime.now().strftime("%H:%M")
    rest_ranges = [
        ("09:15", "09:59"),
        ("11:10", "11:59"),
        ("12:00", "17:29"),
        ("20:01", "21:39"),
        ("22:31", "23:09")
    ]
    return any(start <= now <= end for start, end in rest_ranges)

word_game_words = ["boxer", "strong", "energy", "focus", "study", "victory"]

def shuffle_word(word):
    letters = list(word)
    random.shuffle(letters)
    return "".join(letters)

@bot.message_handler(commands=['game'])
def game_menu(message):
    if not is_rest_time():
        bot.reply_to(message, "⛔ الان وقت کاره قهرمان! وقت استراحت بازی می‌دم.")
        return

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton("🔢 حدس عدد", callback_data="game_number"),
        telebot.types.InlineKeyboardButton("✊✋✌️ سنگ‌کاغذ-قیچی", callback_data="game_rps")
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton("🎰 لاتاری", callback_data="game_lottery"),
        telebot.types.InlineKeyboardButton("🧠 کلمه بهم‌ریخته", callback_data="game_word")
    )
    keyboard.add(
        telebot.types.InlineKeyboardButton("🎯 شانس امروز", callback_data="game_luck")
    )

    bot.reply_to(message, "🎮 *یه بازی انتخاب کن ابوالفضل:*", reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def game_handler(call):

    if not is_rest_time():
        bot.answer_callback_query(call.id, "⛔ الان وقت گیم نیست!")
        return

    if call.data == "game_number":
        num = random.randint(1, 20)
        bot.send_message(call.message.chat.id, f"🔢 *عدد مخفی:* {num}")

    elif call.data == "game_rps":
        choice = random.choice(["✊ سنگ", "✋ کاغذ", "✌️ قیچی"])
        bot.send_message(call.message.chat.id, f"✊✋✌️ انتخاب من: {choice}")

    elif call.data == "game_lottery":
        nums = random.sample(range(1, 40), 5)
        bot.send_message(call.message.chat.id, f"🎰 اعداد شانس: {nums}")

    elif call.data == "game_word":
        w = random.choice(word_game_words)
        mixed = shuffle_word(w)
        bot.send_message(call.message.chat.id, f"🧠 کلمه: `{mixed}`\nدرستش کن!")

    elif call.data == "game_luck":
        luck = [
            "🍀 امروز شانس باهاته!",
            "🔥 انرژی فوق‌العاده داری!",
            "😎 روز قوی‌ای در راهه!",
            "🤣 یک چیز عجیب امروز اتفاق میفته!",
            "⚡ آماده سورپرایز باش!"
        ]
        bot.send_message(call.message.chat.id, random.choice(luck))

# -------------------------
# ℹ️ دستور راهنما
# -------------------------
@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.reply_to(message,
                 "📘 *راهنمای ربات ابوالفضل*\n\n"
                 "/wake — ثبت بیدار شدن\n"
                 "/mot — جمله انگیزشی\n"
                 "/game — بازی‌ها (فقط زمان استراحت)\n"
                 "/help — این راهنما\n",
                 parse_mode="Markdown")

# -------------------------
# 🔁 حلقه زمان
# -------------------------
def time_checker():
    scheduler = BackgroundScheduler(timezone="Asia/Tehran")

    # Adding scheduled tasks for sending messages at specific times
    scheduler.add_job(lambda: send(random.choice(motivations)), CronTrigger(hour=8, minute=20))  # Random motivation at 8:20
    scheduler.add_job(lambda: send("⏰ ابوالفضل بیدار شو قهرمان!"), CronTrigger(hour=8, minute=30))  # Wakeup call at 8:30

    # Adding other scheduled tasks for daily messages
    scheduler.add_job(lambda: send(schedule_zoj.get(str(datetime.datetime.now().strftime('%H:%M')))), CronTrigger(hour=8, minute=30))

    scheduler.start()
    
    while True:
        time.sleep(60)

# -------------------------
# 🚀 اجرای ربات
# -------------------------
keep_alive()
Thread(target=time_checker).start()
bot.polling()
