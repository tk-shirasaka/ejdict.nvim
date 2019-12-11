from os import path
from sqlite3 import connect


def get_root():
    ret = __file__
    for x in range(4):
        ret = path.dirname(ret)

    return ret


def ejdict_path():
    return path.join(get_root(), 'ejdic-hand-sqlite', 'ejdict.sqlite3')


def ejdict_connect():
    return connect(ejdict_path())
