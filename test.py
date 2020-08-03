import json

x = '{"response": [{"confirmed": 0, "addr": "14vDeKDPJHdNTFgRDGt3PKcgbu9AmKGhUd", "unconfirmed": 0}]}'

for unconfirmed in json.loads(x)['response']:
    print(unconfirmed['unconfirmed'])