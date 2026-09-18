import os
import json
import requests
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

LAST_CHAT_FILE = '/tmp/last_chat.txt'


def send(chat_id, text):
    try:
        bot.send_message(chat_id, text)
        print(f"SEND OK to {chat_id}", flush=True)
        return "ok"
    except Exception as e:
        print(f"SEND ERR to {chat_id}: {e}", flush=True)
        return str(e)


@app.route('/webhook', methods=['POST'])
def webhook():
    raw = request.stream.read()
    try:
        data = json.loads(raw.decode('utf-8'))
        if 'message' in data:
            msg = data['message']
            chat_id = msg['chat']['id']

            with open(LAST_CHAT_FILE, 'w') as f:
                f.write(str(chat_id))

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
    try:
        with open(LAST_CHAT_FILE) as f:
            chat_id = int(f.read().strip())
    except Exception as e:
        return {'ok': False, 'error': f'no chat file: {e}'}

    print(f"NOTIFY: sending to {chat_id}", flush=True)
    result = send(chat_id, 'Кнопка на сайте нажата!')
    return {'ok': True, 'chat_id_used': chat_id, 'telegram_response': result}


@app.route('/')
def index():
    return 'Bot is running', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
