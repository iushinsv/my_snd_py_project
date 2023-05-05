import telebot
import config
import messages
import re
import random
import requests
from bs4 import BeautifulSoup as bs
from telebot import types

def parser(url):
    r = requests.get(url)
    #print(r.status_code)
    #print(r.text)

    soup = bs(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    #print(anekdots)
    clear_anekdots = [c.text for c in anekdots]
    #print(*clear_anekdots, sep='\n')
    return clear_anekdots

list_of_jokes = parser(str(config.URL + '5'))
random.shuffle(list_of_jokes)


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #item1 = types.KeyboardButton(messages.MAKE_REMIND_MESSAGE)
    #item2 = types.KeyboardButton("help")
    #markup.add(item1, item2)

    bot.send_message(message.chat.id, messages.WELCOME_MESSAGE_part_1.format(message.from_user, bot.get_me()),
                    parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, messages.WELCOME_MESSAGE_part_2)




@bot.message_handler(content_types=['text'])
def Jokes(message: telebot.types.Message):
    if message.text.lower() in '123456789':
        if len(list_of_jokes) > 0:
            bot.send_message(message.chat.id, list_of_jokes[0])
            del list_of_jokes[0]
        else:
            list_of_jokes.extend(parser(config.URL + '4'))
            random.shuffle(list_of_jokes)
            bot.send_message(message.chat.id, list_of_jokes[0])

    else:
        bot.send_message(message.chat.id, messages.WELCOME_MESSAGE_part_2)
          


#RUN
bot.polling(non_stop=True)
