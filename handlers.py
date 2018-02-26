import telegram
from telegram.ext import (CommandHandler,MessageHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handlers = []
reply_keyboard = [['Стратегии'], ['Обучение','О боте'], ['Служба поддержки', 'Личный кабинет']]
db = DBRepo()
db.setup()

def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Start clicked. Follow start!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  
def profile(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это личный кабинет!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def risks(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это риски!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def strategies(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это стратегии!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def stuff(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это обучающие материалы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def contacts(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это служба поддержки!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def about(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это о боте!", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def setHandlers(dp):
  handlers.append(CommandHandler('start', start))
  handlers.append(RegexHandler('Личный кабинет', profile))
  handlers.append(RegexHandler('Риски', risks))
  handlers.append(RegexHandler('Стратегии', strategies))
  handlers.append(RegexHandler('Обучение', stuff))
  handlers.append(RegexHandler('Служба поддержки', contacts))
  handlers.append(RegexHandler('О боте', about))

  for handler in handlers:
  	dp.add_handler(handler)
  


