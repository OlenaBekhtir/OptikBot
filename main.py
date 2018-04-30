""" Из библиотека Телеграм импортируем нужные нам модули: модуль обновления Updater, модуль
перехвата и обработки команд CommandHandler, модуль перехвата и обработки сообщений MessageHandler,
модуль фильтрации данных
    Также импортируем форматы обмена данными apiai, json
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json

# Устанавливаем ключ доступа к телеграм боту, который был получен от FatherBot при создании этого бота
updater = Updater(token='567859700:AAH-pRjh-LKZ2ht7rnD_kNykcigyZkIlCTw')
# Создаем диспетчера, который будет отслеживать все новые данные
dispatcher = updater.dispatcher

# Создаем функцию, которая будет выводить приветствие при запуске телеграм бота
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, как дела?')

# Создаем функцию, которая будет обрабатывать запросы пользователя и формировать на них ответы
def text_message(bot, update):
    """Подключаем DialogFlow, указав полученный при регистрации client access token
    (берется с учетной записи на сайте https://console.dialogflow.com)"""
    request = apiai.ApiAI('4981be02437a42b4bfd0ecb2b9006c22').text_request()
    # Указываем язык, на котором будем общаться с ботом
    request.lang = 'ru'
    # Указываем имя пользователя, которым был создан телеграм бот (берется из информации о боте в Телеграм)
    request.session_id = 'OlenaBekhtirBot'
    # Формирование текста ответа бота на вопрос пользователя
    request.query = update.messange.text
    # Вывод ответа в удобной для пользователя форме
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']
    # Формируем ответ бота в случае корректного и некорректного запроса пользователя
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не понял!')

"""Запускаем секретарей, которые будут обеспечивать работу функций,
 секретарей должно быть столько же, сколько и функций"""
start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)

#Связываем секретарей с дисперчерами
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Запускаем бесконечную работу бота, до его остановки комбинацией клавиш CTRL_C
updater.start_polling(clean=True)
updater.idle()

