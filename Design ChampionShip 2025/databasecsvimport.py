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
    category TEXT,
    tip TEXT,
    source TEXT DEFAULT 'manual'
)
""")


with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            cursor.execute(
                "INSERT INTO waste_items (item_name, category, tip, source) VALUES (?, ?, ?, ?)",
                (row['item_name'].lower(), row['category'], row['tip'], 'csv')
            )
        except sqlite3.IntegrityError:
            # Skip if item already exists
            continue

conn.commit()
print("CSV items imported successfully!")


def clear_manual_items():
    cursor.execute("DELETE FROM waste_items WHERE source != 'csv'")
    conn.commit()
    print("All manual items cleared, CSV items preserved.")



conn.close()
print("Database ready and safe to use!")
