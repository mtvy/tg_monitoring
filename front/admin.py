from datetime      import datetime
from typing        import Any, Dict, Literal
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import set_keyboard


@logging()
def __is_exist(_id : str) -> bool:
    for it in get_db('accs_tb'):
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
        insert_db(f"INSERT INTO accs_tb (tib) VALUE ('{_id}')")
    
    bot.send_message(_id, 'Загрузка закончена.', reply_markup=set_keyboard(ADMIN_KB))


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


@logging()
def ask_accounts(bot : TeleBot, _id : str) -> None:
    txt = 'Кому сделать уведомление?'
    bot.send_message(_id, txt, reply_markup=set_keyboard(['Админы', 'Пользователи']))

@logging()
def send_info(bot : TeleBot, _id : str, accs : Dict[str, Any]) -> None:
    
    @logging()
    def __send_info(msg : Message, bot: TeleBot, _id : str, accs : Dict[str, Any]) -> None:
        for acc in accs.keys():
            bot.send_message(acc, msg.text)
        bot.send_message(_id, f'Отправлено уведомлений: {len(accs)}')

    txt = 'Введите сообщение для рассылки'
    msg = bot.send_message(_id, txt, reply_markup=rmvKey())
    bot.register_next_step_handler(msg, __send_info, bot, _id, accs)
    
