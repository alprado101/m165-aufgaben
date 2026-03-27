from pymongo import MongoClient

# 1. Verbindung aufbauen (Lokal)
connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

# 2. Test: Informationen vom Server abrufen
print(client.server_info()) 
