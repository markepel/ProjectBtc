import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,CallbackQueryHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton)
import logging
import botconfig as config
import smtplib
from email.message import EmailMessage


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

anyTextPattern = "^(?![Хуй])^(?!\s*$).+"
cancelTextPattern = '^(Отменить)$'

reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]

SENDEMAIL, CANCELEMAIL = range(2)

def email(bot, update):
  keyboard = [['Отменить обращение']]
  bot.send_message(chat_id=update.callback_query.message.chat.id, text="Введите ваше обращение. Если вы хотите получить ответ не в боте, а по email, укажите его адрес в теле обращения, пожалуйста:", reply_markup = ReplyKeyboardMarkup(keyboard))
  return SENDEMAIL
 
def sendEmail(bot, update):
  if update.message.text == "Отменить обращение":
    bot.send_message(chat_id=update.message.chat_id, text="Обращение в службу поддержки отменено.", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))
  else:
    sendEmail(update.message.text + '\n chat_id = {0}'.format(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text="Ваше обращение принято к рассмотрению.", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))
  return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Обращение в службу поддержки отменено.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  return ConversationHandler.END

support_conv_handler = ConversationHandler(
  entry_points=[CallbackQueryHandler(email)],

  states={
  SENDEMAIL: [RegexHandler(anyTextPattern, sendEmail)],
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def sendEmail(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Обращение пользователя'
    msg['From'] = config.EMAILFROM
    msg['To'] = config.EMAILTO
    conn = smtplib.SMTP("smtp.gmail.com")
    conn.ehlo()
    conn.starttls()
    conn.ehlo()
    conn.set_debuglevel(True)
    conn.login(config.EMAILFROM, 'QA1WS2ed3')
    conn.send_message(msg)
    conn.quit()

def get_support_conv_handler():
  return support_conv_handler
