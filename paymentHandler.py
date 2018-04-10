import telegram
from telegram.ext import (CommandHandler,MessageHandler,RegexHandler,Filters)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
import logging
from dbrepo import DBRepo
import botconfig as config
from texts import Texts
from strategy import Strategy
import hashlib

TOKEN = config.TOKEN
bot = telegram.Bot(token=TOKEN)
reply_keyboard_main_menu = [['Стратегии 🏆'], ['Сигналы 💰'], ['Материалы 📂','Служба поддержки 📞'], ['Личный кабинет 🔐']]
logger = logging.getLogger('btcLogger')

def handlePayment(invoiceData):
  logger.info("handlePayment method, invoice data = {0}".format(invoiceData))
  status = invoiceData['invoice_status']
  amount = invoiceData['invoice_amount']
  invoiceForData = getInvoiceForData(invoiceData['order_id'])
  messageToSend = ""
  paymentIsValid = checkPaymentValidity(invoiceData)
  everythingIsFine = False
  rightAwayLinkText = ''
  if paymentIsValid:
    db = DBRepo()
    if status == 'paid':
      if strategyWasBought(invoiceForData):  
        strategyThatWasBought = Strategy.fromDbObject(db.get_strategy_by_id(invoiceForData['strategyId'])[0]) 
        amountHadToBePaid = strategyThatWasBought.price
        rightAwayLinkText = Texts.getRightAwayLinkText(strategyThatWasBought.name, strategyThatWasBought.rightAwayLink) 
        if int(float(amount)) >= int(float(amountHadToBePaid)):
          logger.info('Adding subscription to strategy')
          db.add_subscription_for_strategy(invoiceForData['chatId'], invoiceForData['strategyId'])
          messageToSend = Texts.getTextForSubscriptionForStrategy(strategyThatWasBought.name)
          everythingIsFine = True
        else:
          messageToSend = "Сумма оплаты меньше суммы заказа. Стоимость - {0}, оплачено - {1}. Обратитесь в службу поддержки.".format(amountHadToBePaid, amount)

      else: 
        if int(float(amount)) >= int(float(config.SUBSCRIPTIONFORSIGNALSPRICE)):
          logger.info('Adding subscription to signals'.format(status))
          db.add_subscription_for_signals(invoiceForData['chatId'])
          messageToSend = Texts.getTextForSubscriptionForSignals()
          everythingIsFine = True
        else:
          messageToSend = "Сумма оплаты меньше суммы заказа. Стоимость - {0}, оплачено - {1}. Обратитесь в службу поддержки.".format(config.SUBSCRIPTIONFORSIGNALSPRICE, amount)
      sendResultMessagesToUser(invoiceForData['chatId'], messageToSend, everythingIsFine, strategyWasBought(invoiceForData), rightAwayLinkText)

    elif status == 'cancelled' or status == 'mispaid':
      
      messageToSend = "Статус транзакции - {0}. Подписка не оформлена.".format(status)
      if strategyWasBought(invoiceForData): 
        db.delete_subscription_for_strategy(invoiceForData['chatId'], invoiceForData['strategyId'])       
      else:
        db.delete_subscription_for_signals(invoiceForData['chatId'])
      sendResultMessagesToUser(invoiceForData['chatId'], messageToSend, everythingIsFine, strategyWasBought(invoiceForData), rightAwayLinkText)
  else:
    messageToSend = "Оплата недействительна. Обратитесь в службу поддержки."
    logger.info("AAAAAAAAAAA invoiceForData['chatId'] = {0}".format(invoiceForData['chatId']))
    logger.info("BBBBBBBBBBB type of it = {0}".format(type(invoiceForData['chatId'])))

    bot.send_message(chat_id=invoiceForData['chatId'], text=messageToSend, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def checkPaymentValidity(i):
  stringToCheck = '{0}&{1}&{2}&{3}&{4}&{5}&{6}&{7}&{8}&{9}&{10}&{11}&{12}&{13}'.format(i['merchant_id'], i['invoice_id']
    , i['invoice_created'], i['invoice_expires'], i['invoice_amount'], i['invoice_currency'], i['invoice_status']
    , i['invoice_url'], i['order_id'], i['checkout_address'], i['checkout_amount'], i['checkout_currency'], i['date_time']
    , config.SECRET).encode('utf-8')
  logger.info('stringToCheck = {0}'.format(stringToCheck))
  paymentHash = hashlib.sha1(stringToCheck).hexdigest()
  logger.info('paymentHash = {0}'.format(paymentHash))
  return i['secret_hash'] == paymentHash

def getInvoiceForData(orderInfo):
  orderData = orderInfo.split('_')
  chatId = orderData[1]
  if len(orderData) == 4:
    return {'chatId': chatId, 'strategyId': orderData[3]}
  elif len(orderData) == 2:
    return {'chatId': chatId}

def strategyWasBought(invoiceForData):
  return len(invoiceForData) == 2

def handleCardPayment(invoiceData):
  logger.info("handleCardPayment method, invoice data = {0}".format(invoiceData))
  logger.info('invoiceDataCARD = {0}'.format(invoiceData))
  amount = invoiceData['withdraw_amount']
  logger.info('amountCARD = {0}'.format(invoiceData))
  invoiceForData = getInvoiceForData(invoiceData['label'])
  logger.info('invoiceForDataCARD = {0}'.format(invoiceForData))
  messageToSend = ""
  paymentIsValid = checkCardPaymentValidity(invoiceData)
  everythingIsFine = False
  rightAwayLinkText = ''

  if paymentIsValid:
    db = DBRepo()
    if strategyWasBought(invoiceForData):  
      strategyThatWasBought = Strategy.fromDbObject(db.get_strategy_by_id(invoiceForData['strategyId'])[0]) 
      rightAwayLinkText = Texts.getRightAwayLinkText(strategyThatWasBought.name, strategyThatWasBought.rightAwayLink) 
      amountHadToBePaid = strategyThatWasBought.price
      if int(float(amount)) >= int(float(amountHadToBePaid)):
        logger.info('Adding subscription to strategy')
        db.add_subscription_for_strategy(invoiceForData['chatId'], invoiceForData['strategyId'])
        messageToSend = Texts.getTextForSubscriptionForStrategy(strategyThatWasBought.name)
        everythingIsFine = True
        logger.info('everythingIsFine = {0}'.format(everythingIsFine))
      else:
        messageToSend = "Сумма оплаты меньше суммы заказа. Стоимость - {0}, оплачено - {1}. Обратитесь в службу поддержки.".format(amountHadToBePaid, amount)

    else: 
      if int(float(amount)) >= int(float(config.SUBSCRIPTIONFORSIGNALSPRICE)):
        db.add_subscription_for_signals(invoiceForData['chatId'])
        messageToSend = Texts.getTextForSubscriptionForSignals()
        logger.info('everythingIsFine2 = {0}'.format(everythingIsFine))
        everythingIsFine = True

      else:
        messageToSend = "Сумма оплаты меньше суммы заказа. Стоимость - {0}, оплачено - {1}. Обратитесь в службу поддержки.".format(config.SUBSCRIPTIONFORSIGNALSPRICE, amount)
    sendResultMessagesToUser(invoiceForData['chatId'], messageToSend, everythingIsFine, strategyWasBought(invoiceForData), rightAwayLinkText)

  else:
    messageToSend = "Оплата недействительна. Обратитесь в службу поддержки."
    bot.send_message(chat_id=invoiceForData['chatId'], text=messageToSend, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def checkCardPaymentValidity(i):
  stringToCheck = '{0}&{1}&{2}&{3}&{4}&{5}&{6}&{7}&{8}'.format(i['notification_type'], i['operation_id']
    , i['amount'], i['currency'], i['datetime'], i['sender'], i['codepro']
    , config.YSECRET, i['label']).encode('utf-8')
  paymentHash = hashlib.sha1(stringToCheck).hexdigest()
  logger.info('AAAAAAAAAAA i["sha1_hash"]  = {0}'.format(i['sha1_hash'] ))
  logger.info('BBBBBBBBBBB paymentHash = {0}'.format(paymentHash))

  if(i['sha1_hash'] == paymentHash and i['codepro'] != 'false'):
    return i['sha1_hash'] == paymentHash

def sendResultMessagesToUser(chatId, message, everythingIsFine, strategyWasBought, rightAwayLinkText):
  bot.send_message(chat_id=chatId, text=message, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  if(everythingIsFine):
    if(strategyWasBought):
      bot.send_message(chat_id=chatId, text=rightAwayLinkText, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML) 
    bot.send_message(chat_id=chatId, text=Texts.getFirstLinkText(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
    if(strategyWasBought):
      bot.send_message(chat_id=chatId, text=Texts.getStrategyInstructionText(), reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)


