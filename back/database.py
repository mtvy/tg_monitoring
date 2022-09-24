#/==================================================================\#
# database.py                                         (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from sys          import argv as _dvars
from typing       import Any, Callable, List, Tuple
from json         import dump as _dump, load as _load
from psycopg2     import connect as connect_db
from progress.bar import IncrementalBar as _Bar

if __name__ == "__main__": 
    from utility import logging
else: 
    from back import logging
#\------------------------------------------------------------------/#


CONN_ADRGS = {
    'database' : 'mntr' ,
    'password' : 'mntr' ,
    'user'     : 'mntr' ,
    'host'     : 'localhost',
    'port'     : '5432'     
}

DBRESP = 'SELECT COUNT(1) FROM'

CR_ADMINS_TB = f'CREATE TABLE admins_tb(id serial primary key, tid VARCHAR(64), info TEXT[]); {DBRESP} admins_tb;'
CR_USERS_TB  = f'CREATE TABLE users_tb(id serial primary key, tid VARCHAR(64), info TEXT[]); {DBRESP} users_tb;'
CR_ACCS_TB   = f'CREATE TABLE accs_tb(id serial primary key, tid VARCHAR(64), reg_date VARCHAR(16), entr_date VARCHAR(16), buys TEXT[], ref ); {DBRESP} accs_tb;'

INS_TB = 'INSERT INTO _tb () VALUES '


#\------------------------------------------------------------------/#

def __connect() -> Tuple[Any, Any]:
    """This definition returns connection to database."""
    return connect_db(**CONN_ADRGS)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def push_msg(msg : str) -> Any | bool:
    """This definition sends message to database."""
    con = __connect(); cur = con.cursor()

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
def __dump_tables(_write : Callable[[str], None], _tb : str, _fl : str, **_) -> None:
    _dump(get_db(_tb), open(_fl, 'w')); _write(f'[DUMP][True]\n')
#\------------------------------------------------------------------/#    


#\------------------------------------------------------------------/#
def __load_tables(_write : Callable[[str], None], _tb : str, _fl : str, _) -> None:
    ...
#\------------------------------------------------------------------/# 


#\------------------------------------------------------------------/# 
def __cr_database(_write : Callable[[str], None], _db : str, _usr : str, _psswrd : str, **_) -> None:
    _write(f'[CR_DB_{_db}][{push_msg(f"CREATE DATABASE {_db};")}]')
    _write(f'[CR_USR_{_usr}][{push_msg(f"CREATE USER {_usr} WITH PASSWORD {_psswrd};")}]')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/# 
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
        '_db'     : CONN_ADRGS['database'], 
        '_usr'    : CONN_ADRGS['user'], 
        '_psswrd' : CONN_ADRGS['password'],
        '_tbs'    : ['users_tb', 'admins_tb', 'accs_tb'],
        '_fl'     : 'tb.json',
        '_ctbs'   : [CR_USERS_TB, CR_ADMINS_TB, CR_ACCS_TB]
    }

    for _dvar in _dvars: 
        if _dvar in DB_CNTRL: 
            DB_CNTRL[_dvar](**_args)
#\==================================================================/#