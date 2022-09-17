
from typing        import List, Tuple
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

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
