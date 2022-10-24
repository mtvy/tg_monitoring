#/==================================================================\#
# bot.py                                              (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from typing        import Any, Callable, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKb
#------------------------\ project modules /-------------------------#
from back  import *
from front import *
from front.vars import ADMIN_KB
from setup import *
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
bot = TeleBot(PAY_TOKEN)

__ADMIN_FUNC =  {'Уведомить'       : ask_accounts,
                 'Добавить админа' : add_admin, 
                 'Посмотреть LTV'  : get_session_info}
__USER_FUNC  =  {'Мониторинг'      : enter_monitoring,
                 'Соглашение'      : get_agrmnt,
                 'Тех. Поддержка'  : call_sup,
                 'Профиль'         : show_prfl,
                 'Рефералка'       : get_ref,
                 'Назад'           : start_user}
__MON_FUNC   =  {'Аторизация'      : ...,
                 'Каналы'          : push_chnl, 
                 'Настройка'       : ...}
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@logging()
def start(msg : Message) -> None:
    """### Bot begin actions """
    _id = str(msg.chat.id)

    if _id in get_ids('admins_tb').keys():
        init_admin(bot, _id, ADMIN_KB)
        
    elif _id not in get_ids('users_tb').keys():
        init_user(bot, _id)
    
    else:
        start_user(bot, _id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:

    @logging()
    def __proc_call(bot : TeleBot, 
                    _funcs : Dict[str, Callable], 
                    _id : str, 
                    ids : Dict[str, Any], 
                    txt : str, 
                    info : str) -> bool:
        _funcs[txt](bot, _id) if _id in ids.keys() \
            else send_msg(bot, _id, info, rmvKb())


    _id = str(msg.chat.id)
    txt : str = msg.text

    if txt in __USER_FUNC.keys():
        __proc_call(bot, __USER_FUNC, _id, get_ids('users_tb'), txt, U_NO_ACCESS)

    elif txt in __ADMIN_FUNC.keys():
        __proc_call(bot, __ADMIN_FUNC, _id, get_ids('admins_tb'), txt, A_NO_ACCESS)

    elif txt in ACC_TYPE.keys() and _id in get_ids('admins_tb').keys():
        send_info(bot, _id, get_ids(ACC_TYPE[txt]))
    
    elif txt in __MON_FUNC.keys() and _id in get_ids('users_tb').keys():
        __MON_FUNC[txt](bot, _id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.callback_query_handler(func=lambda call: True)
@logging()
def callback_inline(call):
    data   : str = call.data
    _id    : int = call.message.chat.id
    msg_id : int = call.message.message_id

    if data.isdigit():
        send_call_resp(bot, _id, data, msg_id)

#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    bot.polling(none_stop=True)
#\==================================================================/#
