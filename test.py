# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from colorama import Fore,init
from sys import platform
from os import system
import subprocess
import datetime
import requests
import hashlib
import time
import json


init()

#just some colours
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
nice = Fore.WHITE + "[-]"
magenta = Fore.MAGENTA
red = Fore.LIGHTRED_EX
white = Fore.WHITE
cyan = Fore.CYAN

if platform == "win32": 
    # windows
    clear = "cls"
    hwid = subprocess.check_output('wmic csproduct get uuid')
    hwid = hwid.decode().split('\n')[1].strip()
else:
    # linux
    clear = "clear"
    subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())

def auth():
    """Makes a sha512 hash locally with
    time,salt,key,hwid and checks if
    matches the received hash by auth server
    """
    salt = "00000" #salt which is same as server
    key = input(f"\n{nice} {cyan}Enter Key\n{white}  > ")
 
    hash = hashlib.sha512() #sha512 hash
    time_current = str(time.strftime("%H-%M")) #gets time in hours and minutes
    hash.update(f"{time_current}{salt}{key}{hwid}".encode('utf-8'))
    hash = hash.hexdigest()

    data = {
         "key":key,
         "hwid":hwid
         }

    try:
        #sending post data
        sadauth = requests.post("http://127.0.0.1:1337/auth", 
                                json=json.dumps(data))
    except:
        #if auth system is down, or if we cant connect to it
        print(f"{nice} {red}There seems to be an error with auth server.")
        input()
        quit()

    if json.loads(sadauth.text)['success'] == "false":
        if json.loads(sadauth.text)['reason'] == "invalid hwid":
            print("Invalid HWID!")
        elif json.loads(sadauth.text)['reason'] == "invalid key":
            print("Invalid Key!")
        elif json.loads(sadauth.text)['reason'] == "no":
            print("There was an error.")
        print("Restarting in 5 seconds...") 
        time.sleep(5)
        system(clear)
        auth()

    else:
        #if success is 'true'
        print(json.loads(sadauth.text)['hash'])
        if json.loads(sadauth.text)['hash'] == hash:
            nameInc = json.loads(sadauth.text)['name']
            system(clear)
            #auth granted
            print(f"{nice} {green}Auth Granted. Welcome {nameInc}!\n")
        else:
            #hash not matching
            print("Error...")
            print("Restarting in 5 seconds...") 
            time.sleep(5)
            system(clear)
            auth()

if __name__ == '__main__':
    auth()