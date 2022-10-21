#/==================================================================\#
# database.py                                         (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from sys          import argv as _dvars
from typing       import Any, Callable, Dict, List, Tuple
from json         import dump as _dump
from psycopg2     import connect as connect_db

if __name__ == "__main__": 
    from utility import logging
    from vars    import *
else: 
    from back import logging
    from back.vars import *
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __connect(conn_kwrgs=CONN_ADRGS) -> Tuple[Any, Any]:
    """This definition returns connection to database."""
    return connect_db(**conn_kwrgs)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def push_msg(msg : str, conn_kwrgs=CONN_ADRGS) -> Any | bool:
    """This definition sends message to database."""
    con = __connect(conn_kwrgs); cur = con.cursor()

    if con and cur:
        cur.execute(msg); con.commit()
        return cur.fetchall()

    return False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def get_db(_tb : str) -> List | bool:
    return push_msg(f'SELECT * FROM {_tb};')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def insert_db(msg : str, _tb : str) -> str | bool:
    return push_msg(f'{msg}; {DBRESP} {_tb}')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def delete_db(msg : str, _tb : str) -> str | bool:
    return push_msg(f'DELETE FROM {_tb} WHERE {msg}; {DBRESP} {_tb};')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __dump_tables(_write : Callable[[str], None], _tb : str, _fl : str, **_) -> None:
    _dump(get_db(_tb), open(_fl, 'w')); _write(f'[DUMP][True]\n')
#\------------------------------------------------------------------/#    


#\------------------------------------------------------------------/#
@logging()
def __load_tables(_write : Callable[[str], None], _tb : str, _fl : str, _) -> None:
    ...
#\------------------------------------------------------------------/# 


#\------------------------------------------------------------------/# 
@logging()
def __cr_database(_write : Callable[[str], None], _db : str, _usr : str, _psswrd : str, _p_con : Dict[str, str], **_) -> None:
    _write(f'[CR_DB_{_db}][{push_msg(f"CREATE DATABASE {_db}")}]', _p_con)
    _write(f'[CR_USR_{_usr}][{push_msg(f"CREATE USER {_usr} WITH ENCRYPTED PASSWORD {_psswrd}")}]', _p_con)
    _write(f'[GRANT_PRIVILEGES][{push_msg(f"GRANT ALL PRIVILEGES ON DATABASE {_db} TO {_usr}")}]', _p_con)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/# 
@logging()
def __cr_tables(_write : Callable[[str], None], _ctbs : str, **_) -> None:
    for _tb, ind in zip(_ctbs, range(len(_ctbs))): _write(f'[DB{ind+1}][{bool(push_msg(_tb))}]\n')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/# 
def __help_msg(_write : Callable[[str], None], **_) -> None:
    _write("-s Get database tables json                     \n"
           "-l Load tables into clear database (json needed)\n"
           "-d Create database                              \n"
           "-c Create database tables                       \n"
           "-h Get help message                             \n")
#\------------------------------------------------------------------/# 


#\==================================================================/#
if __name__ == "__main__":
   
    DB_CNTRL = {
        '-s' : __dump_tables,
        '-l' : __load_tables,
        '-d' : __cr_database,
        '-c' : __cr_tables,
        '-h' : __help_msg
    }

    _args = {
        '_write'  : print,
        '_p_con'  : {'database' : 'postgres' , 
                     'user'     : 'postgres' , 
                     'password' : 'postgres' ,
                     'host'     : 'localhost',
                     'port'     : '5432'     },
        '_db'     : CONN_ADRGS['database'], 
        '_usr'    : CONN_ADRGS['user'], 
        '_psswrd' : CONN_ADRGS['password'],
        '_tbs'    : ['users_tb', 'admins_tb', 'accs_tb', 'chnls_tb', 'bot_info_tb'],
        '_fl'     : 'tb.json',
        '_ctbs'   : [CR_USERS_TB, CR_ADMINS_TB, CR_ACCS_TB, CR_CHNLS_TB, CR_BOT_INFO_TB]
    }

    for _dvar in _dvars: 
        if _dvar in DB_CNTRL: 
            DB_CNTRL[_dvar](**_args)
#\==================================================================/#