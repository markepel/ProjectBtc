import json
import requests
import threading
import botconfig as config
import logging
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

TOKEN = config.TOKEN
SVRURL = config.SVRURL
print("JUST PRINT")

