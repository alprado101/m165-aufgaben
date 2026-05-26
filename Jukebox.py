import random
from pymongo import MongoClient
from bson.objectid import ObjectId

# Aufgabe 9.1 - Management
# Aufgabe 9.1.1
class Song:
    def __init__(self, name, artist, album=None, genre=None, year=None, _id=None):
        if _id: 
            self._id = _id
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year

class JukeboxDAO:
    def __init__(self, connection_string):
        self.col = MongoClient(connection_string)["jukebox_db"]["songs"]

    # Aufgabe 9.1.2
    def insert_song(self, song):
        result = self.col.insert_one(song.__dict__)
        return str(result.inserted_id)

    # Aufgabe 9.1.3
    def update_song(self, song_id, new_data):
        result = self.col.update_one(
            {"_id": ObjectId(song_id)}, 
            {"$set": new_data}
        )
        return result.modified_count

    # Aufgabe 9.1.4
    def delete_song(self, song_id):
        result = self.col.delete_one({"_id": ObjectId(song_id)})
        return result.deleted_count

    # Aufgabe 9.2 - Player
    # Aufgabe 9.2.1
    def search_songs(self, search_params):
        query = {}
        for key, value in search_params.items():
            if value:
                query[key] = {"$regex": f".*{value}.*", "$options": "i"}
        
        cursor = self.col.find(query)
        return [Song(**doc) for doc in cursor]

    # Aufgabe 9.2.3
    def get_random_song(self):
        pipeline = [{"$sample": {"size": 1}}]
        result = list(self.col.aggregate(pipeline))
        return Song(**result[0]) if result else None


class Player:
    def __init__(self, dao):
        self.dao = dao
        # Aufgabe 9.2.2
        self.playlist = []

    # Aufgabe 9.2.2
    def add_to_playlist(self, song):
        self.playlist.append(song)
        print(f"Zur Playlist hinzugefügt: {song.name}")

    # Aufgabe 9.2.3
    def play(self):
        print("\n--- Audio Player ---")
        if not self.playlist:
            print("Playlist ist leer. Spiele zufälligen Song...")
            song = self.dao.get_random_song()
        else:
            song = self.playlist.pop(0)
        
        if song:
            print(f"Spiele jetzt: {song.name} von {song.artist}")
        else:
            print("Keine Songs in der Datenbank verfügbar.")


if __name__ == "__main__":
    conn = "mongodb://localhost:27017/"
    dao = JukeboxDAO(conn)
    jukebox_player = Player(dao)

    s1 = Song("Yellow Submarine", "The Beatles", "Yellow Submarine", "Pop", 1969)
    s2 = Song("Another Brick in the Wall", "Pink Floyd", "The Wall", "Rock", 1979)
    
    id1 = dao.insert_song(s1)
    id2 = dao.insert_song(s2)

    ergebnisse = dao.search_songs({"artist": "Beatles", "name": "Yell"})
    
    for gefunden in ergebnisse:
        jukebox_player.add_to_playlist(gefunden)

    jukebox_player.play()  
    jukebox_player.play()  