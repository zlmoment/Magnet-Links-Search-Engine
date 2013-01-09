# -*- coding: utf-8 -*-

from random import choice
from database import getConn

def import_object(name, arg=None):
    if '.' not in name:
        return __import__(name)
    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    return getattr(obj, parts[-1], arg)

def create_token(length=6):
    chars = ('0123456789'
             'abcdefghijklmnopqrstuvwxyz'
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    salt = ''.join([choice(chars) for i in range(length)])
    return salt

def createShortLink(maglink):
    short_link = create_token()
    conn = getConn()
    conn.query("""select short_url from mgnt_url where long_url='%s';""" % maglink)
    result = conn.store_result().fetch_row()
    if result == ():
        sql = """
              INSERT INTO `mgnt`.`mgnt_url` (`id` ,`short_url`, `long_url`, `ctime`) 
              VALUES (NULL ,'%s','%s', CURRENT_TIMESTAMP);
              """ % (short_link, maglink)
        conn.query(sql)
    else:
        short_link = result[0][0]
    return short_link