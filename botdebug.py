import botconfig as config
import telegram
from handlers import setHandlers
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


TOKEN = config.TOKEN
bot = telegram.Bot(token=TOKEN)
updater = telegram.ext.Updater(token=TOKEN)
dp = updater.dispatcher
setHandlers(dp)
updater.start_polling()