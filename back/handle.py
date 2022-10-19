#/==================================================================\#
# handling.py                                         (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from back.utility    import logging, \
                            saveLogs , \
                            rmvFile  , \
                            saveText
from front.utility   import send_msg, set_kb
from database        import get_db, insert_db
from setup.config    import MON_TOKEN
from traceback       import format_exc
from time            import sleep
from telebot         import TeleBot
from typing          import Callable, Tuple, List, Dict, Any
from multiprocessing import Process
from schedule        import every       as set_delay
from schedule        import run_pending as proc_run
from requests        import get         as get_req
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def init_proc(_func : Callable, _args) -> Process:
    return Process(target=_func, args=_args)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def start_proc(proc : Process) -> Process:
    proc.start(); return proc
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def kill_proc(proc : Process) -> Process:
    proc.kill(); return proc
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def start_handler(bot  : TeleBot, 
                  proc : Process, 
                  _id  : int, txt='Запрос мониторинга.') -> Process:

    keyboard = set_kb(['Остановить'])
    bot.send_message(_id, txt, reply_markup=keyboard)

    return start_proc(proc)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def kill_handler(bot  : TeleBot,
                 proc : Process, 
                 _id  : int, txt='Мониторинг отключен.') -> None:
    
    kill_proc(proc)
    key = set_kb(['Начать'])
    bot.send_message(_id, txt, reply_markup=key)
    del proc

    return None
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
_u_st = {'error' : False}
u_ids = []
def user_handle(_id  : int, ids : List[int]) -> None:
    global _u_st, u_ids

    def _send_req(bot : TeleBot, _id  : int, ctg  : List[str]) -> None:
        global _u_st, u_ids
        orgs = get_db('orgs_tb')

        file = f'U{_id}.txt'
        saveText(f'Добавлено: {len(orgs) - len(u_ids)}\n', file)
        bot.send_document(_id, open(file, 'rb'), caption='Добавлено')

        rmvFile(file)


    try:
        bot = TeleBot(MON_TOKEN)

        set_delay(60).seconds.do(_send_req, bot, _id, ...)

        send_msg(bot, _id, 'Мониторинг инициализирован.')
        
        while not _u_st['error']:
            proc_run()
            sleep(1)

        if _u_st['error']:
            send_msg(bot, _id, 'Ошибка мониторинга.')
        
    except:
        saveLogs(f"[run_pending]-->{format_exc()}")

    send_msg(bot, _id, 'Выход из мониторинга.')
#\------------------------------------------------------------------/#
