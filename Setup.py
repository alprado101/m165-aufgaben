from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
print(client.server_info()) 

#Aufgabe 1.1
# ODM steht für Object-Document Mapper.
# Ein ODM ist ein Übersetzer. Er verbindet zwei Welten. ODM erlaubt,Datenbank-Einträge so zu behandeln, als wären es ganz normale Variablen im Code. So musst man keine komplizierten Datenbank-Befehle schreiben. Er übersetzt Python-Objekt in ein MongoDB-Dokument und umgekehrt.

# Aufgabe 1.2
client.admin.command('ping')
print("Verbindung erfolgreich: Der Server antwortet!")

dbs = client.list_database_names()
print("Vorhandene Datenbanken:", dbs)