import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Aufgabe 4.1
"""
RECHERCHE:
Umgebungsvariablen werden in Python über das Modul 'os' mit 'os.getenv()' ausgelesen.
In C# geschieht dies über 'Environment.GetEnvironmentVariable()'.
Dies dient der Sicherheit, damit Passwörter nicht im Code stehen.
"""

path_variable = os.getenv("PATH")

print("Aufgabe 4.1")
if path_variable:
    print(f"Erfolgreich ausgelesen: {path_variable[:100]}...")
else:
    print("Fehler: PATH konnte nicht gefunden werden.")


# Aufgabe 4.2
connection_string = os.getenv("MONGO_URI")

print("\nAufgabe 4.2")

if not connection_string:
    print("Fehler: Die Umgebungsvariable 'MONGO_URI' ist nicht gesetzt!")
else:
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("Verbindung zur Cloud-Datenbank war erfolgreich!")
        print("Vorhandene Datenbanken:", client.list_database_names())
        
    except ConnectionFailure:
        print("Verbindung fehlgeschlagen: Prüfe deinen Link oder deine IP-Freigabe.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")