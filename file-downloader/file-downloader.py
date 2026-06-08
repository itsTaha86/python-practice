import telebot
import os
from dotenv import load_dotenv
import logging
import requests

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

load_dotenv()

telebot.apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

if not os.path.exists("./downloads"):
    os.mkdir("./downloads")

DOWNLOAD_DIR = "./downloads/"


def download_file(url):
    local_filename = url.split("/")[-1]
    file_path = DOWNLOAD_DIR + local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, "برای استفاده از دانلودر از دستور /download استفاده کنید"
    )


@bot.message_handler(commands=["download"])
def get_ready(message):
    bot.reply_to(message, text="لینک فایل مدنظر خود را بفرستید 👇")
    bot.register_next_step_handler(message, download)


def download(message):
    url = message.text
    file_path = download_file(url)
    try:
        bot.send_document(
            chat_id=message.chat.id,
            reply_to_message_id=message.id,
            document=open(file_path, "rb"),
            caption="بفرمایید",
        )
        os.remove(file_path)
    except:
        bot.reply_to(message, text="مشکلی پیش آمد\nمجدد تلاش کنید")


bot.infinity_polling()
