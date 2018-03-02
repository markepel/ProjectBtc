import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from publishReplyInfo import PublishReplyInfo


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
onlyDigitsPattern = "^\d+$"
publishReplyInfo = PublishReplyInfo()


PASSWORD, GETTEXT, GETCHATID, FINISH = range(4)

def publishReply(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите текст ответа:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return GETTEXT

def text(bot, update):
  publishReplyInfo.setText(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите идентификатор пользователя:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return GETCHATID

def chatId(bot, update):
  publishReplyInfo.setChatId(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации или /cancel для отмены.")
  return FINISH

def finish(bot, update):
  bot.send_message(chat_id=publishReplyInfo.chatId, text="<b>Ответ от службы поддержки</b> \n {0}".format(publishReplyInfo.text), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  bot.send_message(chat_id=update.message.chat_id, text="Ответ отправлен.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return ConversationHandler.END

publishreply_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('publishreply', publishReply)],
  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  GETTEXT: [RegexHandler(anyTextPattern, text)],
  GETCHATID: [RegexHandler(onlyDigitsPattern, chatId)],
  FINISH: [RegexHandler(finishPattern, finish)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_publishreply_conv_handler():
  return publishreply_conv_handler