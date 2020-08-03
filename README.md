# Auth-System-with-HWID-lock
### **Uses:** 
* SQLite 
* HWID 
* Salt 
* Current Time (Hours and Minutes)
* SHA512 Hash

## **Requirements**

```
$ pip3 install -r requirements.txt
```


## **Server**

```
$ python3 auth.py
```

#### Server is hosted [locally](http://127.0.0.1:1337/auth "auth page") on port 1337.

## **Client**

```
$ python3 test.py
```

#### The client sends a POST data to the auth server, which if it is a success then checks if both hashes matches.
#### If it does, then access is granted, else access is denied.
