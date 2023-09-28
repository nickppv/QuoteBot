import sqlite3
from datetime import datetime
import random


def parse_function(message):
    # подключаемся к БД
    conn = sqlite3.connect('db_users.sqlite3')
    # объект "курсор" позволяет делать запросы к БД
    cur = conn.cursor()
    users_data = []
    # получаем данные из БД и сравниваем на дублирование записей
    cur.execute('SELECT user_tg_id FROM users')
    users_data = cur.fetchall()
    users_data = [int(i[0]) for i in users_data if len(users_data) > 0]
    if message.from_user.id not in users_data:
        # получаем данные пользователя, которые передадим потом в БД кортежем
        user = (
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
            message.from_user.username,
            datetime.now().strftime("%d.%m.%Y, %H:%M")
            )
        # метод с вопросительными знаками позволяет защититься от sql-инъекций
        cur.execute("INSERT INTO users (user_tg_id, name, surname, username, first_play_time) VALUES (?, ?, ?, ?, ?)", user)
        conn.commit()
    cur.close()
    conn.close()


def get_ending(points):
    ending = ''
    if points % 10 == 1 and not 11 <= points <= 14:
        ending = 'балл'
    elif points % 10 > 1 and points % 10 < 5 and not 11 <= points <= 14:
        ending = 'балла'
    else:
        ending = 'баллов'
    return ending


def plus_point(message):
    conn = sqlite3.connect('db_users.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT points FROM users WHERE user_tg_id == ' + str(message.from_user.id))
    init_points = cur.fetchone()[0]
    # получаем случайное количество баллов и правильное окончание
    points = random.randint(1, 30)
    if 1 < points <= 10:
        result_points = init_points + points
    if points in [20, 25, 30]:
        result_points = init_points + points
    else:
        points = random.randint(1, 10)
        result_points = init_points + points
    cur.execute('UPDATE users SET points = ' + str(result_points) + ' WHERE user_tg_id = ' + str(message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return points


def minus_point(message):
    conn = sqlite3.connect('db_users.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT points FROM users WHERE user_tg_id == ' + str(message.from_user.id))
    init_points = cur.fetchone()[0]
    # получаем случайное количество баллов и правильное окончание
    points = random.randint(1, 30)
    if 1 < points <= 10:
        result_points = init_points - points
    elif points in [20, 25, 30, 40, 50]:
        result_points = init_points - points
    else:
        points = random.randint(1, 10)
        result_points = init_points - points
    cur.execute('UPDATE users SET points = ' + str(result_points) + ' WHERE user_tg_id = ' + str(message.from_user.id))
    conn.commit()
    cur.close()
    conn.close()
    return points


def get_rating(message):
    conn = sqlite3.connect('db_users.sqlite3')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users ORDER BY points DESC')
    all_data = cur.fetchall()
    cur.close()
    conn.close()
    actual_index = [all_data.index(i) for i in all_data if i[0] == message.from_user.id][0]
    if not actual_index:
        return f'''Вы на первом месте! У вас {all_data[0][-1]} {get_ending(all_data[0][-1])}. Опережение соперника за вами составляет {all_data[0][-1] - all_data[1][-1]} {get_ending(all_data[0][-1] - all_data[1][-1])}. А разрыв с третьим местом: {all_data[0][-1] - all_data[2][-1]} {get_ending(all_data[0][-1] - all_data[2][-1])}.'''
    elif actual_index == 1:
        return f'''Вы на втором месте! У вас {all_data[1][-1]} {get_ending(all_data[1][-1])}. От первого места вы отстаете на {all_data[0][-1] - all_data[1][-1]} {get_ending(all_data[0][-1] - all_data[1][-1])}. А разрыв с третьим местом: {all_data[1][-1] - all_data[2][-1]} {get_ending(all_data[1][-1] - all_data[2][-1])}.'''
    elif actual_index == 2:
        return f'Вы на третьем месте! У вас {all_data[2][-1]} {get_ending(all_data[2][-1])}. От второго места вы отстаете на {all_data[1][-1] - all_data[2][-1]} {get_ending(all_data[1][-1] - all_data[2][-1])}. А разрыв с первым местом: {all_data[0][-1] - all_data[2][-1]} {get_ending(all_data[0][-1] - all_data[2][-1])}.'
    elif actual_index == 3:
        return f'Вы на четвертом месте! У вас {all_data[3][-1]} {get_ending(all_data[3][-1])}. От третьего места вы отстаете на {all_data[2][-1] - all_data[3][-1]} {get_ending(all_data[2][-1] - all_data[3][-1])}. Нужно поднажать!'
    else:
        return f'Вы на {actual_index+1}-м месте! У вас {all_data[actual_index][-1]} {get_ending(all_data[actual_index][-1])}. От соперника впереди вы отстаете на {all_data[actual_index-1][-1] - all_data[actual_index][-1]} {get_ending(all_data[actual_index-1][-1] - all_data[actual_index][-1])}. Нужно поднажать!'
