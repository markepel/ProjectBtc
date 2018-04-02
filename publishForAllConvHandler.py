import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from menus import Menus
from texts import Texts
import time

db = DBRepo()
reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
global forAll_state
forAll_state = {}
logger = logging.getLogger('btcLogger')

PASSWORD, GETTEXT, FINISH = range(3)

def publishForAll(bot, update):
  global forAll_state
  logger.info('Initial forAll_state - {0} in publishForAll for chat_id {1}'.format(forAll_state, update.message.chat_id))
  logger.info('PublishForAll Starts for chat_id = {0}'.format(update.message.chat_id))
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Выберите текст для публикации для всех юзеров, пожалуйста:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return GETTEXT

def text(bot, update):
  global forAll_state
  logger.info('forAll_state - {0} for text in publishForAll for chat_id {1}'.format(forAll_state, update.message.chat_id))
  forAll_state[update.message.chat_id] = update.message.text
  logger.info('PublishForAll text = {0}'.format(update.message.text))
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return FINISH

def finish(bot, update):
  try:
    db = DBRepo()
    global forAll_state
    logger.info('forAll_state - {0} on finish in publishForAll for chat_id {1}'.format(forAll_state, update.message.chat_id))
    idsToPublish = db.get_all_users_ids()
    logger.info('PublishForAll ids = {0}'.format(idsToPublish))
    for id in idsToPublish:
      id = id[0]
      try:
        bot.send_message(chat_id=id, text=forAll_state[update.message.chat_id], reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
        time.sleep(0.03)
      except Exception as e:
        print('Exception on send to all - ', e)
        db.delete_user(id)

    logger.info('PublishForAll finished for chat_id {0} successfully'.format(update.message.chat_id))
    del forAll_state[update.message.chat_id]
    logger.info('forAll_state - {0} after finish in publishForAll for chat_id {1}'.format(forAll_state, update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text="Публикация для всех юзеров разослана.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  except:
    e = traceback.format_exc()
    logger.error("An error occured on publishForAll forAll_state  = - \n {0}".format(forAll_state))  
    logger.error("Error itself = \n {0}".format(e).encode('utf-8'))
  finally:
    return ConversationHandler.END

def cancel(bot, update):
  global forAll_state
  logger.info('forAll_state - {0} on cancel in publishForAll for chat_id {1}'.format(forAll_state, update.message.chat_id))
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  if update.message.chat_id in forAll_state:
    del forAll_state[update.message.chat_id]
  logger.info('forAll_state - {0} after cancel in publishForAll for chat_id {1}'.format(forAll_state, update.message.chat_id))
  return ConversationHandler.END

publishforall_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('publishforall', publishForAll)],
  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  GETTEXT: [RegexHandler(anyTextPattern, text)],
  FINISH: [RegexHandler(finishPattern, finish)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_publishforall_conv_handler():
  return publishforall_conv_handler