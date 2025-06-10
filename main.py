import asyncio
from app.client import MCPClient
from db.users import *


async def init_chat():
    """Initializes the chat for a user."""
    username = input("\nName: ").strip()
    if username == "":
        print("Name cannot be empty")
        return

    user_id = get_user_id(username)

    if user_id is None:
        print(f"creating user: {username}")
        add_user(username)
        user_id = get_user_id(username)

    

    #start client for user
    client = MCPClient(user_id)
    try:
        await client.connect_to_mcp_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(init_chat())