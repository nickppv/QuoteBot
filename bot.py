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

bot = telebot.TeleBot(TOKEN, parse_mode=None)


# здоровается с пользователями
@bot.message_handler(commands=['start'])
def start(message):
    file = open('users.txt', 'a', encoding='utf-8')
    file.write(f'''User ID - {
        message.from_user.id}, First name - {
        message.from_user.first_name}, Last name - {
        message.from_user.last_name}, Username - {
        message.from_user.username}\n''')
    file.close()
    if message.from_user.first_name is not None:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    else:
        bot.send_message(message.chat.id, 'Рад тебя видеть!')
    sleep(1.5)
    bot.send_message(message.chat.id, 'Погнали!')
    sleep(1)
    guess_quote(message)


@bot.message_handler(commands=['play'])
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
    markup = types.InlineKeyboardMarkup(row_width=1)
    # и добавляем кнопки по одной
    # в первом значении стоит название кнопики, в значении callback_data
    # стоит значение ответа кнопки, т.е., что передается при ее вызове.
    btn1 = types.InlineKeyboardButton(f'{list_quote[0][1]}',
                                      callback_data=f'{list_quote[0][1]}')
    btn2 = types.InlineKeyboardButton(f'{list_quote[1][1]}',
                                      callback_data=f'{list_quote[1][1]}')
    btn3 = types.InlineKeyboardButton(f'{list_quote[2][1]}',
                                      callback_data=f'{list_quote[2][1]}')
    btn4 = types.InlineKeyboardButton(f'{list_quote[3][1]}',
                                      callback_data=f'{list_quote[3][1]}')
    markup.add(btn1, btn2, btn3, btn4)
    # отправляем цитату из фильма, который угадываем
    bot.send_message(message.chat.id, f'"{TRUE_QUOTE[0]}"',
                     reply_markup=markup)


# сравниваем выданную цитату с нажатой кнопкой
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.register_next_step_handler(call.message, guess_quote)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = types.KeyboardButton(
        f'''{NEXT_ROUND_SLOGAN[randrange(0, len(NEXT_ROUND_SLOGAN))]}'''
    )
    markup.add(btn)
    if call.data == TRUE_QUOTE[1]:
        bot.send_message(call.message.chat.id, f'Ваш выбор: {call.data}')
        sleep(1)
        bot.send_message(
            call.message.chat.id,
            f'''{AFTER_RIGHT_ANSWER[randrange(0, len(AFTER_RIGHT_ANSWER))]} Это "{TRUE_QUOTE[1]}"''',
            reply_markup=markup
        )
    else:
        bot.send_message(call.message.chat.id, f'Ваш выбор: {call.data}')
        sleep(1)
        bot.send_message(
            call.message.chat.id, f'''{AFTER_WRONG_ANSWER[randrange(
            0, len(AFTER_WRONG_ANSWER))]} Это не "{call.data}". Правильный ответ: "{TRUE_QUOTE[1]}"''',
            reply_markup=markup
        )
    bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')



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
