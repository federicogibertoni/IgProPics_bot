import telebot
import os, time, re, requests, json

bot = telebot.TeleBot(token=os.environ['IGPROPIC_TOKEN'])
rfilter = r'(@(\w|\d|\.|_)+)+'


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
    return usr_list


def get_pro_pic_hd(message, p_url):
    response = requests.get(f'{p_url}/?__a=1', headers={"User-Agent": "Mozilla/5.0"})
    try:
        json_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        bot.reply_to(message, "Response string could not be converted to JSON, please try again later")
        return None
    else:
        return json_data['graphql']['user']['profile_pic_url_hd']

@bot.message_handler(regexp=rfilter)
def send_pic(message):
    usernames = get_usernames(message)
    for u in usernames:
        profile_url = f'https://www.instagram.com/{u[1:]}'
        pic_url = get_pro_pic_hd(message, profile_url)
        if pic_url is not None:
            bot.send_photo(message.chat.id, pic_url)


bot.polling()
