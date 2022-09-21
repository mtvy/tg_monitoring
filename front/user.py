from datetime      import datetime
from typing        import Any, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import set_keyboard


USER_KB = [
    'Мониторинг', 
    'Соглашение', 
    'Тех. Поддержка', 
    'Профиль', 
    'Рефералка'
]


@logging()
def init_user(bot : TeleBot, _id : str) -> None:
    txt = ('Вы вошли в аккаунт пользователя. '
           'Идёт получение документов. '
           'Подождите окончания загрузки.')

    bot.send_message(_id, txt, reply_markup=rmvKey())
    
    ...
    now = datetime.now()
    date = f'{now.year}-{now.month}-{now.day}'
    insert_db('INSERT INTO users_tb...')
    insert_db('INSERT INTO accs_tb...')
    ...
    
    bot.send_message(_id, '', reply_markup=set_keyboard(USER_KB))


@logging()
def start_user(bot : TeleBot, _id : str) -> None:
    txt = f'Аккаунт пользователя #{_id}'
    bot.send_message(_id, txt, reply_markup=set_keyboard(USER_KB))


MON_KB = ['Аторизация', 'Каналы', 'Настройка', 'Назад']

@logging()
def enter_monitoring(bot : TeleBot, _id : str) -> None:
    txt = 'Настроки мониторинга.'
    bot.send_message(_id, txt, reply_markup=set_keyboard(MON_KB))


CHNL_KB = ['Показать', 'Добавить', 'Удалить']

@logging()
def push_chnl(bot : TeleBot, _id : str) -> None:
    txt = 'Настройки каналов.'
    bot.send_message(_id, txt, reply_markup=set_keyboard(CHNL_KB))


PRFL_KB = ['Назад']

@logging()
def show_prfl(bot : TeleBot, _id : str) -> None:
    txt = (f'Профиль пользователя #{_id}\n'
           f'...')
    bot.send_message(_id, txt, reply_markup=set_keyboard(PRFL_KB))
