from telebot import types, util

class Page:

    reply_markup = None

    def __init__(self, link, text, photo_file_id = None) -> None:
        self.link = link
        self.photo_file_id = photo_file_id
        self.text = text

    def get_text(self, message):
        if isinstance(self.text, str):
            return self.text
        
        return self.text(message)

    def set_reply_markup(self, reply_markup):
        self.reply_markup = util.quick_markup(reply_markup)

def GREETINGS(message: types.Message):
    return f'Привет {message.from_user.full_name}! Введи свою дату рождения без разделительных знаков, чтобы получить мандалу! Пример даты: 28042004'

START_PAGE = Page(link='start', text=GREETINGS)

INSTRUCTION_PAGE_1 = Page(
    link='inst_page_1', 
    text= 
"""
1⃣ Запишите свою дату рождения, например, 26.03.1969 в виде 26031969.

2⃣ Зеркально отразите и допишите этот ряд цифр в конце исходного. В нашем примере получится следующее: 
26031969 96913062 
(должно быть 16 знаков).

3⃣ Для удобства цифры можно разделить пробелами:                
2 6 0 3 1 9 6 9 9 6 9 1 3 0 6 2.
Впоследствии это также позволит сделать более наглядным наш цифровой треугольник.

4⃣ Далее поочередно сложите все цифры между собой. Результат записывайте снизу под точками (между слагаемыми). Если при сложении получилось двузначное число, последовательно доведите его до однозначного. Например, 6+9=15 (еще раз складываем составляющие число цифры) 1+5=6.

5⃣ Итого во второй строчке получилось:
8 6 3 4 1 6 6 9 6 6 1 4 3 6 8.
Записываем и продолжаем расчеты.
""",
    photo_file_id='AgACAgIAAxkBAAP8ZMpH3a_wzgGK0PVP_WQIJ9b3NnsAAojOMRsmHlFK5RWLr13wyvQBAAMCAANzAAMvBA'
)

INSTRUCTION_PAGE_2 = Page(
    link='inst_page_2',
    text='Результат заполнения',
    photo_file_id='AgACAgIAAxkBAAPsZMlV_8rCsTwlOTv2g5GMjppF3qwAAn7SMRsi-EhKROw5vmEK1kQBAAMCAANzAAMvBA'
)

INSTRUCTION_PAGE_3 = Page(
    link='inst_page_3',
    text='Распечатайте шаблон мандалы для последующей раскраски',
)

INSTRUCTION_PAGE_1.set_reply_markup({'Далее': {'callback_data': INSTRUCTION_PAGE_2.link}})
INSTRUCTION_PAGE_2.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_1.link}, 'Далее': {'callback_data': INSTRUCTION_PAGE_3.link}})
INSTRUCTION_PAGE_3.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_2.link}})

LINKS = {
    START_PAGE.link: START_PAGE,
    INSTRUCTION_PAGE_1.link: INSTRUCTION_PAGE_1,
    INSTRUCTION_PAGE_2.link: INSTRUCTION_PAGE_2,
    INSTRUCTION_PAGE_3.link: INSTRUCTION_PAGE_3
}