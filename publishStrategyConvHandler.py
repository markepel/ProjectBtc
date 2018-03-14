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
reply_keyboard_main_menu = [['Стратегии 🥇'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
strategy_state = {}


PASSWORD, CHOOSESTRATEGY, GETPHOTO, GETTEXT, FINISH = range(5)

def publishStrategy(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Выберите в меню стратегию для публикации, пожалуйста:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return CHOOSESTRATEGY

def name(bot, update):
  publishStrategyInfo = PublishStrategyInfo()
  publishStrategyInfo.setStrategyName(update.message.text) 
  global strategy_state
  strategy_state[update.message.chat_id] = publishStrategyInfo
  bot.send_message(chat_id=update.message.chat_id, text="Картинка для публикации:")
  return GETPHOTO

def photo(bot, update):
  global strategy_state
  strategy_state[update.message.chat_id].setPhotoId(update.message.photo[-1].file_id)

  bot.send_message(chat_id=update.message.chat_id, text="Введите текст для публикации:")
  print("return GETTEXT")
  return GETTEXT

def text(bot, update):
  global strategy_state
  strategy_state[update.message.chat_id].setText(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.")
  return FINISH

def finish(bot, update):
  db = DBRepo()
  global strategy_state
  idsToPublishBig = db.get_active_subscribers_ids_for_strategy_by_name(strategy_state[update.message.chat_id].strategyName)
  print("Ids to publish idsToPublishBig  -- ", idsToPublishBig)

  for idsToPublish in idsToPublishBig:
    for id in idsToPublish:
      print("Idsdddddddddd -- ", id)

      bot.send_photo(chat_id=id, photo=strategy_state[update.message.chat_id].photoId, caption = strategy_state[update.message.chat_id].text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
      time.sleep(0.03)

  bot.send_message(chat_id=update.message.chat_id, text="Публикация стратегии разослана подписантам.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  del strategy_state[update.message.chat_id]
  return ConversationHandler.END

def cancel(bot, update):
  global strategy_state
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  del strategy_state[update.message.chat_id]
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