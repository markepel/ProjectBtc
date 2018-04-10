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
from paymentHandler import handlePayment,handleCardPayment
from werkzeug.datastructures import ImmutableMultiDict
import datetime
from publishStrategyConvHandler import get_publishstrategy_conv_handler
from publishSignalConvHandler import get_publishsignal_conv_handler
from publishSupportReplyConvHandler import get_publishreply_conv_handler
from publishForAllConvHandler import get_publishforall_conv_handler
import smtplib
from email.message import EmailMessage


db = DBRepo()
db.setup()
handlers = []
reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
reply_keyboard_strategies = Menus.generateStrategiesMenu()
reply_support_menu = [['Отправить 📮'],['🔙Назад']]
strategyNamesRegex = Texts.generateRegexForStrategies(db.get_all_strategies_names())
goBackTo = 'start'
logger = logging.getLogger('btcLogger')


def start(bot, update):
  try:
    logger.info('New START!!!, new chat_id = {0}, from_user.id {1}'.format(update.message.chat_id, update.message.from_user.id))
    bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextOnStart(update.message.from_user.first_name), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    db = DBRepo()
    db.add_user(update.message.from_user.id, update.message.from_user.first_name)  
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

# def cancelEmail(bot, update):
#   bot.send_message(chat_id=update.message.chat_id, text="Обращение отменено.", reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def profile(bot, update):
  try:
    logger.info('Getting profile for chat_id = {0}'.format(update.message.chat_id))
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
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

def signals(bot, update):
  # cryptoPaymentButton = [InlineKeyboardButton('Оплатить подписку криптовалютой. Стоимость - ' + str(config.SUBSCRIPTIONFORSIGNALSPRICE) + '₽', callback_data='buy-signals', url = Texts.generatePaymentButtonForSignals(update.message.chat_id, config.SUBSCRIPTIONFORSIGNALSPRICE))]
  # cardPaymentButton = [InlineKeyboardButton('Оплатить картой. Стоимость - ' + str(config.SUBSCRIPTIONFORSIGNALSPRICE) + '₽', callback_data='buy-signals', url = Texts.generateCardPaymentButtonForSignals(update.message.chat_id, config.SUBSCRIPTIONFORSIGNALSPRICE))]
  try:
    cryptoPaymentButton = [InlineKeyboardButton('Оплатить криптовалютой', callback_data='buy-signals', url = Texts.generatePaymentButtonForSignals(update.message.chat_id, config.SUBSCRIPTIONFORSIGNALSPRICE))]
    cardPaymentButton = [InlineKeyboardButton('Оплатить картой', callback_data='buy-signals', url = Texts.generateCardPaymentButtonForSignals(update.message.chat_id, config.SUBSCRIPTIONFORSIGNALSPRICE))]
    keyboard = [cryptoPaymentButton, cardPaymentButton]
    bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForSignals(), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=telegram.ParseMode.HTML)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

def strategies(bot, update):
  try:
    bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForStrategies(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_strategies, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

def stuff(bot, update):
  try:
    bot.send_message(chat_id=update.message.chat_id, text=Texts.getTextForSubscriptionForStuff(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

# def contacts(bot, update):
#   try:
#     keyboard = [[InlineKeyboardButton('Написать в службу поддержки', callback_data='email')]]
#     bot.send_message(chat_id=update.message.chat_id, text="Отправьте свое обращение на адрес {0} или сделайте это здесь и сейчас, нажав на кнопку \"Написать в службу поддержки\"".format(config.EMAILTO), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=telegram.ParseMode.HTML)
#   except Exception as e:
#     logger.exception(e)
#     bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

def contacts(bot, update):
  try:
    keyboard = [[InlineKeyboardButton('Написать в службу поддержки', callback_data='email')]]
    bot.send_message(chat_id=update.message.chat_id, text="Отправьте свое обращение на адрес {0}.\n Или сделайте это здесь и сейчас. Если вы хотите получить ответ не в боте, а по email, укажите его адрес в своем сообщении, пожалуйста.".format(config.EMAILTO), reply_markup=ReplyKeyboardMarkup(reply_support_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

def strategy(bot, update):
  try:
    db = DBRepo()
    strategyItself = Strategy.fromDbObject(db.get_strategy_by_name(update.message.text)[0])
    # cryptoPaymentButton = [InlineKeyboardButton('Оплатить криптовалютой. Стоимость - ' + str(strategyItself.price) + '₽', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generatePaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]
    # cardPaymentButton = [InlineKeyboardButton('Оплатить картой. Стоимость - ' + str(strategyItself.price) + '₽', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generateCardPaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]
    cryptoPaymentButton = [InlineKeyboardButton('Оплатить криптовалютой', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generatePaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]
    cardPaymentButton = [InlineKeyboardButton('Оплатить картой', callback_data='buy-s_name=' + strategyItself.name, url = Texts.generateCardPaymentButtonForStrategy(strategyItself.id, strategyItself.name, update.message.chat_id, strategyItself.price))]
    
    keyboard = [cryptoPaymentButton, cardPaymentButton]
    bot.send_message(chat_id=update.message.chat_id, text=strategyItself.description, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=telegram.ParseMode.HTML)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))

def paymentCheck(bot, update):
  inputInvoiceData = ImmutableMultiDict([
('invoice_status', 'paid'), 
('invoice_expires', '1522430055'), 
('invoice_currency', 'rur'), 
('checkout_address', '1N3mEGtDfLErX3G5RD3RYxN4E5gffW7dGj'), 
('invoice_id', '627658cd455e8392cad690bedc4d2aa3'), 
('secret_hash', 'c9a25b9950e9151a19a91e6f381270d092419365'), 
('checkout_amount', '0.0008'), 
('invoice_created', '1522428255'), 
('invoice_url', 'https://ru.cryptonator.com/merchant/invoice/627658cd455e8392cad690bedc4d2aa3'), ('date_time', '1522428264'), 
('order_id', 'cid_301854836_stid_2'),
('checkout_currency', 'bitcoin'), 
('invoice_amount', '300'), 
('merchant_id', '0ec794355b4f304b47e4052259388e69')])

  fakeInvoice = inputInvoiceData.to_dict(flat=True)
  handlePayment(fakeInvoice)

def cardPaymentCheck(bot, update):
  inputInvoiceData = ImmutableMultiDict([
    ('building', ''), 
    ('suite', ''), 
    ('flat', ''), 
    ('unaccepted', 'false'), 
    ('fathersname', ''), 
    ('lastname', ''), 
    ('sender', ''), 
    ('zip', ''), 
    ('phone', ''), 
    ('firstname', ''), 
    ('notification_type', 'card-incoming'), 
    ('operation_id', '576692812779008012'), 
    ('sha1_hash', '6ace7f01cc6786a4d9b8ef457705373fcc701cd5'), 
    ('street', ''), 
    ('label', 'cid_209017109'), 
    ('withdraw_amount', '4500.00'), 
    ('codepro', 'false'), 
    ('datetime', '2018-04-10T16:26:52Z'), 
    ('currency', '643'), 
    ('email', ''), 
    ('operation_label', '225ef96f-0002-5000-8036-1f09d186e844'), 
    ('amount', '4410.00'), 
    ('city', '')
    ])

  fakeInvoice = inputInvoiceData.to_dict(flat=True)
  handleCardPayment(fakeInvoice)

def backToMainMenu(bot, update):
  try:
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(goBackTo)
    method(bot, update)
  except Exception as e:
    logger.exception(e)
    bot.send_message(chat_id=update.message.chat_id, text="", reply_markup = ReplyKeyboardMarkup(reply_keyboard_main_menu))


def setHandlers(dp):
  handlers.append(CommandHandler('start', start))
  handlers.append(RegexHandler('Личный кабинет 🔐', profile))
  handlers.append(RegexHandler('Сигналы 💰', signals))
  handlers.append(RegexHandler('Стратегии 🏆', strategies))
  handlers.append(RegexHandler('Материалы 📂', stuff))
  #handlers.append(RegexHandler('Служба поддержки 📞', contacts))
  handlers.append(RegexHandler('🔙Назад', backToMainMenu))
  handlers.append(get_addstrategy_conv_handler())
  handlers.append(get_support_conv_handler())
  handlers.append(get_publishsignal_conv_handler())
  handlers.append(get_publishstrategy_conv_handler())
  handlers.append(get_publishreply_conv_handler())
  handlers.append(get_publishforall_conv_handler())
  handlers.append(RegexHandler(strategyNamesRegex, strategy))
  handlers.append(CommandHandler('testpayment', paymentCheck))
  handlers.append(CommandHandler('testcardpayment', cardPaymentCheck))
  #handlers.append(RegexHandler('Отменить обращение', cancelEmail))

  for handler in handlers:
  	dp.add_handler(handler)
  


