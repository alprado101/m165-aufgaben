import psutil
import time
import datetime
import matplotlib.pyplot as plt
from pymongo import MongoClient, ASCENDING

client = MongoClient("mongodb://localhost:27017/")
db = client["system_monitor"]
logs = db["power_stats"]

# Aufgabe 5.1: Klasse Power erstellen
class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if cpu is None:
            self.cpu = psutil.cpu_percent(interval=1) 
            mem = psutil.virtual_memory()
            self.ram_total = mem.total
            self.ram_used = mem.used
            self.timestamp = datetime.datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp

    def to_dict(self):
        return vars(self)

# Aufgabe 5.2: Logging-Applikation mit 10.000er Limit
def start_logging():
    print("Logging gestartet... Drücke Strg+C, um das Logging zu beenden und den Graphen anzuzeigen.")
    try:
        while True:
            entry = Power()
            logs.insert_one(entry.to_dict())
            print(f"[{entry.timestamp.strftime('%H:%M:%S')}] CPU: {entry.cpu}% | RAM: {round(entry.ram_used/1024**3, 2)} GB gespeichert.")

            count = logs.count_documents({})
            if count > 10000:
                to_delete = count - 10000
                oldest_ids = logs.find({}, {"_id": 1}).sort("timestamp", ASCENDING).limit(to_delete)
                ids_to_remove = [doc["_id"] for doc in oldest_ids]
                logs.delete_many({"_id": {"$in": ids_to_remove}})
            
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nLogging beendet. Graph wird geladen...")
        show_graph()

# Aufgabe 5.3: Zusätzliche Applikation für den Graphen
def show_graph():
    data = list(logs.find().sort("timestamp", -1).limit(60))
    data.reverse() 

    if not data:
        print("Keine Daten für den Graphen vorhanden.")
        return

    times = [d["timestamp"].strftime("%H:%M:%S") for d in data]
    cpu_vals = [d["cpu"] for d in data]
    ram_vals = [d["ram_used"] / (1024**3) for d in data] # Umrechnung in GB

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Uhrzeit')
    ax1.set_ylabel('CPU Auslastung (%)', color='tab:red')
    ax1.plot(times, cpu_vals, color='tab:red', linewidth=2, label="CPU %")
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_ylim(0, 100)

    ax2 = ax1.twinx()
    ax2.set_ylabel('RAM verwendet (GB)', color='tab:blue')
    ax2.plot(times, ram_vals, color='tab:blue', linewidth=2, label="RAM GB")
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title('Power Statistics: CPU & RAM Auslastung')
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    start_logging()