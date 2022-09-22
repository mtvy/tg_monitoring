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

from front.admin import *
from front.user  import *
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
    if _id in admins_IDS.keys():
        init_admin(bot, _id)
    elif _id not in users_IDS.keys():
        init_user(bot, _id)
        users_IDS = get_ids('users_tb')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:

    @logging()
    def _proc_call(ids : Dict[str, Any]) -> bool:
        if _id in ids.keys():
            USER_FUNC[txt](bot, _id)
        else:
            txt = 'Нет доступа. Перезапустите бота /start'
            bot.send_message(_id, txt, reply_markup=rmvKey())

        ...
        ...
        ...
        ...


    ADMIN_FUNC = {
        'Уведомить'       : ask_accounts,
        'Добавить админа' : add_admin, 
        'Посмотреть LTV'  : get_session_info,
        'Админы'          : ...,
        'Пользователи'    : ...
    }

    USER_FUNC = {
        'Мониторинг'     : ...,
        'Соглашение'     : ...,
        'Тех. Поддержка' : ...,
        'Профиль'        : ...,
        'Рефералка'      : get_refer
    }

    ACC_STATUS = {
        'Админ'        : 'admins_tb',
        'Пользователи' : 'users_tb'
    }

    _id = str(msg.chat.id)
    txt : str = msg.text

    if txt in USER_FUNC:
        if _id in users_IDS:
            USER_FUNC[txt](bot, _id)
        else:
            txt = 'Нет доступа. Перезапустите бота /start'
            bot.send_message(_id, txt, reply_markup=rmvKey())

    elif txt in ADMIN_FUNC:
        if _id in admins_IDS.keys():
            ADMIN_FUNC[txt](bot, _id)
        else:
            txt = 'Нет прав администратора.'
            bot.send_message(_id, txt, reply_markup=rmvKey())

    elif txt in ACC_STATUS.keys() and _id in admins_IDS.keys():
        send_info(bot, _id, get_ids(ACC_STATUS[txt]))
    
    admins_IDS, users_IDS = get_ids('admins_tb'), get_ids('users_tb')
#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    if not proc_bot(bot):
        bot.polling(none_stop=True)
#\==================================================================/#
