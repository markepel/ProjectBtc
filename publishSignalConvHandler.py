import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
import time

reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
global signal_state
signal_state = {}
logger = logging.getLogger('btcLogger')

PASSWORD, GETPHOTO, GETTEXT, FINISH = range(4)

def publishSignal(bot, update):
  global signal_state
  logger.info('publishSignal starts for chat_id {0}'.format(update.message.chat_id))
  logger.info('Initial signal_state - {0} in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Картинка для публикации:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return GETPHOTO

def photo(bot, update):
  global signal_state
  logger.info('signal_state - {0} for photo in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))
  signal_state["photoId_for_{0}".format(update.message.chat_id)] = update.message.photo[-1].file_id

  bot.send_message(chat_id=update.message.chat_id, text="Введите текст для публикации:")
  return GETTEXT

def text(bot, update):
  global signal_state
  logger.info('signal_state - {0} for text in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))
  signal_state["text_for_{0}".format(update.message.chat_id)] = update.message.text
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.")
  return FINISH

def finish(bot, update):
  try:
    chatId = update.message.chat_id
    logger.info('publishSignal finish starts for chat_id {0}'.format(chatId))
    db = DBRepo()
    idsToPublishBig = db.get_all_active_subscriptions_ids_for_signals()
    logger.info('idsToPublishBig - {0}'.format(idsToPublishBig))
    global signal_state
    logger.info('signal_state - {0} on finish in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))
    text = """Сигнал:
{0}""".format(signal_state["text_for_{0}".format(chatId)])
    photoId = signal_state["photoId_for_{0}".format(chatId)]
    for idsToPublish in idsToPublishBig:
      id = idsToPublish[0]
      bot.send_photo(chat_id=id, photo=photoId, caption = text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
      time.sleep(0.03)
    bot.send_message(chat_id=chatId, text="Сигнал разослан подписантам.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    logger.info('publishSignal finished successfully for chat_id {0}. Signal - {1}'.format(chatId, signal_state["text_for_{0}".format(chatId)]))
    del signal_state["text_for_{0}".format(update.message.chat_id)]
    del signal_state["photoId_for_{0}".format(update.message.chat_id)]
    logger.info('signal_state - {0} for after finish in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))
  except Exception as e:
    logger.error("EEERRROOORRR")
    #e = traceback.format_exc()
    print("XXX")
    logger.info("XXX")
    print(e)
    logger.info(e)
    print("YYY")
    logger.info("YYY")
  finally:
    return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  global signal_state
  logger.info('signal_state - {0} on cancel in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))
  if "text_for_{0}".format(update.message.chat_id) in signal_state:
    del signal_state["text_for_{0}".format(update.message.chat_id)]
  if "photoId_for_{0}".format(update.message.chat_id) in signal_state:
    del signal_state["photoId_for_{0}".format(update.message.chat_id)]
  logger.info('signal_state - {0} after cancel in publishSignal for chat_id {1}'.format(signal_state, update.message.chat_id))

  return ConversationHandler.END

publishsignal_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('publishsignal', publishSignal)],
  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  GETPHOTO: [MessageHandler(Filters.photo, photo)],
  GETTEXT: [RegexHandler(anyTextPattern, text)],
  FINISH: [RegexHandler(finishPattern, finish)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_publishsignal_conv_handler():
  return publishsignal_conv_handler
