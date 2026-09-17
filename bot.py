import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f'Привет, {message.from_user.first_name}! 👋')

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, 'Команды:\n/start — поздороваться\n/help — помощь')

@bot.message_handler(func=lambda m: True)
def echo(message):
    text = message.text.lower()
    if 'привет' in text:
        bot.reply_to(message, 'Привет! 😊')
    elif 'как дела' in text:
        bot.reply_to(message, 'Всё отлично! А у тебя?')
    else:
        bot.reply_to(message, f'Ты написал: {message.text}')

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return 'Bot is running', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))import