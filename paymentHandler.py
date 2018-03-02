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
reply_keyboard_main_menu = [['Стратегии'], ['Сигналы'], ['Материалы','Служба поддержки'], ['Личный кабинет']]


def handlePayment(invoiceData):
  print('invoiceData = {0}'.format(invoiceData))
  status = invoiceData['invoice_status']
  print('status = {0}'.format(status))
  amount = invoiceData['invoice_amount']
  print('amount = {0}'.format(amount))
  invoiceForData = getInvoiceForData(invoiceData['order_id'])
  #invoiceForData = {'chatId': 111384340, 'strategyId': 7}
  print('invoiceForData = {0}'.format(invoiceForData))
  messageToSend = ""
  paymentIsValid = checkPaymentValidity(invoiceData)

  if paymentIsValid:
    db = DBRepo()
    if status == 'paid':

      if strategyWasBought(invoiceForData):  

        strategyThatWasBought = Strategy.fromDbObject(db.get_strategy_by_id(invoiceForData['strategyId'])[0]) 
        amountHadToBePaid = strategyThatWasBought.price
        if int(float(amount)) >= int(float(amountHadToBePaid)):
          print('Adding subscription to strategy')
          db.add_subscription_for_strategy(invoiceForData['chatId'], invoiceForData['strategyId'])
          messageToSend = Texts.getTextForSubscriptionForStrategy(strategyThatWasBought.name)
        else:
          messageToSend = "Сумма оплаты меньше суммы заказа. Стоимость - {0}, оплачено - {1}. Обратитесь в службу поддержки.".format(amountHadToBePaid, amount)

      else: 

        if int(float(amount)) >= int(float(config.SUBSCRIPTIONFORSIGNALSPRICE)):
          print('Adding subscription to signals'.format(status))
          db.add_subscription_for_signals(invoiceForData['chatId'])
          messageToSend = Texts.getTextForSubscriptionForSignals()
        else:
          messageToSend = "Сумма оплаты меньше суммы заказа. Стоимость - {0}, оплачено - {1}. Обратитесь в службу поддержки.".format(config.SUBSCRIPTIONFORSIGNALSPRICE, amount)

    elif status == 'cancelled' or status == 'mispaid':
      
      messageToSend = "Статус транзакции - {0}. Подписка не оформлена.".format(status)
      if strategyWasBought(invoiceForData): 
        db.delete_subscription_for_strategy(invoiceForData['chatId'], invoiceForData['strategyId'])       
      else:
        db.delete_subscription_for_signals(invoiceForData['chatId'])
    bot.send_message(chat_id=invoiceForData['chatId'], text=messageToSend, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)
  else:
    messageToSend = "Оплата недействительна. Обратитесь в службу поддержки."
    bot.send_message(chat_id=invoiceForData['chatId'], text=messageToSend, reply_markup=ReplyKeyboardMarkup(reply_keyboard_main_menu, one_time_keyboard=True), parse_mode=telegram.ParseMode.HTML)

def checkPaymentValidity(i):
  stringToCheck = '{0}&{1}&{2}&{3}&{4}&{5}&{6}&{7}&{8}&{9}&{10}&{11}&{12}&{13}'.format(i['merchant_id'], i['invoice_id']
    , i['invoice_created'], i['invoice_expires'], i['invoice_amount'], i['invoice_currency'], i['invoice_status']
    , i['invoice_url'], i['order_id'], i['checkout_address'], i['checkout_amount'], i['checkout_currency'], i['date_time']
    , config.SECRET).encode('utf-8')
  print('stringToCheck = {0}'.format(stringToCheck))
  paymentHash = hashlib.sha1(stringToCheck).hexdigest()
  print('paymentHash = {0}'.format(paymentHash))
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