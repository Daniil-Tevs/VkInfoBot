import telebot
import requests

from bs4 import BeautifulSoup


def findInfoUserVk(url):
    information = ""
    if url.count("https://vk.com/") == 0:
        response = requests.get("https://vk.com/" + url)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        td = BeautifulSoup(content, 'html.parser')
        name = td.find('h2',class_="op_header")
        information+=name.text
        block = td.find('div', class_="OwnerInfo")
        list = block.findAll('a')
        list.pop()
        for i in list:
            information+="\n"+i.text
        return information


def main():
    bot = telebot.TeleBot("5645360728:AAFQytUgyOXKj6WOisuI38OQZqtyGKPOGOk")

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "/start":
            bot.send_message(message.from_user.id, "Привет. Вот,что я умею:\n /find - поиск информации о людях в вк")
        elif message.text == "/find":
            bot.send_message(message.from_user.id, "Скинь адрес человека в вконтакте")
        else:
            bot.send_message(message.from_user.id, findInfoUserVk(message.text))

    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    main()
