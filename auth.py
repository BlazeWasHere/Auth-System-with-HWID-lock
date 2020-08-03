# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from flask import Flask, request, jsonify
import subprocess
import hashlib
import sqlite3
import json
import time


app = Flask(__name__)

salt = '00000' #enter your salt
#can change the name of the db
db = "auth.db"

def check_hwid(hwid,key):
      """Makes a query to get auth column from the key
      Returns 0 if not found
      """
      connection = sqlite3.connect(db) 
      cursor = connection.cursor() 
      sqlite_check_hwid = f"""SELECT HWID FROM auth
                              WHERE KEY = '{key}'     
                           """
      for row in cursor.execute(sqlite_check_hwid):
        connection.commit()
        hwid_search = row[0] #returns hwid and then breaks out of loop
        break
      else:
        hwid_search = 0 #if nothing found variable is 0

      return hwid_search

def check_key(key):
      """Makes a query, to check if key is in the database
      If it cant be found it returns '0'
      """
      connection = sqlite3.connect(db) 
      cursor = connection.cursor() 
      sqlite_check_key = f"""SELECT KEY FROM auth
                             WHERE KEY = '{key}'
                          """
      for row in cursor.execute(sqlite_check_key):
        connection.commit()
        key_search = row[0]  #returns key and then breaks out of loop
        break
      else:
        key_search = 0 #if nothing found variable is 0

      return key_search

def check_name(key):
      """Checks for name column from the key
      Returns 0 if not found
      """
      global name_search
      connection = sqlite3.connect(db) 
      cursor = connection.cursor() 
      sqlite_check_name = f"""SELECT NAME FROM auth 
                              WHERE KEY = '{key}';
                           """ 
      for row in cursor.execute(sqlite_check_name):
        connection.commit() 
        name_search = row[0] #returns name and then breaks out of loop
        break
      else:
        name_search = 0 #if nothing found variable is 0
    
      return name_search

def hwidWrite(hwid,key):
      """Writes/updates the hwid column
      If it isnt set yet or is NULL
      """
      connection = sqlite3.connect(db) 
      cursor = connection.cursor() 
      # writes the hwid where the key is, therefore HWID locking
      sqlite_insert_hwid = f"""UPDATE auth 
                               SET hwid = '{hwid}' 
                               WHERE KEY = '{key}'
                            """ 
      cursor.execute(sqlite_insert_hwid)
      connection.commit() #executing query
      cursor.close()

def auth_check(key,hwid):
      """Checks the key if it is the database
      Aswell as if it is HWID locked already
      """
      key_search = check_key(key)
      if key_search == 0:
            # if key not found (0)
            return {'response':'invalid key'}
      else:
            #if key is found then it checks for hwid
            hwid_search = check_hwid(hwid,key)
            if hwid_search == 0:
                  # if hwid not found (0)
                  return {'response': 'invalid hwid'}
            elif hwid_search is None:
                   # if hwid is NULL or not set
                  hwidWrite(hwid,key) #enters HWID into the database
                  name_search = check_name(key) # searches for name in the database
                  return {'response': 'valid key'}  
            else:
                  # if hwid is found
                  if hwid_search != hwid:
                        # if hwid is found in the database 
                        # is not the same as hwid received (from client/request)
                        return {'response': 'invalid hwid'}
                  else:
                        #queries for name in the database
                        name_search = check_name(key)
                        return {'response': 'valid key'}         

@app.route('/auth', methods=["POST"])
def auth():
      """Request it receives from the client
      Which then checks for it in the database
      """
      #stores data from request into variables
      data = request.get_json(force=True)
      key = json.loads(data)['key']
      hwid = json.loads(data)['hwid']

      details = auth_check(key,hwid)
      resp = details["response"]

      if resp == "valid key":
            #create a sha512 hash
            hash = hashlib.sha512()
            name = name_search
            #gets current time
            time_current = str(time.strftime("%H-%M")) #gets time in hours and minutes
            # sha512 hash with time,salt,key,hwid
            hash.update(f"{time_current}{salt}{key}{hwid}".encode('utf-8'))
            hash = hash.hexdigest()
            return jsonify({   
                  "success":"true",
                  "hash":hash,
                  "name":name
            }) #returns the hash,name, and a success
      elif resp == "invalid hwid":
           return jsonify({
                  "success":"false",
                  "reason":"invalid hwid"
            }) 
      elif resp == "invalid key":
            return jsonify({
                  "success":"false",
                  "reason":"invalid key"
            })
      else:
            return jsonify({   
                  "success":"false",
                  "reason":"no"
            })

if __name__ == '__main__':
    app.run(port='1337') #running locally, port 1337
