import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config

reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
#finishPattern = '^(/finish)$'
anyTextPattern ="^(?!.*(Отменить обращение))"
onlyDigitsPattern = "^\d+$"
global reply_state
reply_state = {}
logger = logging.getLogger('btcLogger')

PASSWORD, GETTEXT, GETCHATID, FINISH = range(4)

def publishReply(bot, update):
  logger.info('publishReply starts for chat_id {0}'.format(update.message.chat_id))
  global reply_state
  logger.info('Initial reply_state - {0} in publishReply for chat_id {1}'.format(reply_state, update.message.chat_id))
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите текст ответа:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return GETTEXT

def text(bot, update):
  global reply_state
  reply_state["text_for_{0}".format(update.message.chat_id)] = update.message.text
  bot.send_message(chat_id=update.message.chat_id, text="Введите идентификатор пользователя:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  logger.info('reply_state - {0} for text in publishReply for chat_id {1}'.format(reply_state, update.message.chat_id))

  return GETCHATID

def chatId(bot, update):
  global reply_state
  reply_state["chatid_for_{0}".format(update.message.chat_id)] = update.message.text
  logger.info('publishReply sends to user with id {0}'.format(update.message.text))
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации или /cancel для отмены.")
  logger.info('reply_state - {0} for chatId in publishReply for chat_id {1}'.format(reply_state, update.message.chat_id))

  return FINISH

def finish(bot, update):
  try:
    global reply_state
    logger.info('reply_state - {0} on finish in publishReply for chat_id {1}'.format(reply_state["text_for_{0}".format(update.message.chat_id)], update.message.chat_id))
    #bot.send_message(chat_id=reply_state["chatid_for_{0}".format(update.message.chat_id)], text="{0}".format(reply_state["text_for_{0}".format(update.message.chat_id)]), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=reply_state["chatid_for_{0}".format(update.message.chat_id)], text="<b>Ответ от службы поддержки:</b> \n {0}".format(reply_state["text_for_{0}".format(update.message.chat_id)]), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

    bot.send_message(chat_id=update.message.chat_id, text="Ответ отправлен.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    del reply_state["chatid_for_{0}".format(update.message.chat_id)]
    logger.info('publishReply finished successfully. Reply = {0}'.format(reply_state["text_for_{0}".format(update.message.chat_id)]))
    del reply_state["text_for_{0}".format(update.message.chat_id)]
    logger.info('reply_state - {0} after finish in publishReply for chat_id {1}'.format(reply_state, update.message.chat_id))
  except Exception as e:
    logger.exception(e)
  finally:
    return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  global reply_state
  logger.info('reply_state - {0} on cancel in publishReply for chat_id {1}'.format(reply_state, update.message.chat_id))
  if "chatid_for_{0}".format(update.message.chat_id) in reply_state:
    del reply_state["chatid_for_{0}".format(update.message.chat_id)]
  if "text_for_{0}".format(update.message.chat_id) in reply_state:
    del reply_state["text_for_{0}".format(update.message.chat_id)]
  logger.info('reply_state - {0} after cancel in publishReply for chat_id {1}'.format(reply_state, update.message.chat_id))
  return ConversationHandler.END

publishreply_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('publishreply', publishReply)],
  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  GETTEXT: [RegexHandler(anyTextPattern, text)],
  GETCHATID: [RegexHandler(onlyDigitsPattern, chatId)],
  FINISH: [CommandHandler('finish', finish)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_publishreply_conv_handler():
  return publishreply_conv_handler