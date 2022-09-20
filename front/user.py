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


USER_KB = ['']


@logging()
def init_user(bot : TeleBot, _id : str) -> None:
    txt = ('Вы вошли в аккаунт пользователя. '
           'Идёт получение документов. '
           'Подождите окончания загрузки.')

    bot.send_message(_id, txt, reply_markup=rmvKey())
    
    if not __is_exist(_id):
        insert_db(...)
    
    bot.send_message(_id, '', reply_markup=set_keyboard(USER_KB))
