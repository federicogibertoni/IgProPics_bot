import telebot
import os, time, re, requests, json

bot = telebot.TeleBot(token=os.environ['IGPROPIC_TOKEN'])
rfilter = re.compile(r'(@\w+)+')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ciao")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Send multiple Ig username to get some information! Remember to use '@'!")


def get_usernames(message):
    usr_list = list()
    for usr in rfilter.finditer(message.text):
        usr_list.append(usr.group())

    if not usr_list:
        bot.send_message(message, f'No username found for {message.text}')
        raise IndexError
    return usr_list


def get_pro_pic_hd(pro_name):
    response = requests.get(f'{pro_name}/?__a=1', headers={"User-Agent": "Mozilla/5.0"})
    json_data = json.loads(response.text)
    return json_data['graphql']['user']['profile_pic_url_hd']


@bot.message_handler(func=lambda msg: msg.text is not None and rfilter.match(msg.text))
def send_pic(message):
    usernames = get_usernames(message)
    for u in usernames:
        profile_url = f'https://www.instagram.com/{u[1:]}'
        bot.send_photo(message.chat.id, get_pro_pic_hd(profile_name))


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(5)
