#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import psycopg2
import traceback
from datetime import datetime
from dbfread import DBF
from config.config import configs
typemap = {
    'F': 'FLOAT',
    'L': 'BOOLEAN',
    'I': 'INTEGER',
    'C': 'TEXT',
    'N': 'REAL',  # because it can be integer or float
    'M': 'TEXT',
    'D': 'DATE',
    'T': 'DATETIME',
    '0': 'INTEGER',
}


def add_table(cursor, table):
    """Add a dbase table to an open sqlite database."""

    cursor.execute('drop table if exists "{}"'.format(table.name))

    field_types = {}
    for field in table.fields:
        field_types[field.name] = typemap.get(field.type, 'TEXT')

    #
    # Create the table
    #
    defs = ', '.join(['"{}" {}'.format(f, field_types[f])
                      for f in table.field_names])
    sql = 'create table "{}" ({})'.format(table.name, defs)
    cursor.execute(sql)

    # Create data rows
    refs = ', '.join([field for field in table.field_names])
    list_in_parens = lambda l: "(%s)" % str(l).strip('[]')
    for rec in table:
        sql = 'insert into "{}" ({}) values {}'.format(table.name,refs ,list_in_parens(list(rec.values())))
        cursor.execute(sql)
    
def main(file_path,db_driver):
    print(db_driver)
    if db_driver in configs:
        db_data = configs[db_driver]
    start = datetime.now()
    conn = psycopg2.connect(host=db_data['host'], port = db_data['port'], database=db_data['db'], user=db_data['user'], password=db_data['pass'])
    # cursor = conn.cursor()

    # try:
    #     add_table(cursor, DBF(file_path,lowernames=True))
    # except UnicodeDecodeError:
    #     traceback.print_exc()
    #     sys.exit('Please use --encoding or --char-decode-errors.')

    # conn.commit()
    print(datetime.now() - start)
    