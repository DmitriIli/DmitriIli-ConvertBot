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
    'USD': float(json_dict['rates']['USD']),
    'RUB': float(json_dict['rates']['RUB']),
    'EUR': 1
}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Бот для актуальной конвертации валют.\n Ввести через пробел <валюта, для конвертации> '
                     '<валюта, в которую производится конвертация> <количество конвертируемой валюты> \n '
                     '/values - для получения списка доступных валют')


@bot.message_handler(commands=['values'])
def start_message(message):
    bot.send_message(message.chat.id,
                     text='евро - EUR \n доллар - USD \n рубль - RUB ')


@bot.message_handler(content_types=['text'])
def start_message(message):
    message.text = re.sub(r'\s+', ' ', message.text).strip()
    try:
        message.text = re.sub(r'\s+', ' ', message.text).strip()
        ls = message.text.split(' ')
        if len(ls) != 3:
            raise InputError('повторите ввод')
        else:
            convert_from = ls[0]
            convert_into = ls[1]
            convert_from_upper = str(convert_from).upper().strip()
            convert_into_upper = str(convert_into).upper().strip()

        if str(ls[2]).isdigit():
            amount = float(ls[2])
        else:
            raise InputError('количесвто должно быть число')

        if amount < 0:
            raise InputError('количество должно быть больше 0')

        if convert_from_upper in ('USD', 'RUB', 'EUR') and convert_into_upper in (
                'USD', 'RUB', 'EUR'):

            convert_into_EUR = amount / values[convert_from_upper]
            converted = convert_into_EUR * values[convert_into_upper]
            bot.send_message(message.chat.id,
                             text=f'{amount} {convert_from_upper} = {converted:.2f} {convert_into_upper}')
        else:
            raise InputError('не корректный ввод.\n USD,EUR,RUB')

    except InputError as e:
        bot.reply_to(message, text=f'{e.__str__()}')


bot.polling(non_stop=True)
