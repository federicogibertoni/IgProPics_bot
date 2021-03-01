import telebot
import os, time, re, requests, json

bot = telebot.TeleBot(token=os.environ['IGPROPIC_TOKEN'])
rfilter = r'(@\w+)+'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Send me multiple Ig usernames to get some information! Remember to use '@'!")


def get_usernames(message):
    usr_list = list()
    for usr in re.finditer(rfilter, message.text):
        usr_list.append(usr.group())

    if not usr_list:
        bot.send_message(message, f'No username found for {message.text}')
        raise IndexError
    return usr_list


def get_pro_pic_hd(p_url):
    response = requests.get(f'{p_url}/?__a=1', headers={"User-Agent": "Mozilla/5.0"})
    json_data = json.loads(response.text)
    return json_data['graphql']['user']['profile_pic_url_hd']


@bot.message_handler(regexp=rfilter)
def send_pic(message):
    print(message)
    usernames = get_usernames(message)
    for u in usernames:
        profile_url = f'https://www.instagram.com/{u[1:]}'
        bot.send_photo(message.chat.id, get_pro_pic_hd(profile_url))


bot.polling()
