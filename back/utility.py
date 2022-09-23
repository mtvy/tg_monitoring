#/==================================================================\#
# utility.py                                          (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
from io            import open       as _open
from os            import remove     as _rmv
from os.path       import exists     as _is_exist
from traceback     import format_exc as _exc
from datetime      import datetime   as dt
from json          import dump       as dump_json, \
                          load       as load_json
from typing        import Callable, Literal, Any
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def saveText(txt, _f, _md = 'a', _enc = 'utf-8') -> int:
    return open(file = _f, mode = _md, encoding = _enc).write(txt)
#\------------------------------------------------------------------/#

LOG_FILE = 'bot.txt'

#\------------------------------------------------------------------/#
def saveLogs(txt : str, _f : str = LOG_FILE) -> int:
    return saveText(f'\nDate: {dt.now()}\n\n{txt}', _f)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def logging(__write : Callable[[str], None]=print, __rtrn=False):
    """ Logging decorator with args. """
    
    def _logging(func : Callable) -> Any | Literal[False]:
        
        def wrap_func(*args, **kwargs) -> Any | Literal[False]:
            try:
                return func(*args, **kwargs)
            except:
                __write(f"[{func.__name__}]-->{_exc()}")
            return __rtrn

        return wrap_func
        
    return _logging
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def openfileforRead(file = None, txt = '') -> str:
    return txt.join([i for i in _open(file, encoding='utf-8')])
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def rmvFile(pth : str) -> bool:
    if _is_exist(pth): _rmv(pth); return True
    return False
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def dumpData(data : Any, _f : str, _md = 'w') -> None:
    dump_json(data, open(_f, _md))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def loadData(_f : str) -> Any:
    return load_json(open(_f))
#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    ...
#\==================================================================/#
