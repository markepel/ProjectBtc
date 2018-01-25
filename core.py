import json
import requests
import threading
import botconfig as config
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


TOKEN = config.TOKEN
bot = telegram.Bot(token=TOKEN)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def start(bot, update):
    reply_keyboard = [['Стратегии'], ['Обучение','О боте'], ['Настройки', 'Личный кабинет']]
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()