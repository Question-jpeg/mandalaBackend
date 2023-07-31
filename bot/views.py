
from telebot import TeleBot, types
from django.conf import settings
from django.http import HttpResponse
from bot import replyMessages
import re
from bot.utils import is_valid_date
from bot.getImage import get_image
from bot.replyMessages import DATE_ERROR

bot = TeleBot(settings.BOT_TOKEN)


def index(request):
    if request.method == "POST":
        update = types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    name = message.from_user.full_name
    bot.send_message(message.chat.id, replyMessages.GREETINGS(name))

@bot.message_handler()
def mandala(message: types.Message):
    chat_id = message.chat.id
    dateString = message.text

    validator = r'^\d\d[ ]\d\d[ ]\d\d\d\d$'
    is_match = bool(re.fullmatch(validator, dateString))
    is_valid = False

    if is_match:
        day, month, year = [int(v) for v in dateString.split(' ')]
        is_valid = is_valid_date(day, month, year)

    if is_valid:
        bot.send_photo(chat_id, get_image(dateString))
    else:
        bot.send_message(chat_id, DATE_ERROR)