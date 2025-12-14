import sqlite3
from datetime import datetime

DB_FILE = "anpr_system.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stolen_vehicles (
    plate_number TEXT PRIMARY KEY,
    owner_name TEXT,
    vehicle_model TEXT,
    color TEXT,
    contact_number TEXT,
    status TEXT,
    added_timestamp TEXT,
    notes TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS detected_plates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate_number TEXT,
    source TEXT,
    detection_time TEXT
)
""")

sample_data = [
    ("CA455822", "Vishal", "McLaren", "Orange", "+916305164749", "stolen",
     datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Highway theft"),
    ("TS09AB6789", "Aarav", "Honda City", "Silver", "+919876543210", "stolen",
     datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Hyderabad report")
]

cursor.executemany("""
INSERT OR REPLACE INTO stolen_vehicles
(plate_number, owner_name, vehicle_model, color, contact_number, status, added_timestamp, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()

print("✅ Database created successfully")
