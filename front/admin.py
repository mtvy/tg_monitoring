#/==================================================================\#
# admin.py                                            (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from typing        import Any, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKb
#------------------------\ project modules /-------------------------#
from back.database import get_db, insert_db
from back.utility  import logging
from front.utility import get_date, set_kb, del_msg, send_msg, wait_msg
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __is_exist(_id : str) -> bool:
    for it in get_db('accs_tb'):
        if it[1] == _id:
            return True
    return False
#\------------------------------------------------------------------/#


ADMIN_KB = ['Уведомить', 'Добавить админа', 'Посмотреть LTV']

#\------------------------------------------------------------------/#
@logging()
def init_admin(bot : TeleBot, _id : str) -> None:
    txt = ('Вы вошли в аккаунт админа. '
           'Идёт получение документов. '
           'Подождите окончания загрузки.')

    send_msg(bot, _id, txt, rmvKb())
    
    date = get_date()

    if not __is_exist(_id):
        insert_db(f"INSERT INTO accs_tb (tid, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', '{{}}')", 'accs_tb')
    else:
        insert_db(f"UPDATE accs_tb SET entr_date='{date}' WHERE tid='{_id}'", 'accs_tb')

    send_msg(bot, _id, 'Загрузка закончена.', set_kb(ADMIN_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def add_admin(bot : TeleBot, _id : str) -> None:

    @logging()
    def __add_admin(msg : Message, bot : TeleBot, _id : str):
        txt : str = msg.text
        if txt.isdigit():
            if insert_db(f"INSERT INTO admins_tb (tid) VALUES ('{txt}')", 'admins_tb'):
                send_msg(bot, _id, 'Пользователь добавлен!', set_kb(ADMIN_KB))
            else: # ????
                send_msg(bot, _id, 'Пользователь уже добавлен.', set_kb(ADMIN_KB))
        else:
            send_msg(bot, _id, 'Неверный формат id!', set_kb(ADMIN_KB))

    wait_msg(bot, _id, __add_admin, 'Введите id админа в формате 12345678.', rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_session_info(bot : TeleBot, _id : str) -> None:

    send_msg(bot, _id, 'Получение статистики за сегодня...', rmvKb())

    accs = get_db('accs_tb'); info = {'users' : 0, 'buys' : 0}
    date = get_date()

    for acc in accs:
        if acc[3] == date:
            info['users'] += 1
    
    send_msg(bot, _id, f'Пользователей: {info["users"]}\nПокупок: {info["buys"]}')
    send_msg(bot, _id, 'Статистика получена!', set_kb(ADMIN_KB))
#\------------------------------------------------------------------/#


ACCS_TYPE_KB = ['Админы', 'Пользователи']

#\------------------------------------------------------------------/#
@logging()
def ask_accounts(bot : TeleBot, _id : str) -> None:
    send_msg(bot, _id, 'Кому сделать уведомление?', set_kb(ACCS_TYPE_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_info(bot : TeleBot, _id : str, accs : Dict[str, Any]) -> None:
    
    @logging()
    def __send_info(msg : Message, bot: TeleBot, accs : Dict[str, Any]) -> None:
        for acc in accs.keys():
            send_msg(bot, acc, msg.text)
        send_msg(bot, msg.chat.id, f'Отправлено уведомлений: {len(accs)}', set_kb(ADMIN_KB))

    wait_msg(bot, _id, __send_info, 'Введите сообщение для рассылки', rmvKb(), [bot, accs])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_call_resp(bot : TeleBot, _id : int, user_id : str, msg_id : int) -> None:

    @logging()
    def __send_call_resp(msg : Message, bot : TeleBot, _id : int, _user_id : str) -> None:
        send_msg(bot, _user_id, f'Сообщение от тех. поддержки:\n{msg.text}\n')
        send_msg(bot, _id, f'Сообщение отправлено пользователю @test_tim_bot', set_kb(ADMIN_KB))


    del_msg(_id, msg_id)
    wait_msg(bot, _id, __send_call_resp, 'Введите сообщение для ответа.', rmvKb(), [bot, _id, user_id])
#\------------------------------------------------------------------/#
