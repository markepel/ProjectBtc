import telegram
from telegram.ext import (CommandHandler,MessageHandler,ConversationHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
from dbrepo import DBRepo
import botconfig as config
from strategy import Strategy


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

reply_keyboard = [['Завершить'], ['Отменить']]
reply_keyboard_main = [['Стратегии'], ['Обучение','О боте'], ['Служба поддержки', 'Личный кабинет']]
urlPattern = "((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w_-]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)"
delayUrlPattern = "(((^(\d{1}|\d{2}|\d{3})\s[A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w_-]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)|^(/finish)$|^(Завершить)$"
anyTextPattern = "^(?!\s*$).+"
pricePattern = "^([1-9][0-9][0-9])$|^([1-9][0-9][0-9][0-9])$|^([1-9][0-9][0-9][0-9][0-9])$"
strategyToAdd = Strategy.empty()

PASSWORD, NAME, DESCRIPTION, RIGHTAWAYLINK, PRICE, LINK = range(6)

def addStrategy(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите, пожалуйста, пароль:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  return PASSWORD
 
def password(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Введите название добавляемой стратегии, пожалуйста:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  return NAME

def name(bot, update):
  strategyToAdd.set_name(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Краткое описание добавляемой стратегии:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  return DESCRIPTION

def description(bot, update):
  strategyToAdd.set_description(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите ссылку, которую получит клиент сразу после подтверждения оплаты:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  return RIGHTAWAYLINK

def rightawayLink(bot, update):
  strategyToAdd.set_rightAwayLink(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Цена добавляемой стратегии:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  return PRICE

def price(bot, update):
  strategyToAdd.set_price(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text="Введите ссылку на материал по добавляемой стратегии и задержку выхода материала от момента покупки клиентом в формате\n Задержка(в сутках)(пробел)Ссылка(URL)\n Пример: 5 http://telegra.ph/ex-02-26", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
  return LINK

def link(bot, update):
  if update.message.text == '/finish' or update.message.text == 'Завершить':
    db = DBRepo()
    addedStrategyId = db.add_strategy(strategyToAdd.name, strategyToAdd.description, strategyToAdd.price, strategyToAdd.rightAwayLink, strategyToAdd.dateOfCreation)
    for delayLink in strategyToAdd.delayLinks:
      db.add_strategy_link(addedStrategyId, delayLink[0], delayLink[1])
    bot.send_message(chat_id=update.message.chat_id, text="Стратегия успешно добавлена!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main, one_time_keyboard=True))
    return ConversationHandler.END
  else:
    splitValues = update.message.text.split(' ')
    print("splitValues= " ,splitValues)
    strategyToAdd.add_delayLink(update.message.text.split(' '))
    bot.send_message(chat_id=update.message.chat_id, text="Ссылка добавлена. Продолжайте вводить ссылки и задержки в правильном формате\n Задержка(в сутках)(пробел)Ссылка(URL)\n Пример: 5 http://telegra.ph/ex-02-26\n Для завершения создания стратегии введите /finish или нажмите кнопку \"Завершить\" в меню", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return LINK  

def cancel(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Стратегия отменена")
  return ConversationHandler.END

addstrategy_conv_handler = ConversationHandler(
  entry_points=[CommandHandler('addstrategy', addStrategy)],

  states={
  PASSWORD: [RegexHandler(config.MANAGERPASS, password)],
  NAME: [RegexHandler(anyTextPattern, name)],
  DESCRIPTION: [RegexHandler(anyTextPattern, description)],
  RIGHTAWAYLINK: [RegexHandler(urlPattern, rightawayLink)],
  PRICE: [RegexHandler(pricePattern, price)],
  LINK: [RegexHandler(delayUrlPattern, link)]
  },

  fallbacks=[CommandHandler('cancel', cancel)]
)

def get_addstrategy_conv_handler():
  return addstrategy_conv_handler
