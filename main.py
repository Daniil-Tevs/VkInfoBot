import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("5645360728:AAFQytUgyOXKj6WOisuI38OQZqtyGKPOGOk")


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.from_user.id, "Привет! Вот, что я умею:"
                                           "\n/find [адрес] - поиск информации о людях в вк"
                                           "\n/help - помощь")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.from_user.id, "Вот, что я умею:\n\n/find - поиск информации о людях в вк")


@bot.message_handler(commands=['find'])
def find_command(message):
    if len(message.text.split()) == 1:
        bot.send_message(message.from_user.id, "Укажите адрес пользователя")
        return
    url = message.text.split()[1]
    if url.count("https://vk.com/") == 0:
        response = requests.get("https://vk.com/" + url)
    else:
        response = requests.get(url)

    if response.status_code == 200:
        content = BeautifulSoup(response.text, 'html.parser')
        name = content.find('h2', class_="op_header")
        information = name.text

        if content.find('div', class_="service_msg service_msg_null") is None:
            block_info = content.find('div', class_="OwnerInfo")
            info = block_info.findAll('a')
            if len(info) > 0:
                info.pop()
                for i in info:
                    information += "\n" + i.text

        bot.send_message(message.from_user.id, information)
    else:
        bot.send_message(message.from_user.id, "Информация не найдена")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Непонятная команда. Используй /help")


bot.polling(none_stop=True, interval=0)
