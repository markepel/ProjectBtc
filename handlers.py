import telegram
from telegram.ext import (CommandHandler,MessageHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from manageStrategiesConversationHandlers import get_addstrategy_conv_handler

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handlers = []
reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]
db = DBRepo()
db.setup()

def getDB():
  return db

def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Start clicked. Follow start!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  
def profile(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это личный кабинет!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def signals(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это сигналы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def strategies(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это стратегии!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def stuff(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это обучающие материалы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def contacts(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это служба поддержки!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def setHandlers(dp):
  handlers.append(CommandHandler('start', start))
  handlers.append(RegexHandler('Личный кабинет', profile))
  handlers.append(RegexHandler('Сигналы', signals))
  handlers.append(RegexHandler('Стратегии', strategies))
  handlers.append(RegexHandler('Материалы', stuff))
  handlers.append(RegexHandler('Служба поддержки', contacts))
  handlers.append(get_addstrategy_conv_handler())


  for handler in handlers:
  	dp.add_handler(handler)
  


