# database_handler.py
import sqlite3

# Database connection setup
def connect_to_db():
    """Connect to the SQLite database and return the connection and cursor."""
    conn = sqlite3.connect('data/crms_central.db')
    cur = conn.cursor()
    return conn, cur

# Insert reservation details into the bookings table
def store_reservation(resource, space, date_time, note):
    try:
        # Split the date_time into separate date and time
        reservation_date, reservation_time = date_time.split(' ')  # Assuming date_time is "YYYY-MM-DD HH:MM"

        # Connect to the database
        conn = sqlite3.connect('data/crms_central.db')
        cur = conn.cursor()

        # Insert the reservation details into the bookings table
        query = '''
            INSERT INTO bookings (resource, space, reservation_date, reservation_time, note)
            VALUES (?, ?, ?, ?, ?)
        '''
        cur.execute(query, (resource, space, reservation_date, reservation_time, note))

        # Commit and close the connection
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving reservation: {e}")
        return False

# Optionally, you can add a function to retrieve reservations
def get_all_reservations():
    """Retrieve all reservation details from the bookings table."""
    conn, cur = connect_to_db()
    query = "SELECT * FROM bookings"
    cur.execute(query)
    reservations = cur.fetchall()
    conn.close()
    return reservations
