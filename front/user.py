#/==================================================================\#
# user.py                                             (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove  as rmvKb
#------------------------\ project modules /-------------------------#
from back          import insert_db, logging
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
      txt = f'{A_SUP_MSG}test_tim_bot\n{msg.text}'
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

