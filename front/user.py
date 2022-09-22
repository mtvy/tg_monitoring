from datetime      import datetime
from typing        import Any, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db, push_msg
from back.utility  import logging

from front.utility import set_keyboard


USER_KB = [
   'Мониторинг', 
   'Соглашение', 
   'Тех. Поддержка', 
   'Профиль', 
   'Рефералка'
]


@logging()
def init_user(msg : Message, bot : TeleBot, _id : str) -> None:

   @logging()
   def is_ref(msg : Message, bot: TeleBot, _id: str) -> None:
      if msg.text == 'Да':
         txt = 'Пришлите номер реферала в формате 123456789.'
         msg = bot.send_message(_id, txt)
         bot.register_next_step_handler(msg, is_ref, bot, _id)

      elif msg.text == 'Нет':
         insert_db()
         pass

      elif msg.text.isdigit():
         #insert_db
         pass

      else:
         ms = bot.send_message(_id, 'Пожалуйста, пришлите в формате 123456789')
         bot.register_next_step_handler(ms, is_ref)

   txt = (f'Вы вошли в аккаунт пользователя. Необходимо пройти регистрацию.')
   bot.send_message(_id, txt, reply_markup=rmvKey())

   now = datetime.now()
   date = f'{now.year}-{now.month}-{now.day}'
   insert_db(f"INSERT INTO users_tb (tib) VALUES ('{_id}')")
   insert_db(f"INSERT INTO accs_tb (tib, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', ''{''}'')")

   txt = ('У вас есть рефералка?')

   markup = set_keyboard(['Да', 'Нет'])
   msg = bot.send_message(_id, txt, reply_markup=rmvKey(markup))
   bot.register_next_step_handler(msg, is_ref, bot, _id)
    
   bot.send_message(_id, '', reply_markup=set_keyboard(USER_KB))



@logging()
def get_refer(bot: TeleBot, _id: str) -> str:
   bot.send_message(_id, f'Ваш реферал {_id}')


@logging()
def start_user(bot : TeleBot, _id : str) -> None:
   txt = f'Аккаунт пользователя #{_id}'
   bot.send_message(_id, txt, reply_markup=set_keyboard(USER_KB))


MON_KB = ['Аторизация', 'Каналы', 'Настройка', 'Назад']

@logging()
def enter_monitoring(bot : TeleBot, _id : str) -> None:
   txt = 'Настроки мониторинга.'
   bot.send_message(_id, txt, reply_markup=set_keyboard(MON_KB))


CHNL_KB = ['Показать', 'Добавить', 'Удалить']

@logging()
def push_chnl(bot : TeleBot, _id : str) -> None:
   txt = 'Настройки каналов.'
   bot.send_message(_id, txt, reply_markup=set_keyboard(CHNL_KB))


PRFL_KB = ['Назад']

@logging()
def show_prfl(bot : TeleBot, _id : str) -> None:
   txt = (f'Профиль пользователя #{_id}\n'
          f'...')
   bot.send_message(_id, txt, reply_markup=set_keyboard(PRFL_KB))
