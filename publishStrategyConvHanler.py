import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from strategy import Strategy
from menus import Menus
from texts import Texts
from publishStrategyInfo import PublishStrategyInfo
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db = DBRepo()
reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
publishStrategyInfo = PublishStrategyInfo()


PASSWORD, CHOOSESTRATEGY, GETPHOTO, GETTEXT, FINISH = range(5)

def publishStrategy(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Выберите в меню стратегию для публикации, пожалуйста:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True))
  return CHOOSESTRATEGY

def name(bot, update):
  publishStrategyInfo.setStrategyName(update.message.text) 
  bot.send_message(chat_id=update.message.chat_id, text="Картинка для публикации:")
  return GETPHOTO

def photo(bot, update):
  publishStrategyInfo.setPhotoId(update.message.photo[-1].file_id)

  bot.send_message(chat_id=update.message.chat_id, text="Введите текст для публикации:")
  print("return GETTEXT")
  return GETTEXT

def text(bot, update):
  publishStrategyInfo.setText(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.")
  return FINISH

def finish(bot, update):
  db = DBRepo()
  idsToPublish = db.get_active_subscribers_ids_for_strategy_by_name(publishStrategyInfo.strategyName)[0]
  for id in idsToPublish:
    bot.send_photo(chat_id=id, photo=publishStrategyInfo.photoId, caption = publishStrategyInfo.text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    time.sleep(0.03)

  bot.send_message(chat_id=update.message.chat_id, text="Публикация стратегии разослана подписантам.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return ConversationHandler.END

publishstrategy_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('publishstrategy', publishStrategy)],
  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  CHOOSESTRATEGY: [RegexHandler(strategyNamesRegex, name)],
  GETPHOTO: [MessageHandler(Filters.photo, photo)],
  GETTEXT: [RegexHandler(anyTextPattern, text)],
  FINISH: [RegexHandler(finishPattern, finish)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_publishstrategy_conv_handler():
  return publishstrategy_conv_handler