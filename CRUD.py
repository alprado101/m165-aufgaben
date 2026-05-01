from pymongo import MongoClient, GEOSPHERE
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["hungerdb"]
coll = db["restaurants"]

# Aufgabe 3.1
bezirke = coll.distinct("borough")
print("Stadtbezirke:", ", ".join(bezirke))

# Aufgabe 3.2
pipeline = [
    {"$unwind": "$grades"},  
    {"$group": {
        "_id": "$name", 
        "avgScore": {"$avg": "$grades.score"}
    }},
    {"$sort": {"avgScore": -1}},
    {"$limit": 3}
]
print("\nTop 3 nach Rating:")
for r in coll.aggregate(pipeline):
    print(f" - {r['_id']}: {round(r['avgScore'], 2)}")

# Aufgabe 3.3
# Zuerst Index erstellen (falls noch nicht da)
coll.create_index([("address.coord", GEOSPHERE)])

# 1. Koordinaten von Le Perigord finden
perigord = coll.find_one({"name": "Le Perigord"})
if perigord:
    coords = perigord["address"]["coord"]
    # 2. Den nächsten Nachbarn suchen
    nachbar = coll.find_one({
        "name": {"$ne": "Le Perigord"},
        "address.coord": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": coords}
            }
        }
    })
    print(f"\nNächstes Restaurant zu Le Perigord: {nachbar['name']}")

# Aufgabe 3.4
def restaurant_search_app():
    while True:
        print("\n--- Restaurant-Suche & Bewertung ---")
        name_in = input("Name suchen (leer lassen für alle): ").strip()
        kueche_in = input("Küche suchen (leer lassen für alle): ").strip()

        # Query dynamisch aufbauen
        query = {}
        if name_in:
            query["name"] = {"$regex": name_in, "$options": "i"} 
        if kueche_in:
            query["cuisine"] = {"$regex": kueche_in, "$options": "i"}

        # Ergebnisse finden
        results = list(coll.find(query).limit(10))

        if not results:
            print("Keine Restaurants gefunden.")
            if input("Beenden? (y/n): ").lower() == "n": break
            continue

        # Ergebnisse anzeigen
        print("\nErgebnisse:")
        for i, res in enumerate(results):
            print(f"[{i}] {res['name']} ({res['cuisine']})")

        # Auswahl zur Bewertung
        wahl = input("\nIndex wählen für Bewertung (oder Enter für neue Suche): ")
        
        if wahl.isdigit() and int(wahl) < len(results):
            selected = results[int(wahl)]
            new_score = int(input(f"Punkte (0-100) für {selected['name']}: "))
            
            #  Aufgabe 3.5
            new_grade = {
                "date": datetime.datetime.now(), # Aktuelles Datum
                "grade": "A", 
                "score": new_score
            }

            coll.update_one(
                {"_id": selected["_id"]},
                {"$push": {"grades": new_grade}}
            )
            print(f"Bewertung für {selected['name']} gespeichert!")

        if input("\nNoch eine Suche? (y/n): ").lower() == "n":
            break

if __name__ == "__main__":
    restaurant_search_app()