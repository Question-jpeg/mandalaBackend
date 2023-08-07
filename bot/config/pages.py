from telebot import types, util

class Page:

    reply_markup = None

    def __init__(self, link, text, photo_file_id = None, photo_file_ids = None) -> None:
        self.link = link
        self.photo_file_id = photo_file_id
        self.photo_file_ids = photo_file_ids
        self.text = text

    def get_text(self, message):
        if isinstance(self.text, str):
            return self.text
        
        return self.text(message)

    def set_reply_markup(self, reply_markup):
        self.reply_markup = util.quick_markup(reply_markup)

def GREETINGS(message: types.Message):
    return f"""
Здравствуйте, {message.from_user.full_name}!

В этом боте вы можете:

1⃣ Сделать свою мандалу по дате рождения самостоятельно

2⃣ Приобрести мандалу

3⃣ Посмотреть примеры готовых мандал

Для навигации используйте меню
"""

START_PAGE = Page(
    link='start', 
    text=GREETINGS,
    photo_file_id='AgACAgIAAxkDAAIBOmTMkRV9e6eYqnBfwolPOkLOrfMjAAJ0xzEbmbtBSpfb019kAAGBdAEAAwIAA3MAAy8E'
)

EXAMPLES_PAGE = Page(
    link='ex_page',
    text='Примеры готовых мандал',
    photo_file_ids=[
        'AgACAgIAAxkDAAIBVWTMl4vXuhVU0GmcwHECQ81P01tzAAJN0TEb5RlgSgV-sltK2xWIAQADAgADcwADLwQ',
        'AgACAgIAAxkDAAIBWWTMl7wb5Xgvfl8X9JZiknmstH7QAAJO0TEb5RlgSqL5B7Y3t17aAQADAgADcwADLwQ',
        'AgACAgIAAxkDAAIBXWTMl-bx1OZC9Hjcw9v08U-jQbJ_AAJQ0TEb5RlgSlyr3LNGlaTBAQADAgADcwADLwQ'
    ]
)

INSTRUCTION_PAGE_1 = Page(
    link='inst_page_3',
    text='Распечатайте чистую мандалу, которую в дальнейшем будете закрашивать. Для удобства можете скачать её у нас.',
    photo_file_id='AgACAgIAAxkBAAIBHWTMiLNMuguWJIAGPH5WuN_72bNSAAPRMRvlGWBKikQu6xuHZzABAAMCAANzAAMvBA'
)

INSTRUCTION_PAGE_2 = Page(
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

INSTRUCTION_PAGE_3 = Page(
    link='inst_page_2',
    text='Результат заполнения',
    photo_file_id='AgACAgIAAxkBAAPsZMlV_8rCsTwlOTv2g5GMjppF3qwAAn7SMRsi-EhKROw5vmEK1kQBAAMCAANzAAMvBA'
)

INSTRUCTION_PAGE_4 = Page(
    link='inst_page_4',
    text=
"""
Каждая цифра в полученном при расчетах треугольнике соответствует определенному цвету.

Закрасьте именно такими цветами каждую ячейку в треугольном сегменте мандалы (сегментов 6 и они одинаковые). 

В нашем случае последовательность 2603196996913062 будет соответствовать внешней стороне шестиугольника, а цифра 4 будет находиться в самой серединке.
""",
photo_file_id='AgACAgIAAxkBAAIBImTMiwXUNZZhh4LgQxO2TAZwg_EnAAII0TEb5RlgSiJd_MS2dL2tAQADAgADcwADLwQ'
)

INSTRUCTION_PAGE_5 = Page(
    link='inst_page_5',
    text='Закрашенный сегмент (всего 6)',
    photo_file_id='AgACAgIAAxkBAAIB12TM4BwvipUY1DlYGF6ktKTufEMYAAJMzDEbLllpSsvU-angI0VuAQADAgADcwADLwQ'
)

INSTRUCTION_PAGE_6 = Page(
    link='inst_page_6',
    text='Готовая мандала',
    photo_file_id='AgACAgIAAxkDAAIBpGTM2YIox26WXIn-io2MowQDhuFiAAJW0TEb5RlgSlphTvygGnjLAQADAgADcwADLwQ'
)

INSTRUCTION_PAGE_1.set_reply_markup({'Далее': {'callback_data': INSTRUCTION_PAGE_2.link}})
INSTRUCTION_PAGE_2.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_1.link}, 'Далее': {'callback_data': INSTRUCTION_PAGE_3.link}})
INSTRUCTION_PAGE_3.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_2.link}, 'Далее': {'callback_data': INSTRUCTION_PAGE_4.link}})
INSTRUCTION_PAGE_4.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_3.link}, 'Далее': {'callback_data': INSTRUCTION_PAGE_5.link}})
INSTRUCTION_PAGE_5.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_4.link}, 'Далее': {'callback_data': INSTRUCTION_PAGE_6.link}})
INSTRUCTION_PAGE_6.set_reply_markup({'Назад': {'callback_data': INSTRUCTION_PAGE_5.link}})

LINKS = {
    START_PAGE.link: START_PAGE,
    EXAMPLES_PAGE.link: EXAMPLES_PAGE,
    INSTRUCTION_PAGE_1.link: INSTRUCTION_PAGE_1,
    INSTRUCTION_PAGE_2.link: INSTRUCTION_PAGE_2,
    INSTRUCTION_PAGE_3.link: INSTRUCTION_PAGE_3,
    INSTRUCTION_PAGE_4.link: INSTRUCTION_PAGE_4,
    INSTRUCTION_PAGE_5.link: INSTRUCTION_PAGE_5,
    INSTRUCTION_PAGE_6.link: INSTRUCTION_PAGE_6
}