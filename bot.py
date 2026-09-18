import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


def send(chat_id, text):
    """Отправляем сообщение через Telegram API напрямую."""
    import requests
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})


@app.route('/webhook', methods=['POST'])
def webhook():
    raw = request.stream.read()
    print(f"Webhook hit! Len: {len(raw)}", flush=True)
    try:
        data = __import__('json').loads(raw.decode('utf-8'))
        if 'message' in data:
            msg = data['message']
            chat_id = msg['chat']['id']
            text = msg.get('text', '')
            name = msg['from'].get('first_name', 'друг')
            print(f"Got message: {text} from {name}", flush=True)

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

            print(f"Reply sent to {chat_id}", flush=True)
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
    return 'ok', 200


@app.route('/')
def index():
    return 'Bot is running', 200


@app.route('/test-ping')
def test_ping():
    chat_id = int(os.environ.get('CHAT_ID'))
    try:
        bot.send_message(chat_id, "Пинг из Render через telebot")
        return {"ok": True, "method": "telebot"}
    except Exception as e:
        return {"ok": False, "error": str(e)}



@app.route('/show-config')
def show_config():
    return {
        'chat_id_in_env': os.environ.get('CHAT_ID'),
        'chat_id_len': len(os.environ.get('CHAT_ID', '')),
        'token_len': len(BOT_TOKEN)
    }





@app.route('/proxy-check')
def proxy_check():
    return {
        'http_proxy': os.environ.get('HTTP_PROXY'),
        'https_proxy': os.environ.get('HTTPS_PROXY'),
        'no_proxy': os.environ.get('NO_PROXY'),
    }




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
