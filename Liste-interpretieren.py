import os
from pymongo import MongoClient
from PIL import Image, ImageDraw

client = MongoClient('mongodb://localhost:27017/')
db = client['sample_restaurants'] 
collection = db['neighborhoods']

def scale_coords(coords, width, height, min_lon, max_lon, min_lat, max_lat):
    scaled = []
    for lon, lat in coords:
        x = (lon - min_lon) / (max_lon - min_lon) * (width - 40) + 20
        y = height - ((lat - min_lat) / (max_lat - min_lat) * (height - 40) + 20)
        scaled.append((x, y))
    return scaled

# Aufgabe 8.1
def draw_single_neighborhood():
    print("Aufgabe 8.1: Ein einzelnes Viertel")
    item = collection.find_one()
    
    if not item:
        print("Keine Daten in der Collection gefunden!")
        return

    coords = []
    if item['geometry']['type'] == 'Polygon':
        coords = item['geometry']['coordinates'][0]
    else: 
        coords = item['geometry']['coordinates'][0][0]

    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    
    img_size = 500
    im = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(im)
    
    points = scale_coords(coords, img_size, img_size, min(lons), max(lons), min(lats), max(lats))
    draw.polygon(points, outline="red", fill="orange")
    
    print(f"Zeichne Viertel: {item['name']}")
    im.show()

# Aufgabe 8.2
def draw_all_neighborhoods():
    print("\nAufgabe 8.2: Alle Viertel")
    all_items = list(collection.find())
    print(f"Gefundene Dokumente: {len(all_items)}")

    all_points = []
    
    for item in all_items:
        g_type = item['geometry']['type']
        if g_type == 'Polygon':
            all_points.extend(item['geometry']['coordinates'][0])
        elif g_type == 'MultiPolygon':
            for poly in item['geometry']['coordinates']:
                all_points.extend(poly[0])

    if not all_points:
        print("Fehler: Keine Koordinaten gefunden. Prüfe deinen Datenbanknamen!")
        return

    min_lon = min(p[0] for p in all_points)
    max_lon = max(p[0] for p in all_points)
    min_lat = min(p[1] for p in all_points)
    max_lat = max(p[1] for p in all_points)
    
    img_size = 1000
    im = Image.new("RGB", (img_size, img_size), "black")
    draw = ImageDraw.Draw(im)
    
    for item in all_items:
        g_type = item['geometry']['type']
        polys_to_draw = []
        
        if g_type == 'Polygon':
            polys_to_draw.append(item['geometry']['coordinates'][0])
        elif g_type == 'MultiPolygon':
            for poly in item['geometry']['coordinates']:
                polys_to_draw.append(poly[0])
                
        for coords in polys_to_draw:
            if len(coords) > 2:
                points = scale_coords(coords, img_size, img_size, min_lon, max_lon, min_lat, max_lat)
                draw.line(points + [points[0]], fill="lime", width=1)
            
    print("Bild wird erstellt...")
    im.show()

if __name__ == "__main__":
    draw_single_neighborhood()
    draw_all_neighborhoods()