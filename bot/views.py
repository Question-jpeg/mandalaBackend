
from telebot import TeleBot, types
from django.conf import settings
from django.http import HttpResponse
from bot.utils import is_valid_date
from bot.logic.getImage import get_image
from bot.config.pages import INSTRUCTION_PAGE_1, INSTRUCTION_PAGE_2, Page, START_PAGE, LINKS

bot = TeleBot(settings.BOT_TOKEN)

def index(request):
    if request.method == "POST":
        update = types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')

def send_page(page: Page, message: types.Message):
    chat_id = message.chat.id

    if page.photo_file_id:
        bot.send_photo(chat_id, page.photo_file_id, page.get_text(message), 'html', reply_markup=page.reply_markup)
    else:
        bot.send_message(chat_id, page.get_text(message), 'html', reply_markup=page.reply_markup)

def edit_page(page: Page, message: types.Message):
    chat_id = message.chat.id

    if page.photo_file_id:
        bot.edit_message_media(types.InputMediaPhoto(page.photo_file_id, page.get_text(message), 'html'), chat_id, message.id, reply_markup=page.reply_markup)
    else:
        bot.edit_message_text(page.get_text(message), chat_id, message.id, reply_markup=page.reply_markup)


@bot.message_handler(commands=['getFileID'])
def get_file_id(message: types.Message):
    bot.send_message(message.chat.id, message.reply_to_message.photo[0].file_id)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    send_page(START_PAGE, message)

@bot.message_handler(commands=['instruction'])
def instruction(message: types.Message):
    send_page(INSTRUCTION_PAGE_1, message)    
    

@bot.callback_query_handler(lambda q: True)
def handle_callback(query: types.CallbackQuery):
    link = query.data
    message = query.message

    edit_page(LINKS[link], message)


# @bot.message_handler()
# def mandala(message: types.Message):
#     chat_id = message.chat.id
#     dateString = message.text

#     validator = r'^\d\d[.]\d\d[.]\d\d\d\d$'
#     is_match = bool(re.fullmatch(validator, dateString))
#     is_valid = False

#     if is_match:
#         day, month, year = [int(v) for v in dateString.split('.')]
#         is_valid = is_valid_date(day, month, year)

#     if is_valid:
#         imageData = get_image(dateString)
#         bot.send_photo(chat_id, imageData['image'], imageData['text'])
#     else:
#         bot.send_message(chat_id, DATE_ERROR)