from datetime      import datetime
from telebot       import TeleBot
from telebot.types import ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db
from back.utility  import logging

from front.utility import set_keyboard
from telebot import types

USER_KB = ['']


@logging()
def init_user(bot : TeleBot, _id : str) -> None:
   txt = ('У вас есть рефералка?')
   markup = set_keyboard(['Да', 'Нет'])
   msg = bot.send_message(_id, txt, reply_markup=rmvKey(markup))
   bot.register_next_step_handler(msg, is_ref)

   now = datetime.now()
   date = f'{now.year}-{now.month}-{now.day}'
   #insert_db('INSERT INTO users_tb...')
   #insert_db('INSERT INTO accs_tb...')
    
   bot.send_message(_id, '', reply_markup=set_keyboard(USER_KB))

@logging()
def is_ref(message:str, bot: TeleBot, _id: str):
   if message.text == 'Да':
      msg = bot.send_message(_id,"Пришлите номер реферала в формате 123456789")
      bot.register_next_step_handler(msg, is_ref)
   elif message.text == 'Нет':
      #insert_db
      pass
   elif msg.text.isdigit:
      #insert_db
      pass
   else:
      ms = bot.send_message(_id, "Пожалуйста, пришлите в формате 123456789")
      bot.register_next_step_handler(ms, is_ref)


@logging()
def get_ref(bot: TeleBot, _id: str) -> None:
   bot.send_message(_id, f'Ваш реферал: {_id}')


@logging()
def get_agrmnt(bot: TeleBot, _id: str) -> None:
   """### Send agreement to user. """
   bot.send_message(_id, 'Соглашение: https://...')


@logging()
def get_sub_info(_id : str, _tb : str) -> bool:
   return True


@logging()
def check_sub(bot: TeleBot, _id: str):
   if get_sub_info(_id, 'users_tb'):
      """если есть подписка выводит """
      #insert_db
      #bot.send_message(_id, "Ваша подписка действует до {#}")

   elif not get_sub_info(_id, 'users_tb'):
      """если ее нет"""
      bot.send_message(_id, "У вас нет подписки")
      markup = set_keyboard(["На месяц - n $", "3 месяца - n $", "Год - n $"])
      bot.send_message(_id, 'Выберите тариф', reply_markup=rmvKey(markup))

      