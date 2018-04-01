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

db = DBRepo()
reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
global strategy_state 
strategy_state = {}
logger = logging.getLogger('btcLogger')

PASSWORD, CHOOSESTRATEGY, GETPHOTO, GETTEXT, FINISH = range(5)

def publishStrategy(bot, update):
  logger.info('publishStrategy starts for chat_id {0}'.format(update.message.chat_id))
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
  bot.send_message(chat_id=update.message.chat_id, text="Картинка для публикации:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return GETPHOTO

def photo(bot, update):
  global strategy_state
  strategy_state[update.message.chat_id].setPhotoId(update.message.photo[-1].file_id)

  bot.send_message(chat_id=update.message.chat_id, text="Введите текст для публикации:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  print("return GETTEXT")
  return GETTEXT

def text(bot, update):
  global strategy_state
  strategy_state[update.message.chat_id].setText(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return FINISH

def finish(bot, update):
  logger.info('publishStrategy finish starts for chat_id {0}'.format(update.message.chat_id))
  db = DBRepo()
  global strategy_state
  strategyName = strategy_state[update.message.chat_id].strategyName
  idsToPublishBig = db.get_active_subscribers_ids_for_strategy_by_name(strategyName)
  logger.info('idsToPublishBig - {0}'.format(idsToPublishBig))
  for idsToPublish in idsToPublishBig:
    for id in idsToPublish:
      text = """
      <b>Урок стратегии "{1}":</b>
      {0}
       """.format(strategy_state[update.message.chat_id].text, strategyName)
      bot.send_photo(chat_id=id, photo=strategy_state[update.message.chat_id].photoId, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
      bot.send_message(chat_id=id, text=text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
      time.sleep(0.04)

  bot.send_message(chat_id=update.message.chat_id, text="Публикация стратегии разослана подписантам.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  logger.info('publishStrategy finished successfully for chat_id {0}. Strategy = '.format(update.message.chat_id, strategy_state[update.message.chat_id]))
  del strategy_state[update.message.chat_id]
  return ConversationHandler.END

def cancel(bot, update):
  global strategy_state
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  if update.message.chat_id in signal_state:
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