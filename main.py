from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import keyboard as kb
from googletrans import Translator, LANGCODES
import database as db
load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = TeleBot(TOKEN)
translator = Translator()

# @bot.message_handler(commands=['start'])
# def start(message: types. Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, f'Привет, {message.from_user.first_name}',
#                      reply_markup=kb.test_kb())
#
# @bot.message_handler(commands=['help'])
# def start(message: types. Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, f'Вижу вам нужна помощь {message.from_user.first_name}, ну вот ну чо я скажу')
#
# @bot.message_handler(func=lambda msg: msg.text == 'Test')
# def answer_test(message: types.Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, 'Вы нажали Test')
#
# @bot.message_handler(func=lambda msg: msg.text == 'Ezz')
# def answer_test(message: types.Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, 'Вы нажали EZZZZZZZZZZ')
#
# @bot.message_handler(content_types=['text'])
# def answer(message: types. Message):
#     print(message.text)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    db.add_user(first_name, chat_id)
    bot.send_message(chat_id, 'Выберите действие снизу',
                     reply_markup=kb.start_kb()
                     )

@bot.message_handler(func=lambda msg: msg.text == 'Start')
def start_trans(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите язык для перевода',
                     reply_markup=kb.lang_kb())
    bot.register_next_step_handler(message, get_lang_from)

@bot.message_handler(func=lambda msg: msg.text == 'History')
def start_trans(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Вот ваша история переводов: ',
                    reply_markup=kb.lang_kb())
    bot.register_next_step_handler(message, get_history)

def get_lang_from(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите на какой язык вы хотите сделать перевод',
                     reply_markup=kb.lang_kb())
    bot.register_next_step_handler(message, get_lang_to, message.text)

def get_lang_to(message: types.Message, lang_from):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напиши слово или предложение для перевода',
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, translate, lang_from, message.text)

def translate(message: types.Message, lang_from, lang_to):
    chat_id = message.chat.id
    _from = LANGCODES[lang_from]
    _to = LANGCODES[lang_to]
    translated_text = translator.translate(message.text, dest=_to, src=_from).text
    db.add_translations(_from, _to, message.text, chat_id, translated_text)
    db.get_history(lang_from, lang_to, message.text, chat_id, translated_text)
    bot.send_message(chat_id, translated_text)
bot.infinity_polling()



