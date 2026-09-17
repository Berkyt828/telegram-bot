import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
print(f"BOT_TOKEN loaded: {BOT_TOKEN[:10]}...", flush=True)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    print(f"Got /start from {message.chat.id}", flush=True)
    bot.reply_to(message, f'Привет, {message.from_user.first_name}! 👋')


@bot.message_handler(commands=['help'])
def help_cmd(message):
    print(f"Got /help", flush=True)
    bot.reply_to(message, 'Команды:\n/start — поздороваться\n/help — помощь')


@bot.message_handler(func=lambda m: True)
def echo(message):
    print(f"Got message: {message.text}", flush=True)
    text = message.text.lower()
    if 'привет' in text:
        bot.reply_to(message, 'Привет! 😊')
    elif 'как дела' in text:
        bot.reply_to(message, 'Всё отлично! А у тебя?')
    else:
        bot.reply_to(message, f'Ты написал: {message.text}')


@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    print(f"Webhook hit! Data: {request.data[:200]}", flush=True)
    try:
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        print(f"Update parsed: {update}", flush=True)
        bot.process_new_updates([update])
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
    return 'ok', 200


@app.route('/')
def index():
    return 'Bot is running', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
