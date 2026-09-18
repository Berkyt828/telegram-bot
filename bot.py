import os
import json
import threading
import time
import requests
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
CHAT_ID = int(os.environ.get('CHAT_ID', '0'))
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

FLAG_FILE = '/tmp/notify_flag.txt'


def send(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": chat_id, "text": text})
    print(f"SEND to {chat_id}: {r.status_code} {r.text}", flush=True)
    return r.text


@app.route('/webhook', methods=['POST'])
def webhook():
    raw = request.stream.read()
    try:
        data = json.loads(raw.decode('utf-8'))
        if 'message' in data:
            msg = data['message']
            chat_id = msg['chat']['id']
            text = msg.get('text', '')
            name = msg['from'].get('first_name', 'друг')
            if text == '/start':
                send(chat_id, f'Привет, {name}! 👋')
            elif text == '/help':
                send(chat_id, 'Команды:\n/start — поздороваться\n/help — помощь')
            elif 'привет' in text.lower():
                send(chat_id, 'Привет! 😊')
            elif 'как дела' in text.lower():
                send(chat_id, 'Всё отлично! А у тебя?')
            elif text:
                send(chat_id, f'Ты написал: {text}')
    except Exception as e:
        print(f"WEBHOOK ERROR: {e}", flush=True)
    return 'ok', 200


@app.route('/notify')
def notify():
    # Отправляем сразу же, не через фоновый поток
    print(f"NOTIFY HIT, sending to {CHAT_ID}", flush=True)
    result = send(CHAT_ID, 'Кнопка на сайте нажата!')
    return {'ok': True, 'telegram_response': result}


@app.route('/')
def index():
    return 'Bot is running', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
