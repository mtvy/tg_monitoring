#/==================================================================\#
# user.py                                             (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from curses.ascii import isdigit
from typing import List
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove  as rmvKb
#------------------------\ project modules /-------------------------#
from back          import insert_db, logging
from back.database import get_db, push_msg
from front.utility import get_date, get_ids, set_inline_kb, set_kb, wait_msg, send_msg
from front.vars    import *
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def init_user(bot : TeleBot, _id : str) -> None:

   @logging()
   def is_ref(msg : Message, bot: TeleBot, _id: str) -> None:

      # ADD REF COLUMN INTO accs_tb!

      txt : str = msg.text if msg.text in REF_FUNC.keys() \
                     else 'nmbr' if msg.text.isdigit() else 'errVal'

      __kwrgs = {
         'bot'  : bot,
         '_id'  : _id, 
         'func' : is_ref, 
         'mrkp' : rmvKb() if REF_FUNC[txt][0] == wait_msg else set_kb(USER_KB), 
         'txt'  : REF_FUNC[txt][1],
         'args' : [bot, _id]
      }

      REF_FUNC[txt][0](**__kwrgs)

   
   REF_FUNC = {'Да'     : [wait_msg, SEND_REF_NUM       ],
               'Нет'    : [send_msg, REG_DONE           ],
               '/stop'  : [send_msg, REG_DONE_NO_REF    ],
               'nmbr'   : [send_msg, REG_DONE_REF       ],
               'errVal' : [wait_msg, SEND_REF_WRONG_FORM]}

   send_msg(bot, _id, U_INIT_MSG, rmvKb())

   date = get_date()

   insert_db(f"INSERT INTO users_tb (tid) VALUES ('{_id}')", 'users_tb')
   insert_db(f"INSERT INTO accs_tb (tid, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', '{{}}')", 'accs_tb')

   wait_msg(bot, _id, is_ref, U_REF_ASK, set_kb(YN_KB), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def start_user(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, f'{U_ACC}{_id}', set_kb(USER_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def enter_monitoring(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, A_MON_SETUP, set_kb(MON_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def push_chnl(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, U_CHNL_SET, set_kb(CHNL_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def show_chnls(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, 'Получение каналов...', rmvKb())
   users = get_db('users_tb')
   if users:
      for it in users:
         if it[1] == _id:
            if it[2]:
               send_msg(bot, _id, f'Получено {len(it[2])}...')
               for chnl in it[2]:
                  send_msg(bot, _id, chnl)
               send_msg(bot, _id, f'Загрузка закончена.', set_kb(USER_KB))
               return
            else:
               send_msg(bot, _id, f'Вы не добавили каналы.', set_kb(USER_KB))
               return
      send_msg(bot, _id, f'Перезапустите бота /start')
   else:
      send_msg(bot, _id, f'Перезапустите бота /start')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def add_chnl(bot : TeleBot, _id : str) -> None:

   @logging()
   def __add_chnl(msg : Message, bot : TeleBot, _id : str) -> None:
      txt : str = msg.text
      if txt.isdigit():
         users = get_db('users_tb')
         for user in users:
            if _id == user[1]:
               if push_msg(f"UPDATE users_tb SET info = ARRAY{[txt] if not user[2] else user[2] + [txt]} WHERE tid = '{_id}'; SELECT COUNT(1) FROM users_tb"):
                  send_msg(bot, _id, f'{txt} добавлен.', set_kb(USER_KB))
               else:
                  send_msg(bot, _id, f'{txt} не добавлен.', set_kb(USER_KB))
      else:
         send_msg(bot, _id, f'[{txt}] не верный формат id.', set_kb(USER_KB))

               
   wait_msg(bot, _id, __add_chnl, 'Введите id канала. (123456789)', rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def rmv_chnl(bot : TeleBot, _id : str) -> None:

   @logging()
   def __rmv_chnl(msg : Message, bot : TeleBot, _id : str, chnls : List) -> None:
      txt : str = msg.text
      chnls = [chnl for chnl in chnls if chnl != txt]
      if txt.isdigit():
         if chnls:
            if push_msg(f"UPDATE users_tb SET info = ARRAY{chnls} WHERE tid = '{_id}'; SELECT COUNT(1) FROM users_tb"):
               send_msg(bot, _id, f'{txt} удалён.', set_kb(USER_KB))
         elif push_msg(f"UPDATE users_tb SET info = '{{}}' WHERE tid = '{_id}'; SELECT COUNT(1) FROM users_tb"):
               send_msg(bot, _id, f'{txt} удалён.', set_kb(USER_KB))
         else:
            send_msg(bot, _id, f'{txt} не удалён.', set_kb(USER_KB))
      else:
         send_msg(bot, _id, f'[{txt}] не верный формат id.', set_kb(USER_KB)) 

   send_msg(bot, _id, 'Получение каналов...', rmvKb())
   users = get_db('users_tb')
   for user in users if users else []:
      if user[1] == _id and user[2]:
         wait_msg(bot, _id, __rmv_chnl, 'Каналы получены. Какой удалить?', set_kb(user[2]), [bot, _id, user[2]])
         return
   send_msg(bot, _id, 'Каналы получены.', set_kb(USER_KB))   
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def show_prfl(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, f'{U_PRFL}{_id}\n...', set_kb(PRFL_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_ref(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, f'{U_REF}{_id}')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_agrmnt(bot : TeleBot, _id : str) -> None:
   """### Send agreement to user. """
   send_msg(bot, _id, U_AGR_MSG)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def call_sup(bot : TeleBot, _id : str) -> None:
   
   @logging()
   def __proc_call_send(msg : Message, bot : TeleBot, _user_id : str):
      txt = f'{A_SUP_MSG}{msg.chat.username}\n{msg.text}'
      for admin_id in get_ids('admins_tb'):
         send_msg(bot, admin_id, txt, set_inline_kb({'Ответить' : _user_id}))
      send_msg(bot, _user_id, U_SUP_SEND, set_kb(USER_KB))


   wait_msg(bot, _id, __proc_call_send, U_SUP_WRITE, rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def is_sub(_id : str, _tb : str) -> bool:
   return True # sub -> 2022-9-25 | False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def check_sub(bot : TeleBot, _id : str):

   @logging()
   def __get_sub(msg : Message, bot : TeleBot, _id : str):

      txt : str = msg.text

      if txt == 'Да':
         wait_msg(bot, _id, __get_sub, U_PROMO_ENTER, rmvKb(), [bot, _id])
         
      elif txt == 'Нет':
         wait_msg(bot, _id, __get_sub, 'Тариф', \
            set_kb(['Месяц - n $', '3 месяца - k $', 'год - m $']), [bot, _id])

      elif txt == 'Месяц - n $':
         ...

      elif txt == '3 месяца - k $':
         ...

      elif txt == 'год - k $':
         ...
      
      elif txt.isdigit():
         ...


   @logging()
   def __ask_sub(msg : Message, bot : TeleBot, _id : str):
      wait_msg(bot, _id, __get_sub, U_PROMO_ASK, set_kb(YN_KB), [bot, _id]) \
         if msg.text == 'Да' else start_user(bot, _id)

      
   if is_sub(_id, 'users_tb'):
      send_msg(bot, _id, 'Ваша подписка действует до 2023-1-1.')

   else:
      wait_msg(bot, _id, __ask_sub, 'У вас нет подписки. Желаете приобрести?', set_kb(YN_KB), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def auf_mon(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, 'Загрузка каналов...', rmvKb())
   users = get_db('users_tb'); chnls = []
   if users:
      for user in users:
         if _id == user[1]:
            chnls = user[2]
            break
      if chnls:
         for chnl in chnls:
            data = push_msg(f"SELECT * FROM chnls_tb WHERE tid = '{chnl}'")
            
            if data:
               data = data[0]
               if _id not in data[4]:
                  push_msg(f"UPDATE chnls_tb SET num = '{int(data[3]) + 1}', utids = ARRAY{[_id] if not data[4] else [_id] + data[4]}; SELECT COUNT(1) FROM chnls_tb")
            else:
               insert_db(f"INSERT INTO chnls_tb (tid, num, utids) VALUES ('{chnl}', '1', ARRAY{[_id]})", 'chnls_tb')
         send_msg(bot, _id, 'Каналы загружены.', set_kb(USER_KB))
         return


   send_msg(bot, _id, 'Презапустите бота /start', set_kb(USER_KB))
#\------------------------------------------------------------------/#

