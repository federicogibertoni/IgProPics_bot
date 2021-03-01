import telebot
import os
import time
import re
import requests
import json

bot = telebot.TeleBot(token=os.environ['IGPROPIC_TOKEN'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ciao")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Send an Ig username to get some information! Remember to use '@'!")


def get_username(message):
    usr_list = list()
    p = re.compile(r'@\w+')
    for usr in p.finditer(message.text):
        usr_list.append(usr.group())

    if not usr_list:
        bot.send_message(message, f'No username found for {message.text}')
        raise IndexError
    return usr_list


def get_pro_pic_hd(message, pro_name):
    response = requests.get(f'{pro_name}/?__a=1', headers={"User-Agent": "Mozilla/5.0"})
    json_data = json.loads(response.text)
    return json_data['graphql']['user']['profile_pic_url_hd']


@bot.message_handler(func=lambda msg: msg.text is not None and re.match(r'@\w+', msg.text))
def send_pic(message):
    l = get_username(message)
    profile_name = 'https://www.instagram.com/{}'.format(l[0][1:])

    bot.send_photo(message.chat.id, get_pro_pic_hd(message, profile_name))


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(5)
