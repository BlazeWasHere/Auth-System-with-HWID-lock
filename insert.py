# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sqlite3
import datetime

# you can change name of the db
db = "auth.db"

def insert():
    """Just inserts a key and name 
    into the database if you are lazy
    to do manually.
    """
    try:
        #creates a connection to the db,
        #which you can change the name of
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        sqlite_insert_query = f"""INSERT INTO auth
                                (date, name, key) 
                                VALUES 
                                ('{utctime}', '{name}', '{key}') 
                               """
        #adds time, name and key into the database, leaves HWID null
        cursor.execute(sqlite_insert_query)
        connection.commit()
        print("Record inserted successfully ", cursor.rowcount)
        cursor.close()

    except sqlite3.IntegrityError as e:
        print(e)

if __name__ == '__main__':
    utctime = datetime.date.today()
    name = input("Name? ")
    key = input("Key? ")
    insert()
    print("DONE!")