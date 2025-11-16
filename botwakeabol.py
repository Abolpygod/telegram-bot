import telebot
import datetime
import time
from threading import Thread
from flask import Flask, request
import random
import os

# -------------------------
# 🔵 توکن و چت‌آیدی
# -------------------------
TOKEN = "8500598706:AAEkXIdoZh-7kFTdVNkv3bkn2iX0Ig2SrKE"
CHAT_ID = 8110203831
bot = telebot.TeleBot(TOKEN)

# -------------------------
# 🌐 Flask برای رندر
# -------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive on Render ✔️"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.stream.read().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

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
    "🔥 تو ساخته شدی برای سختی‌ها، نه فرار ازشون!",
    "💪 از هر تمرین قوی‌تر برمی‌گردی!",
    "⚡ هیچ‌کس نمی‌تونه جلوی کسی رو بگیره که نخواسته وایسه!",
    "🏆 قهرمان‌ها یک‌دفعه ساخته نمی‌شن، هر روز ساخته می‌شن.",
    "🥊 تو از چیزی که فکر می‌کنی خیلی قوی‌تری!",
    "🚀 امروز بهترین فرصت برای بهتر شدنه!",
    "🔥 شکست فقط یه درس جدیده، نه پایان!",
    "🧠 ذهن قوی = زندگی قوی!",
    "⚡ انرژی امروزت تعیین‌کننده فرداته!",
    "🏋️‍♂️ فشار امروز = قدرت فردا!",
    "🦁 با ترسات روبرو شو، نه اینکه ازشون فرار کنی!",
    "🥇 بهترین نسخه‌ت هنوز نیومده!",
    "🔥 فقط ادامه بده… نتایج خودش میاد!",
    "🚀 با یه قدم شروع میشه، نه با یه رؤیا!",
    "🧨 هیچوقت دیر نیست… دیر وقتی‌ه که جا بزنی!",
    "💯 تمرکز = پیروزی!",
    "🔥 تو قرار نیست معمولی باشی!",
    "💪 کسی که تسلیم نشه همیشه برندست!",
    "🚀 کارهای سخت تو رو میسازن!",
    "⚔️ امروز اون کاری رو بکن که بقیه حوصله‌شو ندارن!",
    "🔥 جنگجو بودن یعنی وقتی خسته‌ای ادامه بدی!",
    "💥 هیچ‌چیزی سخت‌تر از شروع نیست!",
    "⚡ خودتو دست‌کم نگیر!",
    "🏆 روزی خودت از امروزت تشکر می‌کنی!",
    "🧠 نظم از همه چیز مهم‌تره!",
    "🔥 اگه منتظر انگیزه‌ای هیچ‌وقت شروع نمی‌کنی!",
    "🚀 کاری که باید انجام بدی رو انجام بده، نه کاری که دوست داری!",
    "💪 سخت باش. محکم باش. ادامه بده!",
    "⚔️ هر روز یک درصد بهتر شو. فقط یک درصد!",
    "🔥 رقیب اصلی تو خودت هستی!",
    "🏋️ کم نیار، همین الان وقتشه!",
    "🦾 هر چی سخت‌تر، نتیجه بزرگ‌تر!",
    "🦂 از سختیا فرار نکنی، خودت سخت‌تر میشی!",
    "🎯 هدف ریز + تکرار = نابودی شکست!",
    "🔥 تو تنها کسی هستی که می‌تونه زندگیتو عوض کنه!",
    "💯 حتی اگه کم پیشرفت کنی، بهتر از وایستادنه!",
    "🚀 امروز یه کار سخت انجام بده!",
    "🥊 تو رو ساختن برای جنگیدن، نه فرار!",
    "🔥 تو قوی‌ای قوی‌تر هم میشی!",
    "💥 مهم نیست چقدر آرام… مهم اینه وای نمیسی!",
    "🏆 آینده‌ای که میخوای ساخته نمیشه، *ساخته‌ش می‌کنی*!",
    "🦁 کسی که زود جا می‌زنه هیچ‌وقت برندست!",
    "🔥 تو هنوز اول راهی!",
    "🚀 موفقیت از تداوم میاد نه سرعت!",
    "💪 به خودت افتخار کن، حتی اگه قدم کوچیکه!",
    "⚡ هیچ‌چیزی جای سخت‌کوشی رو نمیگیره!",
    "🥊 جنگجو همیشه پا میشه!",
    "🔥 امروزت رو نابود کن قهرمان!"
]

# -------------------------
# 🎂 تبریک تولد
# -------------------------
def check_birthday():
    now = datetime.datetime.now()
    if now.month == 11 and now.day == 21:
        if now.strftime("%H:%M") == "08:30":
            send("🎉🎂 *تولدت مبارک قهرمان!* 🎂🎉\nاین سال سال جهش بزرگته!")

# -------------------------
# 📅 برنامه روزانه
# -------------------------
schedule_zoj = {
    "08:30": "⏰ بیدار شو قهرمان!\n||08:30||",
    "08:40": "🏃‍♂️ وقت دویدن!\n||08:40||",
    "09:00": "🍞 نون بگیر.\n||09:00||",
    "09:10": "🍳 صبحانه.\n||09:10||",
    "10:00": "📚 درس اصلی.\n||10:00||",
    "11:00": "🔁 مرور.\n||11:00||",
    "12:00": "🏫 مدرسه.\n||12:00||",
    "17:30": "🚿 دوش.\n||17:30||",
    "18:00": "🍽️ شام.\n||18:00||",
    "19:00": "👜 آماده باشگاه.\n||19:00||",
    "19:30": "➡️ حرکت.\n||19:30||",
    "20:00": "💪 باشگاه.\n||20:00||",
    "21:45": "🏠 خونه.\n||21:45||",
    "22:30": "😌 ریلکس.\n||22:30||",
    "23:10": "📝 جمع‌بندی.\n||23:10||",
    "23:30": "🌙 خواب.\n||23:30||"
}

schedule_fard = {
    "08:30": "⏰ بیدار شو!\n||08:30||",
    "08:40": "🏃‍♂️ دویدن.\n||08:40||",
    "09:00": "🍞 نان.\n||09:00||",
    "10:00": "📚 درس.\n||10:00||",
    "11:00": "🔁 مرور.\n||11:00||",
    "12:00": "🏫 مدرسه.\n||12:00||",
    "17:30": "🚿 دوش.\n||17:30||",
    "18:00": "🍽️ شام.\n||18:00||",
    "18:50": "📝 کلاس زبان.\n||18:50||",
    "19:00": "🇬🇧 کلاس شروع.\n||19:00||",
    "20:30": "📘 مرور زبان.\n||20:30||",
    "21:40": "🎒 آماده فردا.\n||21:40||",
    "23:00": "🌙 خواب.\n||23:00||"
}

schedule_jome = {
    "08:30": "⏰ بیدار شو!\n||08:30||",
    "09:10": "🍳 صبحانه.\n||09:10||",
    "10:00": "📚 درس 1.\n||10:00||",
    "11:20": "✏️ تمرین.\n||11:20||",
    "12:00": "🍛 ناهار.\n||12:00||",
    "14:00": "📖 درس 2.\n||14:00||",
    "15:00": "🤸‍♂️ ورزش.\n||15:00||",
    "17:00": "📚 درس 3.\n||17:00||",
    "20:00": "🧾 جمع‌بندی.\n||20:00||",
    "21:00": "🎮 تفریح.\n||21:00||",
    "23:00": "🌙 خواب.\n||23:00||"
}

# -------------------------
# ⚡ جمله انگیزشی تصادفی
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

    send("🔥 *ثبت شد!* تو ساعت " + now.strftime("%H:%M") + " بیدار شدی.")

    first_task = datetime.datetime.strptime(FIRST_TASK_TIME, "%H:%M")
    first_task = now.replace(hour=first_task.hour, minute=first_task.minute)

    delta = first_task - now
    minutes_left = int(delta.total_seconds() / 60)

    if minutes_left > 20:
        send(f"⏳ {minutes_left} دقیقه وقت داری — یه شروع آروم کن.")
    elif minutes_left > 5:
        send(f"⚡ {minutes_left} دقیقه وقت داری. آماده شو.")
    else:
        send(f"🚨 عجله کن! فقط {minutes_left} دقیقه مونده!")

# -------------------------
# 🎮 بخش گیم (فقط زمان استراحت)
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
    for start, end in rest_ranges:
        if start <= now <= end:
            return True
    return False

word_game_words = ["boxer", "strong", "energy", "focus", "study", "victory"]

def shuffle_word(word):
    letters = list(word)
    random.shuffle(letters)
    return "".join(letters)

@bot.message_handler(commands=['game'])
def game_menu(message):
    if not is_rest_time():
        bot.reply_to(message, "⛔ الان وقت کاره قهرمان! تو زمان استراحت بازی می‌دم 🔥")
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

    bot.reply_to(message, "🎮 *یه بازی انتخاب کن قهرمان:*", reply_markup=keyboard, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("game_"))
def game_handler(call):

    if not is_rest_time():
        bot.answer_callback_query(call.id, "⛔ الان وقت گیم نیست!")
        return

    if call.data == "game_number":
        number = random.randint(1, 20)
        bot.send_message(call.message.chat.id,
                         f"🔢 *عدد مخفی:* `{number}`\nساده بود، نسخه بعد سخت‌تر می‌کنم!",
                         parse_mode="Markdown")

    elif call.data == "game_rps":
        choice = random.choice(["✊ سنگ", "✋ کاغذ", "✌️ قیچی"])
        bot.send_message(call.message.chat.id, f"✊✋✌️ *انتخاب من:* {choice}", parse_mode="Markdown")

    elif call.data == "game_lottery":
        nums = random.sample(range(1, 40), 5)
        bot.send_message(call.message.chat.id,
                         f"🎰 *اعداد شانس:* `{nums}`",
                         parse_mode="Markdown")

    elif call.data == "game_word":
        word = random.choice(word_game_words)
        mixed = shuffle_word(word)
        bot.send_message(call.message.chat.id,
                         f"🧠 *کلمه:* `{mixed}`\nمی‌تونی درستش کنی؟",
                         parse_mode="Markdown")

    elif call.data == "game_luck":
        luck_list = [
            "🍀 امروز شانس باهاته!",
            "🔥 انرژی بالاست، استفاده کن!",
            "😎 روز خفنی در راهه!",
            "🤣 یه چیز عجیب امروز میشه!",
            "⚡ آماده یه سورپرایز باش!"
        ]
        bot.send_message(call.message.chat.id, random.choice(luck_list))

# -------------------------
# 🔁 حلقه اصلی
# -------------------------
def time_checker():
    while True:
        now = datetime.datetime.now()
        day = now.weekday()
        current = now.strftime("%H:%M")

        check_birthday()

        if current == "08:20":
            send(random.choice(motivations))

        if day in [5, 0, 2] and current in schedule_zoj:
            send(schedule_zoj[current])

        if day in [6, 1, 3] and current in schedule_fard:
            send(schedule_fard[current])

        if day == 4 and current in schedule_jome:
            send(schedule_jome[current])

        time.sleep(30)

# -------------------------
# 🚀 اجرای ربات روی Render
# -------------------------
def start_bot():
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + "/webhook")
    Thread(target=time_checker).start()

start_bot()
app.run(host="0.0.0.0", port=10000)
