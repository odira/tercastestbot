import telebot
import os
from flask import Flask, request

#from telebot import apihelper
#PROXY = 'socks5://208.97.31.229:53124'
#apihelper.proxy = {'https': PROXY}

# BOT
#TOKEN = '1113430903:AAHokCKvymVRH1aM9nmNViZLNeIlE20VrW0'  # TercasTestBot token
TOKEN = '1200961315:AAG-p5ZFEesMzcFoq20834iJ82sKfWCUqNQ' # TercasBot token

bot = telebot.TeleBot(TOKEN)

HEROKU_WEB_URL = 'https://serene-everglades-02368.herokuapp.com/'


server = Flask(__name__)

# SERVER SIDE
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def wibhook():
    bot.remove_webhook()
    bot.set_webhook(url=HEROKU_WEB_URL + TOKEN)
    return "!", 200


keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Привет', 'Пока')


def sendMessage(message, text):
    bot.send_message(message.chat.id, str(text))


@bot.message_handler(commands=['start'])
def send_info(message):
    text = ("<b>Welcome to the Medium 🤖!</b>\n"
            "Say Hello to the bot to get a reply from it!")
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard1)

@bot.message_handler(func=lambda msg: msg.text is not None)
def reply_to_message(message):
    if 'hello' in message.text.lower():
        sendMessage(message, 'Hello! How are you doing today?')
    elif 'привет' in message.text.lower():
        sendMessage(message, 'Привет друг')

@bot.message_handler(content_types=['text'])
def send_text(message):

    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель!')

    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель!')

    elif message.text.lower() == 'abc':
        sticker_id = 'CAACAgIAAxkBAAMdXqWECAGYEbwtl7xgM9tT3jf8u4wAAgYAA9_KShIkA-AxY0DBnhkE'
        bot.send_sticker(message.chat.id, sticker_id)


@bot.message_handler(content_types=['sticker'])
def send_text(message):
    bot.send_message(message.chat.id, message.chat.username)


#if __name__ == "__main__":
#    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except(BaseException):
            pass
