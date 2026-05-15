import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# MODELL-KLASSEN (Struktur der Daten)

class Room:
    def __init__(self, name, seats, is_reservable, _id = None):
        if(_id is not None):
            self._id = _id
        self.name = name
        self.seats = seats
        self.is_reservable = is_reservable

# Aufgabe 6.2.2: Die Modell-Klasse für Witze
class Joke:
    def __init__(self, text, category, author, _id = None):
        if(_id is not None):
            self._id = _id
        self.text = text
        self.category = category  # Erwartet eine Liste von Kategorien
        self.author = author


# DAO-KLASSEN (Datenbank-Schnittstellen)

# Aufgabe 6.1: Ergänzung der Dao_room Klasse
class Dao_room:
    def __init__(self, connection_string):
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        """Erstellt ein neues Zimmer (aus dem Beispiel)"""
        self.col.insert_one(room.__dict__)

    def read(self):
        """Liest ein Zimmer aus (aus dem Beispiel)"""
        data = self.col.find_one()
        return Room(**data) if data else None

    # --- Ergänzung Aufgabe 6.1 ---
    def update(self, room_id, new_data):
        """Aktualisiert ein Zimmer basierend auf der ID."""
        result = self.col.update_one(
            {"_id": ObjectId(room_id)}, 
            {"$set": new_data}
        )
        return result.modified_count

    # --- Ergänzung Aufgabe 6.1 ---
    def delete(self, room_id):
        """Löscht ein Zimmer basierend auf der ID."""
        result = self.col.delete_one({"_id": ObjectId(room_id)})
        return result.deleted_count


# Aufgabe 6.2.2: Erstellung der DAO-Klasse für Witze
class Dao_joke:
    def __init__(self, connection_string):
        # Eigene Datenbank 'joke_db' mit Collection 'jokes'
        self.col = MongoClient(connection_string)["joke_db"]["jokes"]

    # --- Aufgabe 6.2.2: insert ---
    def insert(self, joke):
        """Fügt einen neuen Witz zur Datenbank hinzu."""
        self.col.insert_one(joke.__dict__)

    # --- Aufgabe 6.2.2: get_category ---
    def get_category(self, category_name):
        """Sucht alle Witze einer bestimmten Kategorie."""
        cursor = self.col.find({"category": category_name})
        return [Joke(**doc) for doc in cursor]

    # --- Aufgabe 6.2.2: delete ---
    def delete(self, joke_id):
        """Löscht einen Witz anhand der übergebenen ID."""
        result = self.col.delete_one({"_id": ObjectId(joke_id)})
        return result.deleted_count


# MAIN - TESTBEREICH

if __name__ == "__main__":
    # Verbindung zur lokalen MongoDB (Standard-Port)
    conn = "mongodb://localhost:27017/"
    
    # Instanziierung der DAOs
    room_dao = Dao_room(conn)
    joke_dao = Dao_joke(conn)

    # Test Aufgabe 6.1 (Zimmer)
    print("--- Test Aufgabe 6.1 (Zimmer) ---")
    neuer_raum = Room("Pilatus", 12, True)
    room_dao.create(neuer_raum)
    print("Zimmer erstellt.")

    # Test Aufgabe 6.2.2 (Jokes)
    print("\n--- Test Aufgabe 6.2.2 (Jokes) ---")
    
    # 1. Insert
    witz_beispiel = Joke(
        text="Warum können Bienen so gut rechnen? Weil sie den ganzen Tag mit Summen beschäftigt sind.",
        category=["Tiere", "Wortwitz"],
        author="Alondra"
    )
    joke_dao.insert(witz_beispiel)
    print("Neuer Witz wurde eingefügt.")

    # 2. Get Category
    witze = joke_dao.get_category("Tiere")
    print(f"Gefundene Tier-Witze: {len(witze)}")
    for j in witze:
        print(f" > {j.text}")

    print("\nAlle Aufgaben erfolgreich ausgeführt!")