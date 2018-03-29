import telegram
from telegram.ext import (CommandHandler,MessageHandler,RegexHandler,CallbackQueryHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
import logging
from dbrepo import DBRepo
import botconfig as config
from manageStrategiesConversationHandlers import get_addstrategy_conv_handler
from supportConversationHandler import get_support_conv_handler
from texts import Texts
from menus import Menus
from strategy import Strategy
from paymentHandler import handlePayment
from werkzeug.datastructures import ImmutableMultiDict
import datetime
from publishStrategyConvHandler import get_publishstrategy_conv_handler
from publishSignalConvHandler import get_publishsignal_conv_handler
from publishSupportReplyConvHandler import get_publishreply_conv_handler
from publishForAllConvHandler import get_publishforall_conv_handler


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db = DBRepo()
db.setup()
handlers = []
reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
goBackTo = 'start'


def start(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextOnStart(update.message.from_user.first_name), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  db = DBRepo()
  db.add_user(update.message.from_user.id, update.message.from_user.first_name)  

def cancelEmail(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text="Обращение отменено.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def profile(bot, update):
  db = DBRepo()
  activeStrategySubscriptions = db.get_active_subscriptions_for_strategies_by_user_id(int(update.message.chat_id))
  signalsSubscriptionsDb = db.get_active_subscriptions_for_signals_by_user_id(int(update.message.chat_id))
  strategiesInfo = dict()
  signalsSubscriptions = dict()
  for aSS in activeStrategySubscriptions:
    sName = db.get_strategy_by_id(aSS[1])[0][1]
    strategiesInfo[sName] = datetime.datetime.fromtimestamp(aSS[4] + config.MONTHINSECONDS).date()
  for sig in signalsSubscriptionsDb:
    signalsSubscriptions[True] = datetime.datetime.fromtimestamp(sig[2] + config.MONTHINSECONDS).date()

  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForProfile(strategiesInfo, signalsSubscriptions), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def signals(bot, update):
  cryptoPaymentButton = [InlineKeyboardButton('Оплатить подписку криптовалютой. Стоимость - ' + str(config.SUBSCRIPTIONFORSIGNALSPRICE) + '₽', callback_data='buy-signals', url = Texts.generatePaymentButtonForSignals(update.message.chat_id, config.SUBSCRIPTIONFORSIGNALSPRICE))]
  cardPaymentButton = [InlineKeyboardButton('Оплатить картой. Стоимость - ' + str(config.SUBSCRIPTIONFORSIGNALSPRICE) + '₽', callback_data='buy-signals', url = Texts.generateCardPaymentButtonForSignals(update.message.chat_id, config.SUBSCRIPTIONFORSIGNALSPRICE))]
  keyboard = [cryptoPaymentButton, cardPaymentButton]
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForSignals(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=telegram.ParseMode.HTML)

def strategies(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForStrategies(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def stuff(bot, update):
  bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForSubscriptionForStuff(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def contacts(bot, update):
  keyboard = [[InlineKeyboardButton('Написать в службу поддержки', callback_data='email')]]
  bot.send_message(chat_id=update.message.chat_id, text="Отправьте свое обращение на адрес {0}.\n Или сделайте это прямо здесь, нажав на кнопку \"Написать в службу поддержки\"".format(config.EMAILTO), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=telegram.ParseMode.HTML)

# def email(bot, update):
#   bot.send_message(chat_id=update.callback_query.message.chat.id, text="LOL", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)


def strategy(bot, update):
  db = DBRepo()
  strategyItself = Strategy.fromDbObject(db.get_strategy_by_name(update.message.text)[0])
  cryptoPaymentButton = [InlineKeyboardButton('Оплатить криптовалютой. Стоимость - ' + str(strategyItself.price) + '₽', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generatePaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]
  cardPaymentButton = [InlineKeyboardButton('Оплатить картой. Стоимость - ' + str(strategyItself.price) + '₽', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generateCardPaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]
  keyboard = [cryptoPaymentButton, cardPaymentButton]
  bot.send_message(chat_id=update.message.chat_id, text=strategyItself.description, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=telegram.ParseMode.HTML)

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
  handlers.append(RegexHandler('Личный кабинет 🔐', profile))
  handlers.append(RegexHandler('Сигналы 💰', signals))
  handlers.append(RegexHandler('Стратегии 🏆', strategies))
  handlers.append(RegexHandler('Материалы 📂', stuff))
  handlers.append(RegexHandler('Служба поддержки 📞', contacts))
  handlers.append(RegexHandler('🔙Назад', backToMainMenu))
  handlers.append(get_addstrategy_conv_handler())
  handlers.append(get_support_conv_handler())
  handlers.append(get_publishsignal_conv_handler())
  handlers.append(get_publishstrategy_conv_handler())
  handlers.append(get_publishreply_conv_handler())
  handlers.append(get_publishforall_conv_handler())
  handlers.append(RegexHandler(strategyNamesRegex, strategy))
  handlers.append(CommandHandler('testpayment', paymentCheck))
  handlers.append(RegexHandler('Отменить обращение', cancelEmail))

  for handler in handlers:
  	dp.add_handler(handler)
  


