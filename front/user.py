from datetime      import datetime
from telebot       import TeleBot
from telebot.types import ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import set_keyboard


USER_KB = ['']


@logging()
def init_user(bot : TeleBot, _id : str) -> None:
    txt = ('Вы вошли в аккаунт пользователя. '
           'Идёт получение документов. '
           'Подождите окончания загрузки.')

    bot.send_message(_id, txt, reply_markup=rmvKey())
    
    now = datetime.now()
    date = f'{now.year}-{now.month}-{now.day}'
    insert_db('INSERT INTO users_tb...')
    insert_db('INSERT INTO accs_tb...')
    
    bot.send_message(_id, '', reply_markup=set_keyboard(USER_KB))
