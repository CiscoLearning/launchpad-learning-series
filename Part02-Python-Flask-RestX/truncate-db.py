from tinydb import TinyDB

db = TinyDB('db/data.json')
db.truncate()
print("DB Cleared!")