import botconfig as config
import telegram
from handlers import setHandlers
import logging
import logging.handlers


def main():
  setUpLoggers()
  TOKEN = config.TOKEN
  bot = telegram.Bot(token=TOKEN)
  updater = telegram.ext.Updater(token=TOKEN)
  dp = updater.dispatcher
  setHandlers(dp)
  updater.start_polling()

def setUpLoggers():
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  logger = logging.getLogger('btcLogger')
  logger.setLevel(logging.INFO)
  fh = logging.handlers.TimedRotatingFileHandler(filename = config.LOGPATH, when='d', interval=7, backupCount=3)
  fh.setLevel(logging.INFO)
  fh.setFormatter(formatter)
  logger.addHandler(fh)  

if __name__ == '__main__':
    main()