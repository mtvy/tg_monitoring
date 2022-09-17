from telebot       import TeleBot
from telebot.types import ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import set_keyboard


@logging()
def __is_exist(_id : int) -> bool:
    for it in get_db('ids_tb'):
        if int(it[1]) == _id:
            return True
    return False


ADMIN_KB = ['Уведомить', 'Добавить админа', 'Посмотреть LTV']


@logging()
def init_admin(bot : TeleBot, _id : int) -> None:
    txt = ('Вы вошли в аккаунт админа. '
           'Идёт получение документов. '
           'Подождите окончания загрузки.')

    bot.send_message(_id, txt, reply_markup=rmvKey())
    
    if not __is_exist(_id):
        insert_db(...)
    
    bot.send_message(_id, '', reply_markup=set_keyboard(ADMIN_KB))
