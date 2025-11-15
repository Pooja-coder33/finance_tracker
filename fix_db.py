import sqlite3

# Connect to your existing finance.db
conn = sqlite3.connect(r"C:\Users\Pooja\OneDrive\Documents\AsusProArtCalibration\OneDrive\Desktop\fm folder\finance_manager\finance.db")
cursor = conn.cursor()

# Add the 'notes' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE transactions ADD COLUMN notes TEXT;")
    conn.commit()
    print("✅ 'notes' column added successfully!")
except Exception as e:
    print("⚠️ Error:", e)

conn.close()
