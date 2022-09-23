from datetime      import datetime
from typing        import Any, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db, push_msg
from back.utility  import logging

from front.utility import get_date, set_keyboard


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

      #              ADD REF COLUMN INTO accs_tb!
      txt : str = msg.text
      if txt == 'Да':
         txt = 'Пришлите номер реферала в формате 12345678.'
         msg = bot.send_message(_id, txt, reply_markup=rmvKey())
         bot.register_next_step_handler(msg, is_ref, bot, _id)

      elif txt == 'Нет':
         #insert_db
         txt = 'Регистрация пройдена!'
         bot.send_message(_id, txt, reply_markup=set_keyboard(USER_KB))
         
      elif txt.isdigit():
         #insert_db
         txt = 'Регистрация пройдена! Реферал добавлен.'
         bot.send_message(_id, txt, reply_markup=set_keyboard(USER_KB))
      elif txt == '/stop':
         txt = 'Регистрация пройдена! Реферал не добавлен.'
         bot.send_message(_id, txt, reply_markup=set_keyboard(USER_KB))
      else:
         ms = bot.send_message(_id, 'Пожалуйста, пришлите в формате 123456789 или нажмите /stop')
         bot.register_next_step_handler(ms, is_ref, bot, _id)

   txt = (f'Вы вошли в аккаунт пользователя. Необходимо пройти регистрацию.')
   bot.send_message(_id, txt, reply_markup=rmvKey())

   date = get_date()

   insert_db(f"INSERT INTO users_tb (tid) VALUES ('{_id}')", 'users_tb')
   insert_db(f"INSERT INTO accs_tb (tid, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', '{{}}')", 'accs_tb')

   txt = ('У вас есть рефералка?')

   msg = bot.send_message(_id, txt, reply_markup=set_keyboard(['Да', 'Нет']))
   bot.register_next_step_handler(msg, is_ref, bot, _id)


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
