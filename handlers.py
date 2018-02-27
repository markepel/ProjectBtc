import telegram
from telegram.ext import (CommandHandler,MessageHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from manageStrategiesConversationHandlers import get_addstrategy_conv_handler
from texts import Texts
from menus import Menus
from strategy import Strategy

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handlers = []
reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
db = DBRepo()
db.setup()
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
print('============', strategyNamesRegex)
goBackTo = 'start'

def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextOnStart(update.message.from_user.first_name), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  
def profile(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это личный кабинет!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def signals(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это сигналы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def strategies(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForStrategies(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True))

def stuff(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это обучающие материалы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def contacts(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это служба поддержки!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def strategy(bot, update):
  db = DBRepo()
  print('==============Text ', update.message.text)
  print('--------------dbObj', db.get_strategy_by_name(update.message.text)[0])
  strategyItself = Strategy.fromDbObject(db.get_strategy_by_name(update.message.text)[0])
  print('==============SSSS ', strategyItself)
  bot.send_message(chat_id=update.message.chat_id, text=strategyItself.description, reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True))


def backToMainMenu(bot, update):
  possibles = globals().copy()
  possibles.update(locals())
  method = possibles.get(goBackTo)
  method(bot, update)



def setHandlers(dp):
  handlers.append(CommandHandler('start', start))
  handlers.append(RegexHandler('Личный кабинет', profile))
  handlers.append(RegexHandler('Сигналы', signals))
  handlers.append(RegexHandler('Стратегии', strategies))
  handlers.append(RegexHandler('Материалы', stuff))
  handlers.append(RegexHandler('Служба поддержки', contacts))
  handlers.append(RegexHandler('🔙Назад', backToMainMenu))
  handlers.append(get_addstrategy_conv_handler())
  handlers.append(RegexHandler(strategyNamesRegex, strategy))


  for handler in handlers:
  	dp.add_handler(handler)
  


