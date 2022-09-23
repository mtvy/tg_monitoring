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

from back.utility import logging
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
@logging()
def __connect() -> Tuple[Any, Any]:
    """This definition returns connection to database."""
    return connect_db(**CONN_ADRGS)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
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
def delete_db(_tb : str, msg : str) -> str | bool:
    return push_msg(f'DELETE FROM {_tb} WHERE {msg}; {DBRESP} orgs_tb;')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __test_database(_write : Callable[[str], None], _tb : str, _tst : str, **_) -> None:
    
    TEST_INSERT = ...

    test = bool(insert_db(TEST_INSERT, _tb))
    _write(f'[DB_INSERT] [{test}] <- insert_db({TEST_INSERT})\n\n')

    test = bool(get_db(_tb))
    _write(f'[DB_GET]    [{test}] <- get_db({_tb})\n\n')

    test = bool(delete_db(_tb, _tst))
    _write(f'[DB_DELETE] [{test}]   <- delete_db({_tb}, {_tst})\n\n')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def __dump_tables(_write : Callable[[str], None], _tb : str, _fl : str, **_) -> None:
    _dump(get_db(_tb), open(_fl, 'w')); _write(f'[DUMP][True]\n')
#\------------------------------------------------------------------/#    


#\------------------------------------------------------------------/#
@logging()
def __load_tables(_write : Callable[[str], None], _tb : str, _fl : str, _) -> None:

    orgs : List[List[str | Any]] = _load(open(_fl))

    bar = _Bar('Loading', max=len(orgs))

    for org in orgs: 
        bar.next(); brt = "'"

        txt = f" {INS_TB} '{org[1]}'          , " \
              f"'{org[2].replace(brt, brt*2)}', " \
              f"'{org[3].replace(brt, brt*2)}', ARRAY {org[4]}, " \
              f"'{org[5].replace(brt, brt*2)}', ARRAY {org[6]}, " \
              f"'{org[7]}', ARRAY {org[8]}); {DBRESP} {_tb};    "
              
        if not insert_db(txt, _tb): 
            _write('[LOAD][False]\n'); return
        
        txt = f'{INS_TB} \'{org[1]}\'); {DBRESP} {_tb};'

        if not insert_db(txt, _tb):
            _write('[LOAD][False]\n'); return
            
    bar.finish(); _write(f'[LOAD][True]')
#\------------------------------------------------------------------/# 


#\------------------------------------------------------------------/# 
@logging()
def __cr_database(_write : Callable[[str], None], _db : str, _usr : str, _psswrd : str, **_) -> None:
    _write(f'[CR_DB_{_db}][{push_msg(f"CREATE DATABASE {_db};")}]')
    _write(f'[CR_USR_{_usr}][{push_msg(f"CREATE USER {_usr} WITH PASSWORD {_psswrd};")}]')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/# 
@logging()
def __cr_tables(_write : Callable[[str], None], _ctbs : str, **_) -> None:
    for _tb, ind in zip(_ctbs, range(len(_ctbs))): _write(f'[DB{ind+1}][{bool(push_msg(_tb))}]\n')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/# 
def __help_msg(_write : Callable[[str], None], **_) -> None:
    _write("-t Database testing                             \n"
           "-s Get database tables json                     \n"
           "-l Load tables into clear database (json needed)\n"
           "-c Create database tables                       \n"
           "-h Get help message                             \n")
#\------------------------------------------------------------------/# 


#\==================================================================/#
if __name__ == "__main__":
   
    DB_CNTRL = {
        '-t' : __test_database,
        '-s' : __dump_tables,
        '-l' : __load_tables,
        '-d' : __cr_database,
        '-c' : __cr_tables,
        '-h' : __help_msg
    }

    _args = {
        '_write'  : print,
        '_db'     : 'mntr', 
        '_usr'    : 'mntr', 
        '_psswrd' : 'mntr',
        '_tbs'    : ['users_tb', 'admins_tb', 'accs_tb'],
        '_tst'    : '',
        '_fl'     : 'tb.json',
        '_ctbs'   : [CR_USERS_TB, CR_ADMINS_TB, CR_ACCS_TB]
    }

    for _dvar in _dvars: 
        if _dvar in DB_CNTRL: 
            DB_CNTRL[_dvar](**_args)
#\==================================================================/#