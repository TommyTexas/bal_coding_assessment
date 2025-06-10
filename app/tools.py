from mcp.server.fastmcp import FastMCP
from playsound import playsound
import sys
import os
from pathlib import Path

# Add parent directory to Python path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from db.users import *
from db.keywords import *

user_id = int(os.environ.get('USER_ID'))

mcp = FastMCP("keyword_tracker")

@mcp.tool()
def play_notification(keyword: str):
    """plays notification sound and updates the keyword count"""
    playsound("assets/notification.mp3", block=False)
    update_keyword_occurrences(user_id, keyword, 1)
    # return "[say the keyword]"

@mcp.tool()
def set_keyword(keyword: str) -> str:
    """
    set the keyword for the user

    Args:
        keyword (str): The keyword to set.

    Returns:
        str: The keyword that was set.
    """
    set_db_keyword(user_id, keyword)
    return f"Notification key word set to {keyword}"

@mcp.tool()
def get_keyword() -> str:
    """
    get the current keyword for the user

    Returns:
        str: The current keyword.
    """
    keyword = get_current_keyword(user_id)
    if keyword is None:
        return "No keyword set, do not use the play_notification tool until the user sets a keyword"
    return f"Current Keyword is {keyword}"

@mcp.tool()
def get_keyword_count(keyword: str) -> str:
    """
    get the number of times the keyword has been mentioned for the current user

    Args:
        keyword (str): The keyword to get the count for.

    Returns:
        str: The number of times the keyword has been mentioned by the user.
    """
    num_times = get_keyword_occurrences(user_id, keyword)
    return f"The keyword has been mentioned {num_times} times"

@mcp.tool()
def get_total_keyword_count(keyword: str) -> str:
    """
    get the total number of times the keyword has been mentioned by all users

    Args:
        keyword (str): The keyword to get the count for.

    Returns:
        str: The number of times the keyword has been mentioned by all users.
    """
    num_times = get_total_keyword_occurrences(keyword)
    return f"The keyword has been mentioned a total of {num_times} times"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
