import telebot
import os, re, requests, json

bot = telebot.TeleBot(token=os.environ['IGPROPIC_TOKEN'])
rfilter = r'(@(\w|\d|\.|_)+)+'


# risposta al comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi")


# risposta al comando /help
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Send me one or more Ig usernames to get some information! Remember to use '@'!")


# dato il messaggio, è restituita una lista di username che sono stati scritti nel messaggio
def get_usernames(message):
    usr_list = list()
    for usr in re.finditer(rfilter, message.text):
        usr_list.append(usr.group())
    return usr_list


# ottenimento di tutti i dati di un profilo, estrazione della foto profilo
def get_pro_pic_hd(message, p_url):
    response = requests.get(f'{p_url}/?__a=1', headers={"User-Agent": "Mozilla/5.0"})
    # controllo dello status code della risposta
    if 300 > response.status_code >= 200:
        try:
            json_data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            bot.reply_to(message, "Response string could not be converted to JSON, please try again later")
            return None
        try:
            return json_data['graphql']['user']['profile_pic_url_hd']
        except KeyError:
            bot.reply_to(message, "I cannot retrieve the profile picture of this account")
            return None
    bot.reply_to(message, f"HTTP error {response.status_code} {response.reason}")
    return None


# ricezione del messaggio con gli username e risposta con foto
@bot.message_handler(regexp=rfilter)
def send_pic(message):
    usernames = get_usernames(message)
    for u in usernames:
        profile_url = f'https://www.instagram.com/{u[1:]}'
        pic_url = get_pro_pic_hd(message, profile_url)
        if pic_url is not None:
            bot.send_photo(message.chat.id, pic_url)


bot.polling()
