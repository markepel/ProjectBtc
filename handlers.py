import telegram
from telegram.ext import CommandHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(bot, update):
  reply_keyboard = [['Стратегии'], ['Обучение','О боте'], ['Настройки', 'Личный кабинет']]
  bot.send_message(chat_id=update.message.chat_id, text="Start clicked. Follow start!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  

def info(bot, update):
  reply_keyboard = [['Стратегии'], ['Обучение','О боте'], ['Настройки', 'Личный кабинет']]
  bot.send_message(chat_id=update.message.chat_id, text="Info clicked. Enjoy info!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def setHandlers(dp):
  start_handler = CommandHandler('start', start)
  info_handler = CommandHandler('info', info)
  dp.add_handler(start_handler)
  dp.add_handler(info_handler)


