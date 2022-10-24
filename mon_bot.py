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

__ADMIN_FUNC = {'Статус'     : get_bot_status,
                'Список'     : get_chnls,
                'Мониторинг' : push_mon,
                'Конфиг'     : set_conf}
__CONF_FUNC  = {'Проверка канала' : check_chnl,
                'Добавление бота' : add_bot,
                'Статус'          : get_bot_status}


#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@logging()
def start(msg : Message) -> None:
    """### Bot begin actions """
    _id = str(msg.chat.id)

    if _id in get_ids('admins_tb').keys():
        init_admin(bot, _id, ['Статус', 'Список', 'Мониторинг', 'Конфиг'])
    else:
        send_msg(bot, _id, 'Нет доступа.', rmvKb())
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:

    @logging()
    def __proc_call(bot : TeleBot, 
                    defs : Dict[str, Callable], 
                    _id : str, 
                    ids : Dict[str, Any], 
                    txt : str, 
                    info : str) -> bool:
        defs[txt](bot, _id) if _id in ids.keys() \
            else send_msg(bot, _id, info, rmvKb())


    _id = str(msg.chat.id)
    txt : str = msg.text

    if txt in __ADMIN_FUNC.keys():
        __proc_call(bot, __ADMIN_FUNC, _id, get_ids('admins_tb'), txt, A_NO_ACCESS) 
    elif txt in __CONF_FUNC.keys():
        __proc_call(bot, __CONF_FUNC, _id, get_ids('admins_tb'), txt, A_NO_ACCESS)
#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    bot.polling(none_stop=True)
#\==================================================================/#
