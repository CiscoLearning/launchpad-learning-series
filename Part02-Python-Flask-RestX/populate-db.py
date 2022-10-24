from tinydb import TinyDB
import random

db = TinyDB('db/data.json')
db.insert({"id": random.randint(1,500), "ipadd": "192.168.100.12", "mask": "255.255.255.0", "vrf": "Global", "status": "available"})
db.insert({"id": random.randint(1,500), "ipadd": "192.168.100.10", "mask": "255.255.255.0", "vrf":"Admin", "status":"reserved"})
db.insert({"id": random.randint(1,500), "ipadd": "192.168.100.100", "mask": "255.255.255.0", "vrf":"dmz", "status":"used"})
