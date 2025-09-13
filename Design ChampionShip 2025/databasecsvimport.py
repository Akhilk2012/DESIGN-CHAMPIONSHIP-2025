import sqlite3
import csv

DATABASE_FILE = "waste_classification.db"
CSV_FILE = "waste_items.csv"

conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS waste_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT UNIQUE,
    response TEXT,
    source TEXT DEFAULT 'manual'
)
""")

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        item = row['item'].strip().lower()
        response = row['response'].strip()
        try:
            cursor.execute(
                "INSERT INTO waste_items (item_name, response, source) VALUES (?, ?, ?)",
                (item, response, 'csv')
            )
        except sqlite3.IntegrityError:
            continue  # skip duplicates

conn.commit()
print("CSV items imported successfully!")
conn.close()
