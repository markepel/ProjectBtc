from flask import Flask,request
import botconfig as config
import telegram
from handlers import setHandlers
import sys
from paymentHandler import handlePayment,hadleCardPayment
from werkzeug.datastructures import ImmutableMultiDict
import logging

TOKEN = config.TOKEN
HOST = config.HOST
CERT = "/etc/letsencrypt/live/chaispechenkoi.club/fullchain.pem"
CERT_KEY = "/etc/letsencrypt/live/chaispechenkoi.club/privkey.pem"
PORT = 443
context = (CERT, CERT_KEY)

bot = telegram.Bot(TOKEN)
dp = telegram.ext.Dispatcher(bot, None)
setHandlers(dp)

app = Flask(__name__)
 
@app.route("/", methods=["POST", "GET"])
def webhook():
  update = telegram.update.Update.de_json(request.get_json(force=True),bot)
  dp.process_update(update)
  return ''

@app.route('/invoice', methods=["POST", "GET"])
def invoice():
  try:
    invoice = request.form.to_dict(flat=True)
    handlePayment(invoice)
    print('----Invoice-----', request.form)
    return ''
  except Exception as e:
    print('----Invoice-----', request.form)

@app.route('/cardInvoice', methods=["POST", "GET"])
def cardInvoice():
  try:
    invoice = request.form.to_dict(flat=True)
    hadleCardPayment(invoice)
    print('----Card Invoice-----', request.form)
    return ''
  except Exception as e:
    print('----Invoice-----', request.form)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT, ssl_context=context)