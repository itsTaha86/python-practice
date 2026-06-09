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

telebot.apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
