import telebot
from telebot import types
from random import shuffle, randrange
from time import sleep
from answers import (AFTER_RIGHT_ANSWER,
                     AFTER_WRONG_ANSWER,
                     TRUE_QUOTE,
                     NEXT_ROUND_SLOGAN)
from config import TOKEN
from quote import quote
from parse_func import parse_function, plus_point, minus_point, get_ending

bot = telebot.TeleBot(TOKEN, parse_mode=None)


# здоровается с пользователями
@bot.message_handler(commands=['start'])
def start(message):
    parse_function(message)
    if message.from_user.first_name is not None:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    else:
        bot.send_message(message.chat.id, 'Рад тебя видеть!')
    sleep(1.2)
    bot.send_message(message.chat.id, 'Погнали!')
    sleep(0.7)
    guess_quote(message)


@bot.message_handler(commands=['Продолжаем', 'Еще цитату!', 'Попробуем еще одну!', 'Дальше!'])
def guess_quote(message):
    global TRUE_QUOTE
    # выбираем из списка список с названием фильма и цитатой для угадывания
    TRUE_QUOTE = quote[randrange(0, len(quote))]
    x = 0
    # добавляем название фильма в список, если такого названия там еще нет
    # т.к. из одного фильма может быть несколько цитат.
    buffer_film_name = [TRUE_QUOTE[1]]
    # добавляем цитату и название фильма
    list_quote = [TRUE_QUOTE, ]
    while x != 3:
        i = quote[randrange(0, len(quote))]
        if i[1] not in buffer_film_name:
            list_quote.append(i)
            buffer_film_name.append(i[1])
            x += 1
    shuffle(list_quote)

    # создаем встроенные кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # и добавляем кнопки по одной
    # в первом значении стоит название кнопики, в значении callback_data
    # стоит значение ответа кнопки, т.е., что передается при ее вызове.
    btn1 = types.KeyboardButton(f'{list_quote[0][1]}')
    btn2 = types.KeyboardButton(f'{list_quote[1][1]}')
    btn3 = types.KeyboardButton(f'{list_quote[2][1]}')
    btn4 = types.KeyboardButton(f'{list_quote[3][1]}')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    # отправляем цитату из фильма, который угадываем
    bot.send_message(message.chat.id, f'"{TRUE_QUOTE[0]}"',
                     reply_markup=markup)


# сравниваем выданную цитату с нажатой кнопкой
@bot.message_handler(content_types=['text'])
def check_answer(message):
    # register_next_step_handler() принимает два обязательных аргумента:
    # первый это message, а второй это function. Работает таким образом:
    # ждёт сообщ-е пользователя и вызывает указ-ю функцию с аргументом message
    bot.register_next_step_handler(message, guess_quote)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton(
        f'''{NEXT_ROUND_SLOGAN[randrange(0, len(NEXT_ROUND_SLOGAN))]}'''
    )
    markup.add(btn)
    if message.text == TRUE_QUOTE[1]:
        # здесь хранится количество очков и правильное окончание слова 'балл'
        points = plus_point(message)
        ending = get_ending(points)
        bot.send_message(message.chat.id, f'Ваш выбор: {message.text}')
        sleep(0.5)
        bot.send_message(
            message.chat.id,
            f'''{AFTER_RIGHT_ANSWER[randrange(0, len(AFTER_RIGHT_ANSWER))]} Это "{TRUE_QUOTE[1]}".\n{points} {ending} вам на счет''',
            reply_markup=markup
        )
    else:
        # здесь хранится количество очков и правильное окончание слова 'балл'
        points = minus_point(message)
        ending = get_ending(points)
        bot.send_message(message.chat.id, f'Ваш выбор: {message.text}')
        sleep(0.5)
        bot.send_message(
            message.chat.id, f'''{AFTER_WRONG_ANSWER[randrange(
            0, len(AFTER_WRONG_ANSWER))]} Это не "{message.text}". Правильный ответ: "{TRUE_QUOTE[1]}".\n{points} {ending} спишем с вашего счета''',
            reply_markup=markup
        )


# выводит всю доступную информацию о чате
@bot.message_handler(commands=['message'])
def msg_info(message):
    bot.reply_to(message, message)


# выводит описание
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(
        message, """Игровой бот с цитатами из фильмов. Все просто:
        4 варианта названия фильмов - один правильный. Угадываешь откуда
        цитата - получаешь мое почтение, не угадываешь... Что ж...
        Правильный ответ выводится и идем пересматривать классику.
        Написать автору бота можно сюда: pvnick@yandex.ru""",
        parse_mode='html'
    )


# запускаем бот на постоянное выполнение
bot.infinity_polling()
# или так: bot.polling(none_stop=True)
