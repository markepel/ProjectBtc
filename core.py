import json
import requests
import threading

TOKEN = "498994079:AAExPGmBBKu3I7wKjfDu94pWJ-mTJ5LmFRI"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    if num_updates > 0 :
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def allTogether():
    print("Enter allTogether part")
    threading.Timer(5.0, allTogether).start()
    text, chat = get_last_chat_id_and_text(get_updates())
    if chat:
        send_message(text, chat)

def new():
    return ''

def handleUpdate(update):
    chat_id = update["message"]["chat"]["id"]
    send_message(update, chat_id)
