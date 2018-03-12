import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
import time


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

reply_keyboard_main_menu = [['Стратегии 🥇'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
signal_state = {}


PASSWORD, GETTEXT, FINISH = range(3)

def publishSignal(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Выберите текст сигнала:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return GETTEXT

def text(bot, update):
  global signal_state
  signal_state["text_for_{0}".format(update.message.chat_id)] = update.message.text
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.")
  return FINISH

def finish(bot, update):
  db = DBRepo()
  idsToPublish = db.get_all_active_subscriptions_ids_for_signals()[0]
  global signal_state
  text = signal_state["text_for_{0}".format(update.message.chat_id)]
  for id in idsToPublish:
    bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    time.sleep(0.03)
  bot.send_message(chat_id=update.message.chat_id, text="Сигнал разослан подписантам.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  del signal_state["text_for_{0}".format(update.message.chat_id)]

  return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  global signal_state
  if "text_for_{0}".format(update.message.chat_id) in signal_state:
    del signal_state["text_for_{0}".format(update.message.chat_id)]
 
  return ConversationHandler.END

publishsignal_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('publishsignal', publishSignal)],
  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  GETTEXT: [RegexHandler(anyTextPattern, text)],
  FINISH: [RegexHandler(finishPattern, finish)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_publishsignal_conv_handler():
  return publishsignal_conv_handler