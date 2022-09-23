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
#\------------------------------------------------------------------/#


USER_KB = ['Мониторинг', 'Соглашение', 'Тех. Поддержка', 
                     'Профиль', 'Рефералка'            ]

YN_KB = ['Да', 'Нет']

#\------------------------------------------------------------------/#
@logging()
def init_user(bot : TeleBot, _id : str) -> None:

   @logging()
   def is_ref(msg : Message, bot: TeleBot, _id: str) -> None:

      # ADD REF COLUMN INTO accs_tb!
      REF_FUNC = {
         'Да'     : [wait_msg, 'Пришлите номер реферала в формате 12345678.'],
         'Нет'    : [send_msg, 'Регистрация пройдена!'],
         '/stop'  : [send_msg, 'Регистрация пройдена! Реферал не добавлен.'],
         'nmbr'   : [send_msg, 'Регистрация пройдена! Реферал добавлен.'],
         'errVal' : [wait_msg, 'Пожалуйста, пришлите в формате 12345678 или нажмите /stop']
      }

      txt : str = msg.text if msg.text in REF_FUNC.keys() \
                     else 'nmbr' if msg.text.isdigit() \
                        else 'errVal'

      __kwrgs = {
         'bot'  : bot,
         '_id'  : _id, 
         'func' : is_ref, 
         'mrkp' : rmvKb() if REF_FUNC[txt][0] == wait_msg else set_kb(USER_KB), 
         'txt'  : REF_FUNC[txt][1],
         'args' : [bot, _id]
      }

      REF_FUNC[txt][0](**__kwrgs)


   txt = ('Вы вошли в аккаунт пользователя.\n'
          'Необходимо пройти регистрацию.')
   send_msg(bot, _id, txt, rmvKb())

   date = get_date()

   insert_db(f"INSERT INTO users_tb (tid) VALUES ('{_id}')", 'users_tb')
   insert_db(f"INSERT INTO accs_tb (tid, reg_date, entr_date, buys) VALUES ('{_id}', '{date}', '{date}', '{{}}')", 'accs_tb')

   wait_msg(bot, _id, is_ref, 'У вас есть рефералка?', set_kb(YN_KB), [bot, _id])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_refer(bot: TeleBot, _id: str) -> str:
   send_msg(bot, _id, f'Ваш реферал {_id}')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def start_user(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, f'Аккаунт пользователя #{_id}', set_kb(USER_KB))
#\------------------------------------------------------------------/#


MON_KB = ['Аторизация', 'Каналы', 'Настройка', 'Назад']

#\------------------------------------------------------------------/#
@logging()
def enter_monitoring(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, 'Настроки мониторинга.', set_kb(MON_KB))
#\------------------------------------------------------------------/#


CHNL_KB = ['Показать', 'Добавить', 'Удалить', 'Назад']

#\------------------------------------------------------------------/#
@logging()
def push_chnl(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, 'Настройки каналов.', set_kb(CHNL_KB))
#\------------------------------------------------------------------/#


PRFL_KB = ['Назад']

#\------------------------------------------------------------------/#
@logging()
def show_prfl(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, f'Профиль пользователя #{_id}\n...', set_kb(PRFL_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_ref(bot : TeleBot, _id : str) -> None:
   send_msg(bot, _id, f'Ваш реферал: {_id}')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def get_agrmnt(bot : TeleBot, _id : str) -> None:
   """### Send agreement to user. """
   send_msg(bot, _id, 'Соглашение: https://...')
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
      txt = f'Сообщение от @test_tim_bot\n{msg.text}'
      for admin_id in get_ids('admins_tb'):
         __send_call_req(bot, _user_id, admin_id, txt)
      send_msg(bot, _user_id, 'Сообщение в тех. поддержку отправлено.', set_kb(USER_KB))

   wait_msg(bot, _id, __proc_call_send, 'Ведите сообщение для тех. поддержки.', rmvKb(), [bot, _id])
#\------------------------------------------------------------------/#
