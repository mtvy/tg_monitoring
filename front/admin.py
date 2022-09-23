from curses.ascii import isdigit
from datetime      import datetime
from typing        import Any, Dict, Literal
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import get_date, set_keyboard


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
    
    date = get_date()

    if not __is_exist(_id):
        insert_db(f"INSERT INTO accs_tb (tid, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', '{{}}')", 'accs_tb')
    else:
        insert_db(f"UPDATE accs_tb SET entr_date='{date}' WHERE tid='{_id}'", 'accs_tb')

    
    bot.send_message(_id, 'Загрузка закончена.', reply_markup=set_keyboard(ADMIN_KB))


@logging()
def add_admin(bot : TeleBot, _id : str) -> None:

    @logging()
    def __add_admin(msg : Message, bot : TeleBot, _id : str):
        txt : str = msg.text
        if txt.isdigit():
            if insert_db(f"INSERT INTO admins_tb (tid) VALUES ('{txt}')", 'admins_tb'):
                bot.send_message(_id, 'Пользователь добавлен!', reply_markup=set_keyboard(ADMIN_KB))
            else:
                bot.send_message(_id, 'Пользователь уже добавлен.', reply_markup=set_keyboard(ADMIN_KB))
        else:
            bot.send_message(_id, 'Неверный формат id!', reply_markup=set_keyboard(ADMIN_KB))


    msg = bot.send_message(_id, 'Введите id админа в формате 12345678.', reply_markup=rmvKey())
    bot.register_next_step_handler(msg, __add_admin, bot, _id)


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
        bot.send_message(_id, f'Отправлено уведомлений: {len(accs)}', reply_markup=set_keyboard(ADMIN_KB))

    txt = 'Введите сообщение для рассылки'
    msg = bot.send_message(_id, txt, reply_markup=rmvKey())
    bot.register_next_step_handler(msg, __send_info, bot, _id, accs)


@logging()
def send_call_resp(bot : TeleBot, _id : int, user_id : str, msg_id : int) -> None:

    #           make del_msg global
    @logging()
    def del_msg(sender_id : int, _msg_id : int) -> None:
        bot.delete_message(sender_id, _msg_id)
    

    @logging()
    def __send_call_resp(msg : Message, bot : TeleBot, _id : int, _user_id : str) -> None:
        bot.send_message(_user_id, f'Сообщение от тех. поддержки:\n{msg.text}\n')
        bot.send_message(_id, f'Сообщение отправлено пользователю @test_tim_bot')

    del_msg(_id, msg_id)
    msg = bot.send_message(_id, 'Введите сообщение для ответа.')
    bot.register_next_step_handler(msg, __send_call_resp, bot, _id, user_id)
