import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,CallbackQueryHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton)
import logging
import botconfig as config
import smtplib
from email.message import EmailMessage

anyTextPattern = "^(?!.*(Отменить обращение))"
startSupportRequestTextPattern = '^(Служба поддержки 📞)$'
cancelTextPattern = '^(Отменить обращение)$'
logger = logging.getLogger('btcLogger')

reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]

SENDEMAIL = range(1)

def email(bot, update):
  keyboard = [['Отменить обращение']]
  logger.info('Someone starts writing to support. Chat id = {0}'.format(update.message.chat.id))
  bot.send_message(chat_id=update.message.chat.id, text="Введите ваше обращение. Если вы хотите получить ответ не в боте, а по email, укажите его адрес в теле обращения, пожалуйста. Конечно, вы всегда можете отправить его вручную на {0}.".format(config.EMAILTO), reply_markup = ReplyKeyboardMarkup(keyboard))
  return SENDEMAIL
 
def sendEmail(bot, update):
  try:
    messageText = update.message.text + '\n chat_id = {0}'.format(update.message.chat_id)
    sendEmail(messageText)
    bot.send_message(chat_id=update.message.chat_id, text="Ваше обращение принято к рассмотрению.", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))
    logger.info('Chat id = {0} successfully finished his support request. Request - '.format(update.message.chat_id, messageText))
  except Exception as e:
    logger.exception(e)
  finally:
    return ConversationHandler.END

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Обращение в службу поддержки отменено.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  logger.info('Cancel Chat id = {0} canceled his support request'.format(update.message.chat_id))

  return ConversationHandler.END

support_conv_handler = ConversationHandler(
  entry_points=[RegexHandler(startSupportRequestTextPattern, email)],

  states={
  SENDEMAIL: [RegexHandler(anyTextPattern, sendEmail)],
  },

  fallbacks=[RegexHandler(cancelTextPattern, cancel)]
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
    conn.login(config.EMAILFROM, config.EMAILFROMPAS)
    conn.send_message(msg)
    conn.quit()

def get_support_conv_handler():
  return support_conv_handler
