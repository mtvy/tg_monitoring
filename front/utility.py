#/==================================================================\#
# utility.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from datetime      import datetime
from typing        import Callable, Dict, List
from telebot       import TeleBot
from telebot.types import KeyboardButton       as KbButton, \
                          ReplyKeyboardRemove  as rmvKb    , \
                          ReplyKeyboardMarkup  as replyKb   , \
                          InlineKeyboardMarkup as inlineKb   , \
                          InlineKeyboardButton as inlineButton
#------------------------\ project modules /-------------------------#
from back import get_db, logging
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def set_kb(btns : List[str]) -> replyKb:
    """
    Making keyboard
    """
    key = replyKb(resize_keyboard=True)
    key.add(*(KbButton(txt) for txt in btns))

    return key
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def set_inline_kb(btns : Dict[str, str]) -> None:
    """
    Making inline keyboard
    """
    key = inlineKb(row_width=2)
    key.add(*(inlineButton(txt, callback_data=btns[txt]) for txt in btns.keys()))

    return key
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def get_ids(tb : str) -> Dict[str, None]:
    ids = {}; data = get_db(tb)
    for it in data if data else []:
        ids[it[1]] = None
    return ids
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_date() -> str:
    now = datetime.now()
    return f'{now.year}-{now.month}-{now.day}'
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def del_msg(bot : TeleBot, sender_id : int, _msg_id : int) -> None:
    bot.delete_message(sender_id, _msg_id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def wait_msg(bot : TeleBot, _id : str, func : Callable, txt : str, mrkp : replyKb | inlineKb | rmvKb=None, args=[], **_) -> None:
    """
    Replacement for register_next_step_handler.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ```
    #Example 1:
        __kwrgs = {
            'bot'   : bot,
            '_id'   : _id, 
            'func'  : _call_func,     #_call_func(data, info)  
            'mrkp'  : set_kb(['Hi']), 
            'txt'   : 'Hello World!,
            'args'  : [data, info],
            ...
            ...
        }
    
        wait_msg(**__kwrgs)  
    
    #Example 2: 
        wait_msg(bot, _id, _call_func, txt, set_kb(['Hi']), [data, info])
    ```
    @note Other info at __kwrgs that does not use will comment at this func
    """
    msg = bot.send_message(_id, txt, reply_markup=mrkp)
    bot.register_next_step_handler(msg, func, *args)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_msg(bot : TeleBot, _id : str, txt : str, mrkp : replyKb | inlineKb | rmvKb=None, *args, **_) -> None:
    """
    Replacement for send_message.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ```
    #Example 1:
        __kwrgs = {
            'bot'  : bot,
            '_id'  : _id, 
            'func' : _call_func,     #_call_func(data, info)  
            'mrkp' : set_kb(['Hi']), 
            'txt'  : 'Hello World!,
            'args' : [data, info]
            ...
            ...
        }
    
        send_msg(**__kwrgs)  
    
    #Example 2: 
        send_msg(bot, _id, txt, set_kb(['Hi'])

    #Example 3: 
        send_msg(bot, _id, txt)
    ```
    """
    bot.send_message(_id, txt, reply_markup=mrkp)
#\------------------------------------------------------------------/#
