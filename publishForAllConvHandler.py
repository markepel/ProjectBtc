import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from menus import Menus
from texts import Texts
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db = DBRepo()
reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
finishPattern = '^(/finish)$'
anyTextPattern = "^(?![/cancel])^(?!\s*$).+"
forAll_state = {}


PASSWORD, GETTEXT, FINISH = range(3)

def publishForAll(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:")
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Выберите текст для публикации для всех юзеров, пожалуйста:", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return GETTEXT

def text(bot, update):
  global forAll_state
  forAll_state[update.message.chat_id] = update.message.text
  bot.send_message(chat_id=update.message.chat_id, text="Введите /finish для завершения и публикации ли /cancel для отмены.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return FINISH

def finish(bot, update):
  db = DBRepo()
  global forAll_state
  idsToPublish = db.get_all_users_ids()
  for id in idsToPublish:
    id = id[0]
    try:
      bot.send_message(chat_id=id, text=forAll_state[update.message.chat_id], reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
      time.sleep(0.03)
    except Exception as e:
      print('Exception on send to all - ', e)
      db.delete_user(id)


  bot.send_message(chat_id=update.message.chat_id, text="Публикация для всех юзеров разослана.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  return ConversationHandler.END

def cancel(bot, update):
  global forAll_state
  bot.send_message(chat_id=update.message.chat_id, text="Отмена публикации", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  del forAll_state[update.message.chat_id]
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