import re
from telebot import TeleBot, types
from django.conf import settings
from django.http import HttpResponse
from bot.utils import is_valid_date
from bot.logic.getImage import get_image
from bot.config.pages import (
    LINKS,
    START_PAGE,
    EXAMPLES_PAGE,
    INSTRUCTION_PAGE_1,
    BUY_PAGE,
    Page,
    PageTypes,
)
import bot.config.botMessages as BOT_MESSAGES

bot = TeleBot(settings.BOT_TOKEN)


def index(request):
    if request.method == "POST":
        update = types.Update.de_json(request.body.decode("utf-8"))
        bot.process_new_updates([update])

    return HttpResponse("<h1>Ты подключился!</h1>")


def send_page(page: Page, message: types.Message):
    chat_id = message.chat.id

    if page.type == PageTypes.PHOTO:
        bot.send_photo(
            chat_id,
            page.photo_file_id,
            page.get_text(message),
            "html",
            reply_markup=page.reply_markup,
        )
    elif page.type == PageTypes.MEDIA_GROUP:
        bot.send_media_group(
            chat_id,
            [
                types.InputMediaPhoto(
                    page.photo_file_ids[i],
                    page.get_text(message) if i == 0 else None,
                    parse_mode="html",
                )
                for i in range(len(page.photo_file_ids))
            ],
        )
    elif page.type == PageTypes.INVOICE:
        bot.send_invoice(
            chat_id=chat_id,
            title=page.title,
            description=page.get_text(message),
            invoice_payload="invoice",
            provider_token=settings.PAYMENT_PROVIDER_TOKEN,
            currency="RUB",
            prices=[page.price],

        )
    else:
        bot.send_message(
            chat_id, page.get_text(message), "html", reply_markup=page.reply_markup
        )


def handle_callback_page(page: Page, message: types.Message):
    chat_id = message.chat.id

    if page.type == PageTypes.PHOTO:
        bot.edit_message_media(
            types.InputMediaPhoto(page.photo_file_id, page.get_text(message), "html"),
            chat_id,
            message.id,
            reply_markup=page.reply_markup,
        )
    elif page.type == PageTypes.TEXT:
        bot.edit_message_text(
            page.get_text(message), chat_id, message.id, reply_markup=page.reply_markup
        )
    else:
        send_page(page, message)


@bot.callback_query_handler(lambda q: True)
def handle_callback(query: types.CallbackQuery):
    link = query.data
    message = query.message

    handle_callback_page(LINKS[link], message)

@bot.message_handler(commands=["getFileID"])
def get_file_id(message: types.Message):
    bot.send_message(message.chat.id, message.reply_to_message.photo[0].file_id)


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    send_page(START_PAGE, message)


@bot.message_handler(commands=["examples"])
def examples(message: types.Message):
    send_page(EXAMPLES_PAGE, message)


@bot.message_handler(commands=["instruction"])
def instruction(message: types.Message):
    send_page(INSTRUCTION_PAGE_1, message)


@bot.message_handler(commands=["buy"])
def buy(message: types.Message):
    send_page(BUY_PAGE, message)

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Возникла проблема, попробуйте позднее")                                  

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message: types.Message):
    sent = bot.send_message(message.chat.id, BOT_MESSAGES.SUCCESSFUL_PAYMENT)
    bot.register_next_step_handler(sent, mandala)


def mandala(message: types.Message):
    chat_id = message.chat.id
    dateString = message.text

    validator = r"^\d\d\d\d\d\d\d\d$"
    is_match = bool(re.fullmatch(validator, dateString))
    is_valid = False

    if is_match:
        day = int(dateString[:2])
        month = int(dateString[2:4])
        year = int(dateString[4:])
        is_valid = is_valid_date(day, month, year)

    if is_valid:
        imageData = get_image(dateString)
        bot.send_photo(chat_id, imageData["image"])
    else:
        sent = bot.send_message(chat_id, BOT_MESSAGES.DATE_ERROR)
        bot.register_next_step_handler(sent, mandala)


@bot.message_handler()
def handle_none(message: types.Message):
    bot.send_message(message.chat.id, BOT_MESSAGES.HELP)