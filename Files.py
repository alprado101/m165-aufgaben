import os
from pymongo import MongoClient
import gridfs

# Aufgabe 7.1: Theorie & Beobachtung
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

# Aufgabe 7.2: Fotoalbum Applikation

class PhotoAlbum:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['photo_album_db']
        self.fs = gridfs.GridFS(self.db)

    def add_photo(self, file_path, album_name):
        """
        Speichert ein Bild in GridFS.
        Laut Dokumentation können Metadaten über das Argument 'metadata' 
        als Dictionary mitgegeben werden.
        """
        if not os.path.exists(file_path):
            print(f"❌ Datei {file_path} nicht gefunden.")
            return

        filename = os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_id = self.fs.put(
                f, 
                filename=filename, 
                metadata={"album": album_name}
            )
        print(f"✅ Foto '{filename}' wurde dem Album '{album_name}' hinzugefügt. (ID: {file_id})")

    def download_album(self, album_name):
        """
        Sucht alle Dateien, die in ihren Metadaten den passenden Albumnamen haben,
        und stellt sie im lokalen Ordner wieder her.
        """
        print(f"\n--- Download Album: {album_name} ---")
        
        query = {"metadata.album": album_name}
        files = self.db['fs.files'].find(query)
        
        found = False
        for file_info in files:
            found = True
            file_id = file_info['_id']
            filename = file_info['filename']
            
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            
            restore_path = os.path.join("downloads", f"{album_name}_{filename}")
            
            data = self.fs.get(file_id).read()
            with open(restore_path, 'wb') as f:
                f.write(data)
            print(f" > '{filename}' wiederhergestellt unter: {restore_path}")
            
        if not found:
            print(f"ℹ️ Keine Fotos im Album '{album_name}' gefunden.")


if __name__ == "__main__":
    conn_string = 'mongodb://localhost:27017/'
    album_app = PhotoAlbum(conn_string)

    album_app.download_album("Sommerurlaub")