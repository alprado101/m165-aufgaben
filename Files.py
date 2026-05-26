import os
from pymongo import MongoClient
import gridfs

# Aufgabe 7.1
"""
FRAGE: Wie wird die Verbindung der einzelnen Documents zueinander hergestellt?
ANTWORT: GridFS nutzt zwei Collections. In 'fs.files' liegt das Hauptdokument mit einer 
einzigartigen '_id'. In 'fs.chunks' liegen die Datenpakete. Jedes Paket in 'fs.chunks' 
besitzt ein Feld namens 'files_id', welches auf die '_id' in 'fs.files' verweist. 
Zusätzlich gibt es ein Feld 'n', das die Reihenfolge der Pakete angibt.

FRAGE: In welcher Codierung werden die Rohdaten des Files gespeichert?
ANTWORT: Die Daten werden als reine Binärdaten (BSON-Typ: binData) gespeichert. 
Es findet keine Text-Codierung (wie z.B. Base64) statt, was Speicherplatz spart.
"""

# Aufgabe 7.2
class PhotoAlbum:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['photo_album_db']
        self.fs = gridfs.GridFS(self.db)

    # Aufgabe 7.2.1
    def add_photo(self, file_path, album_name):
        if not os.path.exists(file_path):
            print(f"Datei {file_path} nicht gefunden.")
            return

        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            self.fs.put(f, filename=filename, metadata={"album": album_name})
        print(f"Foto '{filename}' zu Album '{album_name}' hinzugefügt.")

    # Aufgabe 7.2.2
    def download_album(self, album_name):
        files = self.db['fs.files'].find({"metadata.album": album_name})
        
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        for file_info in files:
            file_id = file_info['_id']
            filename = file_info['filename']
            
            data = self.fs.get(file_id).read()
            restore_path = os.path.join("downloads", f"{album_name}_{filename}")
            
            with open(restore_path, 'wb') as f:
                f.write(data)
            print(f"Wiederhergestellt: {restore_path}")

# Aufgabe 7.2.3
if __name__ == "__main__":
    conn = 'mongodb://localhost:27017/'
    album = PhotoAlbum(conn)
