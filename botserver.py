from flask import Flask,request
import botconfig as config
import telegram
from handlers import setHandlers
import sys
from paymentHandler import handlePayment, handleCardPayment
from werkzeug.datastructures import ImmutableMultiDict
import logging
import logging.handlers

def setUpLoggers():
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  logger = logging.getLogger('btcLogger')
  logger.setLevel(logging.DEBUG)
  fh = logging.handlers.TimedRotatingFileHandler(filename = config.LOGPATH, when='d', interval=7, backupCount=3)
  fh.setLevel(logging.DEBUG)
  fh.setFormatter(formatter)
  logger.addHandler(fh)  

TOKEN = config.TOKEN
HOST = config.HOST
CERT = "/etc/letsencrypt/live/chaispechenkoi.club/fullchain.pem"
CERT_KEY = "/etc/letsencrypt/live/chaispechenkoi.club/privkey.pem"
PORT = 443
context = (CERT, CERT_KEY)

bot = telegram.Bot(TOKEN)
dp = telegram.ext.Dispatcher(bot, None)
setHandlers(dp)
setUpLoggers()
logger = logging.getLogger('btcLogger')

app = Flask(__name__)
 
@app.errorhandler(Exception)
def handle_error(e):
  logger.error("Error itself = \n {0}".format(e).encode('utf-8'))

@app.route("/", methods=["POST", "GET"])
def webhook():
  try:
    update = telegram.update.Update.de_json(request.get_json(force=True),bot)
    dp.process_update(update)
  except Exception as e:
    logger.error("An error occured handling webhook when request was - \n {0}".format(request.get_json(force=True)))  
    logger.exception(e)
  finally:
    return ''

@app.route('/invoice', methods=["POST", "GET"])
def invoice():
  try:
    invoice = request.form.to_dict(flat=True)
    handlePayment(invoice)
    logger.info('----Invoice-----', request.form)
  except Exception as e:
    logger.error("An error occured handling invoice when request was - \n {0}".format(request.form))  
    logger.exception(e)
  finally:
    return ''

@app.route('/cardInvoice', methods=["POST", "GET"])
def cardInvoice():
  try:
    invoice = request.form.to_dict(flat=True)
    handleCardPayment(invoice)
    logger.info('----Card Invoice-----', request.form)
  except Exception as e:
    logger.error("An error occured handling card invoice when request was - \n {0}".format(request.form))  
    logger.exception(e)
  finally:
    return ''

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT, ssl_context=context)