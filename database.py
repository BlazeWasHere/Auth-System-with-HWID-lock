import sqlite3
import datetime

connection = sqlite3.connect("auth.db")
cursor = connection.cursor()
print("Connected")
utctime = datetime.date.today()
key = "POSTIFY-81R35-Z7S37-H4LA1-LBDGJ"
hwid = "est"


def check_hwid():
    sqlite_check_hwid = f"""SELECT HWID FROM auth
                       WHERE HWID = '{hwid}'
                     """
    for row in cursor.execute(sqlite_check_hwid):
        connection.commit()
        hwid_search = row[0]
        break
    else:
        hwid_search = 0 

    return hwid_search

def check_key():
    sqlite_check_key = f"""SELECT KEY FROM auth
                       WHERE KEY = '{key}'
                    """
    for row in cursor.execute(sqlite_check_key):
        connection.commit()
        key_search = row[0]
        break
    else:
        key_search = 0 

    return key_search

def check_name():
    sqlite_check_name = f"""SELECT NAME FROM auth 
                        WHERE KEY = '{key}';
                        """
    for row in cursor.execute(sqlite_check_name):
        connection.commit()
        name_search = row[0]
        break
    else:
        name_search = 0 
    
    return name_search

def hwidWrite():
    sqlite_insert_hwid = f"""UPDATE auth 
                        SET hwid = '{hwid}' 
                        WHERE KEY = '{key}'
                        """
    cursor.execute(sqlite_insert_hwid)
    connection.commit()
    cursor.close()

if __name__ == '__main__':
    key_search = check_key()
    if key_search == 0:
        print("Invalid Key")

    else:
        print(f"Key is Valid: {key_search}")
        hwid_search = check_hwid()
        if hwid_search == 0:
            print("Invalid HWID")
        elif hwid_search is None:
            hwidWrite()
            name_search = check_name()
            print(f"Name is: {name_search}")
        else:
            print(f"HWID is Valid: {hwid_search}")
            name_search = check_name()
            print(f"Name is: {name_search}")

connection.close()
print("Closed")



