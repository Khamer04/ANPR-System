import cv2
import easyocr
import sqlite3
from datetime import datetime

DB_FILE = "anpr_system.db"
reader = easyocr.Reader(['en'], gpu=False)

def load_stolen_plates():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT plate_number, owner_name, vehicle_model, color, contact_number, status, notes
        FROM stolen_vehicles
    """)
    rows = cur.fetchall()
    conn.close()

    stolen = {}
    for r in rows:
        stolen[r[0].strip().upper()] = {
            "Owner Name": r[1],
            "Vehicle Model": r[2],
            "Color": r[3],
            "Contact Number": r[4],
            "Status": r[5],
            "Notes": r[6]
        }
    return stolen

def save_detected_plate(plate, source):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO detected_plates (plate_number, source, detection_time)
        VALUES (?, ?, ?)
    """, (plate, source, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def extract_plate_text(img):
    results = reader.readtext(img)
    for _, text, _ in results:
        cleaned = "".join(c for c in text if c.isalnum()).upper()
        if len(cleaned) >= 5:
            return cleaned
    return None

def process_video(video_path):
    stolen = load_stolen_plates()
    cap = cv2.VideoCapture(video_path)
    matches = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 17, 17)
        edges = cv2.Canny(blur, 30, 200)

        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 2 < w / float(h) < 6 and w > 100:
                plate_img = frame[y:y+h, x:x+w]
                plate = extract_plate_text(plate_img)
                if plate:
                    save_detected_plate(plate, "Video")
                    if plate in stolen and stolen[plate]["Status"] == "stolen":
                        matches.append((plate, stolen[plate]))

    cap.release()
    return matches
