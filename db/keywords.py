from .init_db import *

def set_db_keyword(user_id, keyword):
    """
    Stores the keyword for the user in the database.

    Args:
        user_id (int): The user's id.
        keyword (str): The keyword to set.

    Returns:
        None
    """
    db, cursor = get_db()
    if cursor.execute("SELECT * FROM keywords WHERE user_id = ? AND keyword = ?", (user_id, keyword)).fetchone() is None:
        cursor.execute("INSERT INTO keywords (user_id, keyword, occurrences) VALUES (?, ?, 0)", (user_id, keyword))
        db.commit()
    else:
        cursor.execute("UPDATE keywords SET last_used_ts = CURRENT_TIMESTAMP WHERE user_id = ? AND keyword = ?", (user_id, keyword))
        db.commit()
    close_db(db)

def get_current_keyword(user_id):
    """
    Gets the keyword for the user from the database.

    Args:
        user_id (int): The user's id.

    Returns:
        str: The keyword for the user.
    """
    db, cursor = get_db()
    row = cursor.execute("SELECT keyword FROM keywords WHERE user_id = ? ORDER BY last_used_ts DESC LIMIT 1", (user_id,)).fetchone()
    if row is None:
        return None
    else:
        keyword = row[0]
    db.close()
    return keyword

def update_keyword_occurrences(user_id, keyword, occurrences):
    """
    Updates the number of times the keyword has been mentioned for the user.

    Args:
        user_id (int): The user's id.
        keyword (str): The keyword to update.
        occurrences (int): The number of times the keyword has been mentioned.

    Returns:
        None
    """
    db, cursor = get_db()
    cursor.execute("UPDATE keywords SET occurrences = occurrences + ? WHERE user_id = ? AND keyword = ?", (occurrences, user_id, keyword))
    db.commit()
    close_db(db)

def get_keyword_occurrences(user_id, keyword):
    """
    Gets the number of times the keyword has been mentioned for the user.

    Args:
        user_id (int): The user's id.
        keyword (str): The keyword to get the count for.

    Returns:
        int: The number of times the keyword has been mentioned by the user.
    """
    db, cursor = get_db()
    cursor.execute("SELECT occurrences FROM keywords WHERE user_id = ? AND keyword = ?", (user_id, keyword))
    count = cursor.fetchone()[0]
    db.close()
    return count

def get_total_keyword_occurrences(keyword):
    """
    Gets the total number of times the keyword has been mentioned by all users.

    Args:
        keyword (str): The keyword to get the count for.

    Returns:
        int: The number of times the keyword has been mentioned by all users.
    """
    db, cursor = get_db()
    cursor.execute("SELECT SUM(occurrences) FROM keywords WHERE keyword = ?", (keyword,))
    count = cursor.fetchone()[0]
    db.close()
    return count