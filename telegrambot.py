import telebot
from telebot import types
import requests
import json
import re
from config import TOKEN, API_KEY, base, convert_into
from utils import InputError



url = f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&symbols={convert_into}&format=1'

r = requests.get(url)

json_dict = json.loads(r.content)

values = {
    'EUR': 1,
    'USD': float(json_dict['rates']['USD']),
    'RUB': float(json_dict['rates']['RUB'])
}


class InputError(Exception):
    pass


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Бот для актуальной конвертации валют.\n <валюта, для конвертации> ,'
                     '<валюта, в которую производится конвертация>, <количество конвертируемой валюты> \n '
                     '/values - для получения списка доступных валют')


@bot.message_handler(commands=['values'])
def start_message(message):
    bot.send_message(message.chat.id,
                     text='Бот возвращает цену на определённое количество валюты (евро - EUR, доллар - USD или рубль - RUB).')


@bot.message_handler(content_types=['text'])
def start_message(message):
    pattern = '\w+\,\w+\,\d+'

    try:
        if re.search(pattern, message.text):
            ls = message.text.split(',')
            print(*ls)
            convert_from = ls[0]
            convert_into = ls[1]
            amount = int(ls[2])

            if convert_from in ('USD', 'RUB', 'EUR') and convert_into in (
                    'USD', 'RUB', 'EUR') and convert_into != convert_from \
                    and str(amount).isdigit():
                convert_into_EUR = amount / values[convert_from]
                converted = convert_into_EUR * values[convert_into]
                bot.send_message(message.chat.id, text=f'{amount} {convert_from} = {converted:.2f} {convert_into}')
            else:
                raise InputError('/values')
        else:
            raise InputError(
                'формат ввода:<валюта для конветации>,<валюта,в которую будет производиться конвертация>,<количество '
                'конвертируемой валюты>')
    except InputError as e:
        bot.reply_to(message, text=f'{e}')


bot.polling(non_stop=True)
