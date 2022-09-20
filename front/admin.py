from datetime      import datetime
from telebot       import TeleBot
from telebot.types import ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import set_keyboard


@logging()
def __is_exist(_id : str) -> bool:
    for it in get_db('ids_tb'):
        if it[1] == _id:
            return True
    return False


ADMIN_KB = ['Уведомить', 'Добавить админа', 'Посмотреть LTV']


@logging()
def init_admin(bot : TeleBot, _id : str) -> None:
    txt = ('Вы вошли в аккаунт админа. '
           'Идёт получение документов. '
           'Подождите окончания загрузки.')

    bot.send_message(_id, txt, reply_markup=rmvKey())
    
    if not __is_exist(_id):
        insert_db(...)
    
    bot.send_message(_id, '', reply_markup=set_keyboard(ADMIN_KB))


@logging()
def add_admin(bot : TeleBot, _id : str) -> None:
    if insert_db('INSERT INTO admin_tb...'):
        bot.send_message(_id, 'Пользователь добавлен!')
    else:
        bot.send_message(_id, 'Пользователь не добавлен!')


@logging()
def get_session_info(bot : TeleBot, _id : str) -> None:
    txt = 'Получение статистики за сегодня...'
    bot.send_message(_id, txt, reply_markup=rmvKey())

    accs = get_db('accs_tb'); info = {'users' : 0, 'buys' : 0}
    for acc in accs:
        now = datetime.now()
        if acc[3] == f'{now.year}-{now.month}-{now.day}':
            info['users'] += 1
    
    txt = (f'Пользователей: {info["users"]}\n'
           f'Покупок: {info["buys"]}')
    bot.send_message(_id, txt)

    txt = 'Статистика получена!'
    bot.send_message(_id, txt, reply_markup=set_keyboard(ADMIN_KB))
