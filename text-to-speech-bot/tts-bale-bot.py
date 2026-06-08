import telebot
import os
from dotenv import load_dotenv
import logging
from gtts import gTTS
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import apihelper, types

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

load_dotenv()

if not os.path.exists("./voices"):
    os.mkdir("./voices")

telebot.apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button0 = types.KeyboardButton("شروع مجدد")
keyboard.add(button0)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi\nWelcome to gTTS\nSend your text for me 👇")


@bot.message_handler(func=lambda message: True)
def tts(message):
    text = message.text
    filename = "voices/output.mp3"
    output = gTTS(text=text, lang="en", tld="com.eu")
    output.save(filename)
    bot.send_audio(
        message.chat.id,
        reply_to_message_id=message.id,
        audio=open(filename, "rb"),
        reply_markup=keyboard,
        caption="☝️",
    )
    os.remove(filename)


bot.infinity_polling()
