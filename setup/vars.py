from os.path import join as join_f

mon_status = False

CHNLS_FILE = join_f('data', 'chnls.txt')

ACC_TYPE =  {'Админы'          : 'admins_tb',
             'Пользователи'    : 'users_tb'}

U_NO_ACCESS = 'Нет доступа. Перезапустите бота /start'
A_NO_ACCESS = 'Нет прав администратора.'
