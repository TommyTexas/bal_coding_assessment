import sqlite3

def get_db():
    """
    Connects to the database and returns the connection and cursor.

    Args:
        None

    Returns:
        tuple: A tuple containing the connection and cursor.
    """
    conn = sqlite3.connect("mock.db")
    cursor = conn.cursor()
    return conn, cursor

def close_db(db):
    """
    Closes the database connection.

    Args:
        db (sqlite3.Connection): The database connection to close.
    """
    db.close()



