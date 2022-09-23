#/==================================================================\#
# bot.py                                              (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/------------------------/ installed libs \------------------------\#
from telebot         import TeleBot
from telebot.types   import Message
#--------------------------\ project files /-------------------------#
from back.webhook  import proc_bot        
from back.utility  import logging
from back.database import *

from front.admin   import *
from front.user    import *
from front.utility import get_ids
#\------------------------------------------------------------------/#

TOKEN = '5361529726:AAHkDG9SoOJUA_1F9rWnIjTXkxW_kpq4vQg'

#\------------------------------------------------------------------/#
bot = TeleBot(TOKEN)
#\------------------------------------------------------------------/#

admins_IDS : Dict[str, Any] = get_ids('admins_tb')
users_IDS : Dict[str, Any] = get_ids('users_tb')

#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@logging()
def start(msg : Message) -> None:
    """### Bot begin actions """
    _id = str(msg.chat.id)

    if _id in get_ids('admins_tb').keys():
        init_admin(bot, _id)
        
    elif _id not in get_ids('users_tb').keys():
        init_user(msg, bot, _id)
    
    else:
        start_user(bot, _id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:

    @logging()
    def __proc_call(bot : TeleBot, _funcs : Dict[str, Callable], _id : str, ids : Dict[str, Any], txt : str, info : str) -> bool:
        if _id in ids.keys():
            _funcs[txt](bot, _id)
        else:
            bot.send_message(_id, info, reply_markup=rmvKey())


    ADMIN_FUNC = {
        'Уведомить'       : ask_accounts,
        'Добавить админа' : add_admin, 
        'Посмотреть LTV'  : get_session_info
    }

    USER_FUNC = {
        'Мониторинг'     : enter_monitoring,
        'Соглашение'     : get_agrmnt,
        'Тех. Поддержка' : call_sup,
        'Профиль'        : show_prfl,
        'Рефералка'      : get_ref,
        'Назад'          : start_user
    }

    MON_FUNC = {
        'Аторизация' : ...,
        'Каналы'     : push_chnl, 
        'Настройка'  : ..., 
    }

    ACC_STATUS = {
        'Админ'        : 'admins_tb',
        'Пользователи' : 'users_tb'
    }

    _id = str(msg.chat.id)
    txt : str = msg.text

    if txt in USER_FUNC.keys():
        __proc_call(bot, USER_FUNC, _id, get_ids('users_tb'), txt,
            'Нет доступа. Перезапустите бота /start')

    elif txt in ADMIN_FUNC.keys():
        __proc_call(bot, ADMIN_FUNC, _id, get_ids('admins_tb'), txt,
            'Нет прав администратора.')

    elif txt in ACC_STATUS.keys() and _id in get_ids('admins_tb').keys():
        send_info(bot, _id, get_ids(ACC_STATUS[txt]))
    
    elif txt in MON_FUNC.keys() and _id in get_ids('users_tb').keys():
        MON_FUNC[txt](bot, _id)
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
    #if not proc_bot(bot):
    bot.polling(none_stop=True)
#\==================================================================/#
