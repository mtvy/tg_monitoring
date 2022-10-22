#/==================================================================\#
# admin.py                                            (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from typing        import Any, Dict, List, Literal
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKb
from back.database import push_msg
from back.utility import saveText
#------------------------\ project modules /-------------------------#
from front.utility import get_date, set_kb, del_msg, send_msg, showFile, wait_msg
from back          import get_db, insert_db, logging
from front.vars    import *
from setup.vars    import CHNLS_FILE
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __is_exist(_id : str) -> bool:
    for it in get_db('accs_tb'):
        if it[1] == _id:
            return True
    return False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def init_admin(bot : TeleBot, _id : str, kb : List[str]) -> None:

    send_msg(bot, _id, A_INIT_MSG, rmvKb())
    
    date = get_date()

    if not __is_exist(_id):
        insert_db(f"INSERT INTO accs_tb (tid, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', '{{}}')", 'accs_tb')
    else:
        insert_db(f"UPDATE accs_tb SET entr_date='{date}' WHERE tid='{_id}'", 'accs_tb')

    send_msg(bot, _id, A_LOAD_DONE, set_kb(kb))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def add_admin(bot : TeleBot, _id : str) -> None:

    @logging()
    def __add_admin(msg : Message, bot : TeleBot, _id : str):
        txt : str = msg.text
        if txt.isdigit():
            if push_msg(f"DELETE FROM users_tb WHERE tid='{txt}'; SELECT COUNT(1) FROM users_tb") and \
                    insert_db(f"INSERT INTO admins_tb (tid) VALUES ('{txt}')", 'admins_tb'):
                send_msg(bot, _id, A_ADMIN_ADD, set_kb(ADMIN_KB))
            else: # ????
                send_msg(bot, _id, 'Ошибка.', set_kb(ADMIN_KB))
        else:
            send_msg(bot, _id, A_WRONG_ID_FRMT, set_kb(ADMIN_KB))

    wait_msg(bot, _id, __add_admin, A_ADMIN_ID, rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_session_info(bot : TeleBot, _id : str) -> None:

    send_msg(bot, _id, A_STATS_GET, rmvKb())

    accs = get_db('accs_tb'); info = {'users' : 0, 'buys' : 0}
    date = get_date()

    for acc in accs:
        if acc[3] == date:
            info['users'] += 1
    
    send_msg(bot, _id, f'{A_USERS}{info["users"]}\nПокупок: {info["buys"]}')
    send_msg(bot, _id, A_ADDED_STATS, set_kb(ADMIN_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def ask_accounts(bot : TeleBot, _id : str) -> None:
    send_msg(bot, _id, A_ASK_MSG_SEND, set_kb(ACCS_TYPE_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_info(bot : TeleBot, _id : str, accs : Dict[str, Any]) -> None:
    
    @logging()
    def __send_info(msg : Message, bot: TeleBot, accs : Dict[str, Any]) -> None:
        for acc in accs.keys():
            send_msg(bot, acc, msg.text)
        send_msg(bot, msg.chat.id, f'{A_NOTIF_SEND}{len(accs)}', set_kb(ADMIN_KB))

    wait_msg(bot, _id, __send_info, A_ENTER_RESP_MSG, rmvKb(), [bot, accs])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_call_resp(bot : TeleBot, _id : int, user_id : str, msg_id : int) -> None:

    @logging()
    def __send_call_resp(msg : Message, bot : TeleBot, _id : int, _user_id : str) -> None:
        send_msg(bot, _user_id, f'{A_SUP}\n{msg.text}\n')
        send_msg(bot, _id, f'{A_SUP_MSG}test_tim_bot', set_kb(ADMIN_KB))


    del_msg(_id, msg_id)
    wait_msg(bot, _id, __send_call_resp, A_RESP_MSG, rmvKb(), [bot, _id, user_id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_bot_status(bot : TeleBot, _id : str | int) -> None:
    __KB = ['Статус', 'Список', 'Мониторинг', 'Конфиг']

    @logging()
    def __insert_bot(msg : Message, bot : TeleBot, _id : str | int) -> None:
        txt : str = msg.text
        if txt == 'Да':
            wait_msg(bot, _id, __insert_bot, 'Введите id бота. (12345678)', rmvKb(), [bot, _id])
        elif txt.isdigit():
            if insert_db(f"INSERT INTO bot_info_tb (bot, status, entr_date) VALUES ('{txt}', 'active', '{get_date()}')", 'bot_info_tb'):
                send_msg(bot, _id, 'Бот добавлен.', set_kb(__KB))
            else: 
                send_msg(bot, _id, 'Бот не добавлен.', set_kb(__KB))
        else:
                send_msg(bot, _id, 'Бот не добавлен.', set_kb(__KB))
            


    send_msg(bot, _id, 'Получение данных...', rmvKb())
    data = get_db('bot_info_tb')
    if data:
        for it in data: # | bot | status | last_req | ... | #
            send_msg(bot, _id, f'Bot: {it[0]}\nСтатус: {it[1]}\nПоследний запрос: {it[3]}\nДата регистрации: {it[2]}')
        send_msg(bot, _id, 'Данные получены.', set_kb(__KB))
    else:
        wait_msg(bot, _id, __insert_bot, 'В БД не добавлено ботов. Добавить?', set_kb(['Да','Нет']), [bot, _id])
                               
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_chnls(bot : TeleBot, _id : str | int) -> None:
    send_msg(bot, _id, 'Получение списка каналов...', rmvKb())
    data = get_db('chnls_tb') # | id | name | tid | num | utids | #
    txt = f'Количество каналов: {len(data)}\n'
    if data:
        for it in data:
            txt = f'{txt}{it[0]} {it[1]} {it[2]} {it[3]}\n'
        saveText(txt, CHNLS_FILE, 'w')
        showFile(bot, _id, CHNLS_FILE, 'Каналы', 'Ошибка получения.')
        send_msg(bot, _id, 'Загрузка закончена.', set_kb(['Статус', 'Список', 'Мониторинг', 'Конфиг']))
    else:
        send_msg(bot, _id, 'Каналы не добавлены.', set_kb(['Статус', 'Список', 'Мониторинг', 'Конфиг']))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def push_mon(bot : TeleBot, _id : str | int, _status : bool) -> None:
    __MON_KB = ['Остановить мониторинг' if _status else 'Запуск по каналам', 'Отправка сообщения в канал', 'Назад']
    send_msg(bot, _id, 'Мониторинг.', set_kb(__MON_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def set_conf(bot : TeleBot, _id : str | int) -> None:
    __CONF_KB = ['Проверка канала', 'Добавление бота', 'Статус']
    send_msg(bot, _id, 'Конфигурирование.', set_kb(__CONF_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def start_list_mon(bot : TeleBot, _id : str | int) -> Literal[True]:
    __STOP_MON_KB = ['Остановить мониторинг', 'Отправка сообщения в канал', 'Назад']
    send_msg(bot, _id, 'Запущен мониториг по списку.', set_kb(__STOP_MON_KB))
    return True
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def stop_mon(bot : TeleBot, _id : str | int) -> Literal[False]:
    __MON_KB = ['Запуск по каналам', 'Отправка сообщения в канал', 'Назад']
    send_msg(bot, _id, 'Мониторинг остановлен.', set_kb(__MON_KB))
    return False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_msg_to_chnl(bot : TeleBot, _id : str | int) -> None:
    __KB = ['Статус', 'Список', 'Мониторинг', 'Конфиг']

    @logging()
    def __send_msg(msg : Message, bot : TeleBot, _id : str | int, chnl : str) -> None:

        chnls : Dict[str, str] = [it[2] for it in get_db('chnls_tb')] # {name : tid}

        if chnl in chnls:
            data = send_msg(bot, chnl, msg.text)
            if data:
                send_msg(bot, _id, 'Сообение отправлено.', set_kb(__KB))
            else:
                send_msg(bot, _id, 'Сообение не отправлено.', set_kb(__KB))

        else:
            send_msg(bot, _id, 'Канал не найден.', set_kb(__KB))



    @logging()
    def __send_msg_to_chnl(msg : Message, bot : TeleBot, _id : str | int) -> None:
        txt : str = msg.text
        if txt.isdigit():
            wait_msg(bot, _id, __send_msg, 'Введите сообщение.', rmvKb(), [bot, _id, txt])
        else:
            send_msg(bot, _id, 'Неправильный формат id.', set_kb(__KB))
    
    wait_msg(bot, _id, __send_msg_to_chnl, 'Введите id канала. (123456789)', rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_new_msg(bot : TeleBot, gid : str, msg : Message) -> None:
    # | id | name | tid | num | utids | #
    ids = []; txt : str = f'Группа: {gid}\n{msg.text}'
    for group in get_db('chnls_tb'):
        if group[2] == gid:
            ids = group[4]
    
    for _id in ids:
        send_msg(bot, _id, txt)
#\------------------------------------------------------------------/#
