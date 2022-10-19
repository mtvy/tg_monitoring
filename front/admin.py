#/==================================================================\#
# admin.py                                            (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from typing        import Any, Dict, List
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKb
from back.utility import saveText
#------------------------\ project modules /-------------------------#
from front.utility import get_date, set_kb, del_msg, send_msg, showFile, wait_msg
from back          import get_db, insert_db, logging
from front.vars    import *
from setup.vars    import CHNLS_FILE, mon_status
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
            if insert_db(f"INSERT INTO admins_tb (tid) VALUES ('{txt}')", 'admins_tb'):
                send_msg(bot, _id, A_ADMIN_ADD, set_kb(ADMIN_KB))
            else: # ????
                send_msg(bot, _id, A_ADMIN_WAS, set_kb(ADMIN_KB))
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

    send_msg(bot, _id, 'Получение данных...', rmvKb())
    data = get_db('bot_info_tb')
    for it in data if data else []: # | bot | status | last_req | ... | #
        send_msg(bot, _id, f'bot: {it[1]}\nstatus: {it[2]}\nlast_req: {it[3]}')
                               
    send_msg(bot, _id, 'Данные получены.', rmvKb())
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_chnls(bot : TeleBot, _id : str | int) -> None:
    data = get_db('chnls_tb') # | id | name | tid | num | #
    txt = f'Количество каналов: {len(data)}\n'
    for it in data:
        txt = f'{txt}{it[0]+1} {it[1]} {it[2]} {it[3]}\n'
    saveText(txt, CHNLS_FILE)
    showFile(bot, _id, CHNLS_FILE, 'Каналы', 'Ошибка получения.')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def push_mon(bot : TeleBot, _id : str | int) -> None:
    __MON_KB = ['Запуск по каналам', 'Отправка сообщения в канал']
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
def start_list_mon(bot : TeleBot, _id : str | int) -> None:
    global mon_status; mon_status = True

    __STOP_MON_KB = ['Остановить мониторинг', 'Отправка сообщения в канал']
    send_msg(bot, _id, 'Запущен мониториг по списку.', set_kb(__STOP_MON_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def stop_mon(bot : TeleBot, _id : str | int) -> None:
    global mon_status; mon_status = False

    __MON_KB = ['Запуск по каналам', 'Отправка сообщения в канал']
    send_msg(bot, _id, 'Мониторинг остановлен.', set_kb(__MON_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_msg_to_chnl(bot : TeleBot, _id : str | int) -> None:

    @logging()
    def __send_msg(msg : Message, bot : TeleBot, _id : str | int, chnl : str) -> None:
        global mon_status
        __mon_kb = ['Остановить мониторинг' \
            if mon_status else 'Запуск по каналам', 'Отправка сообщения в канал']

        chnls : Dict[str, str] = get_db('chnls_tb') # {name : tid}

        if chnl in chnls.keys():
            txt = msg.text
            _id = chnls[chnl]
        else:
            txt = 'Канал не найден.'

        send_msg(bot, _id, txt, set_kb(__mon_kb))
        

    @logging()
    def __send_msg_to_chnl(msg : Message, bot : TeleBot, _id : str | int) -> None:
        wait_msg(bot, _id, __send_msg, 'Введите сообщение.', rmvKb(), [bot, _id, msg.text])
        
    
    wait_msg(bot, _id, __send_msg_to_chnl, 'Введите название канала.', rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#
