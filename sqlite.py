import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('courier.db')
cursor = conn.cursor()

# Create BRANCH table
cursor.execute("""
CREATE TABLE IF NOT EXISTS BRANCH (
    Branch_ID TEXT PRIMARY KEY,
    Branch_Location TEXT,
    Contact_No INTEGER
)
""")

# Create CUSTOMER table
cursor.execute("""
CREATE TABLE IF NOT EXISTS CUSTOMER (
    Customer_Name TEXT,
    Customer_Address TEXT,
    Email TEXT,
    Contact_No INTEGER PRIMARY KEY
)
""")

# Create COURIER table
cursor.execute("""
CREATE TABLE IF NOT EXISTS COURIER (
    Courier_Id TEXT PRIMARY KEY,
    From_Address TEXT,
    To_Address TEXT,
    Branch_ID TEXT,
    Booking_Date DATE,
    Expected_Delivery_Date DATE,
    Weight INTEGER,
    Cost INTEGER,
    Contact_No INTEGER,
    FOREIGN KEY (Branch_ID) REFERENCES BRANCH(Branch_ID),
    FOREIGN KEY (Contact_No) REFERENCES CUSTOMER(Contact_No)
)
""")

# Create COURIER_STATUS table
cursor.execute("""
CREATE TABLE IF NOT EXISTS COURIER_STATUS (
    Courier_Id TEXT,
    Status TEXT,
    Remarks TEXT,
    Actual_Delivered_date DATE,
    Delivered_Branch_ID TEXT,
    FOREIGN KEY (Courier_Id) REFERENCES COURIER(Courier_Id),
    FOREIGN KEY (Delivered_Branch_ID) REFERENCES BRANCH(Branch_ID)
)
""")

# Insert sample data into BRANCH
cursor.executemany("""
INSERT OR IGNORE INTO BRANCH VALUES (?, ?, ?)
""", [
    ("B001", "Bangalore", 9876543210),
    ("B002", "Mumbai", 9123456780),
    ("B003", "Delhi", 9988776655)
])

# Insert sample data into CUSTOMER
cursor.executemany("""
INSERT OR IGNORE INTO CUSTOMER VALUES (?, ?, ?, ?)
""", [
    ("Alice", "123 MG Road, Bangalore", "alice@example.com", 9000010001),
    ("Bob", "42 Marine Drive, Mumbai", "bob@example.com", 9000020002),
    ("Charlie", "7 CP, Delhi", "charlie@example.com", 9000030003)
])

# Insert sample data into COURIER
cursor.executemany("""
INSERT OR IGNORE INTO COURIER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [
    ("C001", "123 MG Road, Bangalore", "42 Marine Drive, Mumbai", "B001", "2025-04-01", "2025-04-05", 2, 150, 9000010001),
    ("C002", "42 Marine Drive, Mumbai", "7 CP, Delhi", "B002", "2025-04-02", "2025-04-06", 5, 300, 9000020002),
    ("C003", "7 CP, Delhi", "123 MG Road, Bangalore", "B003", "2025-04-03", "2025-04-07", 3, 200, 9000030003)
])

# Insert sample data into COURIER_STATUS using None for NULL values
cursor.executemany("""
INSERT OR IGNORE INTO COURIER_STATUS VALUES (?, ?, ?, ?, ?)
""", [
    ("C001", "Delivered", "On time", "2025-04-05", "B002"),
    ("C002", "In Transit", "Delayed due to weather", None, None),
    ("C003", "Delivered", "Slight delay", "2025-04-08", "B001")
])

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created, and sample data inserted successfully.")
