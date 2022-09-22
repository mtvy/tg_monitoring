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
def get_refer(bot: TeleBot, _id: str) -> str:
       bot.send_message(_id, f'Ваш реферал {_id}')
       