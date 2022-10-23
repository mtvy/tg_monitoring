#/==================================================================\#
# bot.py                                              (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/------------------------/ installed libs \------------------------\#
from typing        import Any, Callable, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKb
#--------------------------\ project files /-------------------------#
from back  import *
from front import *
from setup import *
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
bot = TeleBot(MON_TOKEN)

__ADMIN_FUNC = {'Статус'                     : get_bot_status,
                'Список'                     : get_chnls,
                'Мониторинг'                 : push_mon,
                'Конфиг'                     : set_conf}
__MON_FUNC   = {'Запуск по каналам'          : start_list_mon, 
                'Остановить мониторинг'      : stop_mon,
                'Отправка сообщения в канал' : send_msg_to_chnl}

MON_ADMIN_KB = ['Статус', 'Список', 'Мониторинг', 'Конфиг']

mon_status = False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@logging()
def start(msg : Message) -> None:
    """### Bot begin actions """
    _id = str(msg.chat.id)

    if _id in get_ids('admins_tb').keys():
        init_admin(bot, _id, MON_ADMIN_KB)
    else:
        send_msg(bot, _id, 'Нет доступа.', rmvKb())
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:
    global mon_status

    @logging()
    def __proc_call(bot : TeleBot, 
                    defs : Dict[str, Callable], 
                    _id : str, 
                    ids : Dict[str, Any], 
                    txt : str, 
                    info : str) -> bool:
        return defs[txt](bot, _id) if _id in ids.keys() \
            else send_msg(bot, _id, info, rmvKb())

 
    _id = str(msg.chat.id)
    txt : str = msg.text

    if mon_status and _id in (it[2] for it in get_db('chnls_tb')):
        send_new_msg(TeleBot(PAY_TOKEN), _id, msg)
    elif txt == 'Мониторинг' and _id in get_ids('admins_tb').keys():
        push_mon(bot, _id, mon_status)
    elif txt in __ADMIN_FUNC.keys():
        __proc_call(bot, __ADMIN_FUNC, _id, get_ids('admins_tb'), txt, A_NO_ACCESS) 
    elif txt in __MON_FUNC.keys():
        mon_status = __proc_call(bot, __MON_FUNC, _id, get_ids('admins_tb'), txt, A_NO_ACCESS)
    elif txt == 'Назад' and _id in get_ids('admins_tb').keys():
        send_msg(bot, _id, 'Главное меню.', set_kb(MON_ADMIN_KB))
#\------------------------------------------------------------------/#
 

#\==================================================================/#
if __name__ == "__main__":
    if DEBUG or not proc_bot(bot):
        bot.polling(none_stop=True)
#\==================================================================/#
