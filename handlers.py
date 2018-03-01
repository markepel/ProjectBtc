import telegram
from telegram.ext import (CommandHandler,MessageHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
import logging
from dbrepo import DBRepo
import botconfig as config
from manageStrategiesConversationHandlers import get_addstrategy_conv_handler
from texts import Texts
from menus import Menus
from strategy import Strategy
from paymentHandler import handlePayment
from werkzeug.datastructures import ImmutableMultiDict

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db = DBRepo()
db.setup()
handlers = []
reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
goBackTo = 'start'


def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextOnStart(update.message.from_user.first_name), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  #bot.send_photo(chat_id=update.message.chat_id, photo='https://www.iconexperience.com/_img/o_collection_png/green_dark_grey/256x256/plain/dog.png')
def profile(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это личный кабинет!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
def signals(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это сигналы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def strategies(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForStrategies(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True))

def stuff(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это обучающие материалы!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def contacts(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Это служба поддержки!", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))

def strategy(bot, update):
  db = DBRepo()
  strategyItself = Strategy.fromDbObject(db.get_strategy_by_name(update.message.text)[0])
  keyboard = [[InlineKeyboardButton('Купить данную стратегию за ' + str(strategyItself.price) + '₽', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generatePaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]]
  bot.send_message(chat_id=update.message.chat_id, text=strategyItself.description, reply_markup=InlineKeyboardMarkup(keyboard))

def getAllStrategiesInfo(bot, update):
  db = DBRepo()
  bot.send_message(chat_id=update.message.chat_id, text=db.get_all_strategies(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True))
  

def paymentCheck(bot, update):
  inputInvoiceData = ImmutableMultiDict([
('invoice_status', 'paid'), 
('invoice_expires', '1519824248'), 
('invoice_currency', 'usd'), 
('checkout_address', 'your_address_goes_here'), 
('invoice_id', 'your_token_goes_here'), 
('secret_hash', 'b1a6bacbe4c948b795f713d7b88224d313aa1400'), 
('checkout_amount', '0.00010000'), 
('invoice_created', '1519822448'), 
('invoice_url', 'https://www.cryptonator.com/merchant/invoice/your_token_goes_here'), ('date_time', '1519823448'), 
('order_id', '00001'),
('checkout_currency', 'bitcoin'), 
('invoice_amount', '5.5'), 
('merchant_id', 'c19abb8aeca27d180d2f82e04a933f72')])
  fakeInvoice = inputInvoiceData.to_dict(flat=True)
  handlePayment(fakeInvoice)


def backToMainMenu(bot, update):
  possibles = globals().copy()
  possibles.update(locals())
  method = possibles.get(goBackTo)
  method(bot, update)



def setHandlers(dp):
  handlers.append(CommandHandler('start', start))
  handlers.append(RegexHandler('Личный кабинет', profile))
  handlers.append(RegexHandler('Сигналы', signals))
  handlers.append(RegexHandler('Стратегии', strategies))
  handlers.append(RegexHandler('Материалы', stuff))
  handlers.append(RegexHandler('Служба поддержки', contacts))
  handlers.append(RegexHandler('🔙Назад', backToMainMenu))
  handlers.append(get_addstrategy_conv_handler())
  handlers.append(RegexHandler(strategyNamesRegex, strategy))
  handlers.append(CommandHandler('testpayment', paymentCheck))
  handlers.append(CommandHandler('requestAllStrategies', getAllStrategiesInfo))

  for handler in handlers:
  	dp.add_handler(handler)
  


