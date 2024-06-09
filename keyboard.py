from telebot import types
from googletrans import LANGCODES


def start_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('Start'),
        types.KeyboardButton('History')
    )
    return markup

def lang_kb():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for lang in LANGCODES.keys():
        button = types.KeyboardButton(text=lang)
        buttons.append(button)
    markup.add(*buttons)
    return markup