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

admins_IDS = {'281321076'  : None} #get_ids('admins_tb')
users_IDS = {}  #get_ids('users_tb')

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

    KEYBOARD_FUNC = {...}
    ADMIN_FUNC = {
        'Уведомить'       : ...,
        'Добавить админа' : add_admin, 
        'Посмотреть LTV'  : get_session_info
    }

    _id = str(msg.chat.id)
    txt : str = msg.text

    if txt in KEYBOARD_FUNC:
        ...
    elif txt in ADMIN_FUNC:
        if _id in admins_IDS.keys():
            ADMIN_FUNC[txt](bot, _id)
        else:
            bot.send_message(_id, 'Нет прав администратора.', 
                reply_markup=rmvKey())
    
    admins_IDS = get_ids('admins_tb')
    users_IDS = get_ids('users_tb')
#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    if not proc_bot(bot):
        bot.polling(none_stop=True)
#\==================================================================/#
