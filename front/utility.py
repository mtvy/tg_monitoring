#/==================================================================\#
# utility.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from datetime      import datetime
from typing        import Callable, Dict, List, Tuple
from telebot       import TeleBot
from telebot.types import KeyboardButton       as KbButton, \
                          ReplyKeyboardRemove  as rmvKb    , \
                          ReplyKeyboardMarkup  as replyKb   , \
                          InlineKeyboardMarkup as inlineKb
#------------------------\ project modules /-------------------------#
from back import get_db, logging
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def set_kb(btns : List[str]) -> replyKb:
    """
    Making keyboard
    """

    def __get_keyboard(resize=True) -> replyKb:
        return replyKb(resize_keyboard=resize)


    def __get_btn(txt : str) -> KbButton:
        return KbButton(txt)


    def __gen_btns(btns : List[str]) -> Tuple[KbButton]:
        return (__get_btn(txt) for txt in btns)


    key = __get_keyboard()
    key.add(*__gen_btns(btns))

    return key
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_ids(tb : str) -> Dict[str, None]:
    ids = {}
    for it in get_db(tb):
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
    msg = bot.send_message(_id, txt, reply_markup=mrkp)
    bot.register_next_step_handler(msg, func, *args)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def send_msg(bot : TeleBot, _id : str, txt : str, mrkp : replyKb | inlineKb | rmvKb=None, *args, **_) -> None:
    bot.send_message(_id, txt, reply_markup=mrkp)
#\------------------------------------------------------------------/#
