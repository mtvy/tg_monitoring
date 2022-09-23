from datetime      import datetime
from typing        import Any, Dict
from telebot       import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove as rmvKey

from back.database import get_db, insert_db, push_msg
from back.utility  import logging

from front.utility import get_date, get_ids, set_keyboard


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


CHNL_KB = ['Показать', 'Добавить', 'Удалить', 'Назад']

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


@logging()
def get_ref(bot : TeleBot, _id : str) -> None:
   bot.send_message(_id, f'Ваш реферал: {_id}')


@logging()
def get_agrmnt(bot : TeleBot, _id : str) -> None:
   """### Send agreement to user. """
   bot.send_message(_id, 'Соглашение: https://...')


@logging()
def call_sup(bot : TeleBot, _id : str) -> None:

   @logging()
   def __send_call_req(bot : TeleBot, _user_id : str, _admin_id : str, txt : str):

      #         ADD inline markup def 
      markup = InlineKeyboardMarkup()
      markup.add(InlineKeyboardButton(text='Ответить', callback_data=_user_id))
      #...
      bot.send_message(_admin_id, txt, reply_markup=markup)

   
   @logging()
   def __proc_call_send(msg : Message, bot : TeleBot, _user_id : str):
      txt = f'Сообщение от @test_tim_bot\n{msg.text}'
      for admin_id in get_ids('admins_tb'):
         __send_call_req(bot, _user_id, admin_id, txt)
      bot.send_message(_user_id, 'Сообщение в тех. поддержку отправлено.', reply_markup=set_keyboard(USER_KB))

   msg = bot.send_message(_id, 'Ведите сообщение для тех. поддержки.', reply_markup=rmvKey())
   bot.register_next_step_handler(msg, __proc_call_send, bot, _id)

