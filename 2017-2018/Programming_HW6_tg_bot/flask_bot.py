from random import choice
import telebot
import flask
import HW_BOT_just_console as bot_words
import conf


WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
STICKERS = []


bot = telebot.TeleBot(conf.TOKEN)
bot.remove_webhook()
# bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)
app = flask.Flask(__name__)


@bot.message_handler(commands=['start', 'help'])
def info(message):
    user = message.chat.id
    bot.send_message(user, 'Привет! Этот бот абсолютно бесполезен, но можешь что-нибудь ему написать.')


@bot.message_handler(content_types=['text'])
def message_len(message):
    text = message.text
    user = message.chat.id
    new_text = bot_words.main(text)
    bot.send_message(user, new_text)


@bot.message_handler(content_types=['sticker'])
def answer_stickers(message):
    user = message.chat.id
    bot.send_message(user, "Классный стикер!")
    STICKERS.append(message.sticker.file_id)
    bot.send_sticker(user, choice(STICKERS))


if __name__ == '__main__':
    bot.polling(none_stop=True)
