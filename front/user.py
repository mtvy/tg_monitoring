#/==================================================================\#
# user.py                                             (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove  as rmvKb   , \
                                   InlineKeyboardMarkup as inlineKb, \
                                   InlineKeyboardButton as inlineBtn
#------------------------\ project modules /-------------------------#
from back          import insert_db, logging
from front.utility import get_date, get_ids, set_kb, wait_msg, send_msg
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
   def __send_call_req(bot : TeleBot, _user_id : str, _admin_id : str, txt : str):

      #         ADD inline markup def 
      markup = inlineKb()
      markup.add(inlineBtn(text='Ответить', callback_data=_user_id))
      #...
      send_msg(bot, _admin_id, txt, markup)

   
   @logging()
   def __proc_call_send(msg : Message, bot : TeleBot, _user_id : str):
      txt = f'{A_SUP_MSG}test_tim_bot\n{msg.text}'
      for admin_id in get_ids('admins_tb'):
         __send_call_req(bot, _user_id, admin_id, txt)
      send_msg(bot, _user_id, U_SUP_SEND, set_kb(USER_KB))

   wait_msg(bot, _id, __proc_call_send, U_SUP_WRITE, rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#


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
      bot.send_message(_id, "У вас нет подписки. Желаете приобрести?")
      markup = set_kb(["Да, Нет"])
      msg = bot.send_message(_id, 'У вас есть ли купон?', reply_markup=rmvKb(markup))
      bot.register_next_step_handler(msg, get_sub)
      

@logging()
def get_sub(message: str, bot: TeleBot, _id: str):

   markup1 = set_kb(['Месяц - n $, 3 месяца - k $, год - m $'])
   markup2 = set_kb(['Месяц - n $, 3 месяца - k $, год - m $'])
   pay_methds = set_kb(['Сбер, Тинькофф, Qiwi'])

# покупка с купоном
   if message.text == 'Да':
      msg= bot.send_message(_id, 'Введите промо')
      bot.register_next_step_handler(msg, get_sub)
      
# покупка без купона
   elif message.text == 'Нет':
      msg = bot.send_message(_id, 'Тариф', reply_markup=markup2)
      bot.register_next_step_handler(msg, get_sub)

   elif message.text == 'Месяц - n $':
      """Процедура оплаты"""
      pass
      #bot.register_next_step_handler(msg, get_sub)

   elif message.text == '3 месяца - k $':
      pass
    # bot.register_next_step_handler(msg, get_sub)

   elif message.text == 'год - k $':
      """Процедура оплаты"""
      pass
      #bot.register_next_step_handler(msg, get_sub)
   
   #elif message.text.isdigit:
   """проверка купона"""
   # bot.send_message(_id, 'Тариф', reply_markup=markup1)
