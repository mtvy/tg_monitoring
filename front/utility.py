
from typing        import Dict, List, Tuple
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from back.database import get_db
from back.utility import logging

def set_keyboard(btns : List[str]) -> ReplyKeyboardMarkup:
    """
    Making keyboard
    """

    def __get_keyboard(resize=True) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=resize)


    def __get_btn(txt : str) -> KeyboardButton:
        return KeyboardButton(txt)


    def __gen_btns(btns : List[str]) -> Tuple[KeyboardButton]:
        return (__get_btn(txt) for txt in btns)


    key = __get_keyboard()
    key.add(*__gen_btns(btns))

    return key


@logging()
def get_ids(tb : str) -> Dict[str, None]:
    ids = {}
    for it in get_db(tb):
        ids += {it[1] : None}
    return ids
