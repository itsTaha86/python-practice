# Imports
import telebot
import os
from dotenv import load_dotenv
import logging
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Set logger and telebot
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Set API Token
# Gets token from .env file in project's folder
load_dotenv()

telebot.apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Global variables
TICKETS = {}
ADMIN_IDS = set()
USERS = {}


# bot's Keyboard
markup = InlineKeyboardMarkup()
contact_support = InlineKeyboardButton(text="ارتباط با پشتیبانی", callback_data="contact_support")
submit_ticket = InlineKeyboardButton(text="ثبت تیکت", callback_data="submit_ticket")
markup.add(contact_support)
markup.add(submit_ticket)

# ------------------ #
@bot.message_handler(commands=["start"])
def greeting(message):
        bot.send_message(chat_id=message.chat.id, text="سلام\nچطور میتونم کمکتون کنم؟", reply_markup=markup)

# ------------------ #
@bot.message_handler(func=lambda m: True)
def track_users(message):
    if message.from_user.username:
        USERS[message.from_user.username] = message.from_user.id

# ------------------ #
@bot.message_handler(commands=["add_admin"])
def add_admin(message):
        bot.send_message(message.chat.id, "آیدی ادمین جدید را بدون @ وارد کنید")
        user_id = message.text
        from_user = USERS[user_id]
        
        global ADMIN_IDS
        ADMIN_IDS.add(from_user)


# ------------------ #
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
        if call.data == "contact_support":
                bot.answer_callback_query(call.id, text="پشتیبانی 24 ساعته پاسخگوی شماست", show_alert=True)
                bot.send_message(call.message.chat.id, "برای ارتباط با پشتیبانی با شماره زیر تماس بگیرید:\n09121234567")
        if call.data == "submit_ticket":
                bot.answer_callback_query(call.id, text="تیکت خود را ثبت کنید، در اسرع وقت رسیدگی خواهد شد", show_alert=True)
                bot.register_next_step_handler(call.message,get_ticket)
                bot.send_message(call.message.chat.id, text="تیکت خود را بنویسید")

def get_ticket(message):

        global TICKETS
        
        TICKETS[message.chat.id] = {"text": message.text,
                                    "status": "open"
                                    }
                
        bot.reply_to(message, "تیکت شما ثبت شد.")
        
# ------------------ #        
@bot.message_handler(commands=["answer_ticket"])
def show_tickets(message):
        
        global ADMIN_IDS
        
        allowed_ids = ADMIN_IDS
        
        if message.from_user.id in allowed_ids:
        
                global TICKETS
                if not TICKETS:
                        bot.send_message(message.chat.id, "تیکتی وجود ندارد")
                        return
                
                chat_id = list(TICKETS.keys())[0]
                bot.send_message(chat_id=message.chat.id, text=TICKETS[chat_id]["text"])
                bot.send_message(chat_id=message.chat.id, text="پاسخ خود را برای این تیکت بنویسید")
                bot.register_next_step_handler(message,
                                               lambda m: answer_ticket(m, chat_id))

def answer_ticket(message, chat_id):
        answer_text = message.text
        bot.send_message(chat_id=chat_id, text=f"پاسخ پشتیبان:\n{answer_text}")
        
        global TICKETS
        
        TICKETS.pop(chat_id, None)
# ------------------ #


bot.infinity_polling()