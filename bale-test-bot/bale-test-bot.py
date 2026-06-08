# Imports
import telebot
from telebot import apihelper, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import logging
import sqlite3
from dotenv import load_dotenv

load_dotenv()


conn = sqlite3.connect("files.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS files
                  (id INTEGER PRIMARY KEY, file_id TEXT, file_type TEXT)""")
conn.commit()
conn.close()


def add_file_id(file_id, file_type):
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO files (file_id, file_type) VALUES (?, ?)", (file_id, file_type)
    )
    conn.commit()
    conn.close()


def get_file_id():
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM files")
    result = cursor.fetchall()
    conn.close()
    for x in result:
        return x if x else None


# Set API_URL and API_TOKEN
telebot.apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Set logger
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


# # Work with message_handler
@bot.message_handler(func=lambda message: message.text == "شروع")
def say_hello(message):
    bot.reply_to(message, "سلام پفیوز")
    bot.register_next_step_handler(message, ask_name)
    logger.info(message.from_user.id)


def ask_name(message):
    bot.reply_to(message, "اسمت چیه پفیوز؟")
    bot.register_next_step_handler(message, ask_age)


def ask_age(message):
    bot.reply_to(message, "چند سالته پفیوز؟")


# Keyboard Buttons
keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button0 = types.KeyboardButton("/options")
button1 = types.KeyboardButton("دستور اول")
button2 = types.KeyboardButton("دستور دوم")
button3 = types.KeyboardButton("دستور سوم")
keyboard.add(button0, button3)
keyboard.add(button1, button2)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message, "سلام! یکی از دستورات زیر را انتخاب کنید:", reply_markup=keyboard
    )


# Inline Keyboard Buttons
markup = InlineKeyboardMarkup()
option_1 = InlineKeyboardButton("گزینه 1", callback_data="option1")
option_2 = InlineKeyboardButton("گزینه 2", callback_data="option2")
option_3 = InlineKeyboardButton("خدافظی", callback_data="delete")
markup.add(option_1, option_2)
markup.add(option_3)


@bot.message_handler(commands=["options"])
def hello(message):
    bot.reply_to(message, "انتخاب کن:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def options(call):
    if call.data == "option1":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="شما گزینه 1 را انتخاب کردید",
        )
    if call.data == "option2":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="شما گزینه 2 را انتخاب کردید",
        )
    if call.data == "delete":
        bot.answer_callback_query(call.id, "بای بای", show_alert=True)
        bot.delete_message(
            chat_id=call.message.chat.id, message_id=call.message.id, timeout=10
        )


# ------------------------------------------------------------------------- #


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    file_id = message.photo[-1].file_id
    add_file_id(file_id, "Photo")
    bot.reply_to(message, "عکس شما دریافت شد")


@bot.message_handler(commands=["photo"])
def send_photo(message):
    file_id = get_file_id()
    logger.info(file_id)
    if file_id:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=file_id[0],
            caption="بفرمایید",
        )
    else:
        bot.reply_to(message, "NOT EXISTS!")


logging.basicConfig(level="INFO")


bot.infinity_polling()
