from pymongo import MongoClient
from bson.objectid import ObjectId

# Aufgabe 6.1
class Room:
    def __init__(self, name, seats, is_reservable, _id = None):
        if(_id is not None):
            self._id = _id
        self.name = name
        self.seats = seats
        self.is_reservable = is_reservable

# Aufgabe 6.1 
class Dao_room:
    def __init__(self, connection_string):
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        self.col.insert_one(room.__dict__)

    def read(self):
        data = self.col.find_one()
        return Room(**data) if data else None

    def update(self, room_id, new_data):
        self.col.update_one({"_id": ObjectId(room_id)}, {"$set": new_data})

    def delete(self, room_id):
        self.col.delete_one({"_id": ObjectId(room_id)})


# Aufgabe 6.2
class Joke:
    def __init__(self, text, category, author, _id = None):
        if(_id is not None):
            self._id = _id
        self.text = text
        self.category = category  
        self.author = author

# Aufgabe 6.3
class Dao_joke:
    def __init__(self, connection_string):
        self.col = MongoClient(connection_string)["joke_db"]["jokes"]

    def insert(self, joke):
        self.col.insert_one(joke.__dict__)

    def get_category(self, category_name):
        cursor = self.col.find({"category": category_name})
        return [Joke(**doc) for doc in cursor]

    def delete(self, joke_id):
        self.col.delete_one({"_id": ObjectId(joke_id)})


# Testbereich
if __name__ == "__main__":
    conn = "mongodb://localhost:27017/"
    
    # Test Room (6.1)
    dr = Dao_room(conn)
    r = Room("Pilatus", 12, True)
    dr.create(r)
    
    # Test Joke (6.2 & 6.3)
    dj = Dao_joke(conn)
    j = Joke("Was ist gelb und kann schiessen? Eine Banone.", ["Wortwitz"], "Alondra")
    dj.insert(j)
    
    results = dj.get_category("Wortwitz")
    for item in results:
        print(f"Joke: {item.text}")