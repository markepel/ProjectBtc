from flask import Flask,request
import botconfig as config
import telegram
from handlers import setHandlers

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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=PORT, ssl_context=context)