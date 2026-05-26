from pymongo import MongoClient
from bson.objectid import ObjectId

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

dblist = client.list_database_names()

for db in dblist:
	print(db)

if "admin" in dblist:
    print("Database exists.")
else:
    print("Database does not exist.")


# Aufgabe 2
def main():
    print("Tippe 'exit' bei der Datenbank-Auswahl, um zu stoppen")
    while True:
        dblist = client.list_database_names()
        
        if not dblist:
            print("No Database")
            input("\nPress any button to return")
            continue 

        # Aufgabe 2.1
        print("Databases")
        for db_name in dblist:
            print(f" - {db_name}")

        selected_db = input("\nSelect Database: ")

        if selected_db.lower() in ['exit']:
            print("Programm wird beendet")
            break
        
        if selected_db not in dblist:
            print(f"Error: '{selected_db}' doesn't exist!")
            continue

        # Aufgabe 2.2
        db = client[selected_db]
        collist = db.list_collection_names()

        print(f"\n{selected_db}")
        print("\nCollections")
        
        if not collist:
            print("No Collection")
            input("\nPress any button to return")
            continue

        for col_name in collist:
            print(f" - {col_name}")

        selected_col = input("\nSelect Collection: ")
        
        if selected_col not in collist:
            print(f"Error: '{selected_col}' doesn't exist!")
            continue

        # Aufgabe 2.3
        collection = db[selected_col]

        documents = list(collection.find({}, {"_id": 1}))

        print(f"\n{selected_db}.{selected_col}")
        print("\nDocuments")
        
        if not documents:
            print("No document found.")
            input("\nPress any button to return")
            continue

        for doc in documents:
            print(f" - {doc['_id']}")

        selected_id = input("\nSelect Document: ")

        # Aufgabe 2.4
        try:
            if len(selected_id) == 24:
                doc_content = collection.find_one({"_id": ObjectId(selected_id)})
            else:
                doc_content = collection.find_one({"_id": selected_id})
        except:
            doc_content = None

        if not doc_content:
            print(f"Fehler: Dokument '{selected_id}' nicht gefunden.")
            continue

        print(f"\n{selected_db}.{selected_col}.{selected_id}")
        
        for key, value in doc_content.items():
            print(f" > {key}: {value}")

        input("\nPress any button to return")

if __name__ == "__main__":
    main()