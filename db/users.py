from .init_db import *

def add_user(name):
    """
    Adds a user to the database.

    Args:
        name (str): The name of the user.

    Returns:
        None
    """
    db, cursor = get_db()
    if cursor.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone() is None:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        db.commit()
    close_db(db)

def get_user_id(name):
    """
    Gets the user's id from the database.

    Args:
        name (str): The name of the user.

    Returns:
        int: The user's id.
    """
    db, cursor = get_db()
    row = cursor.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()
    if row is None:
        user_id = None
    else:
        user_id = row[0]
    db.close()
    return user_id