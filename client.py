from anthropic import AsyncAnthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack
from typing import Optional
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("api_key")
tool_path = os.getenv("tool_path")


system_prompt = """
You have access to two tools:
1. get_notification_keyword — returns the current notification keyword.
2. play_notification — plays a notification sound.

First call the get_notification_keyword tool to get the current notification keyword.
If the keyword is None then disregard the instructions below until the user sets a keyword.
Otherwise, follow the instructions below.

Instructions:
- Every time you mention or refer to the notification keyword, including when summarizing, restate the keyword exactly as returned by get_notification_keyword.
- Whenever you generate the exact notification keyword in your response, immediately pause generation.
- After pausing, call the play_notification tool.
- Wait for the play_notification tool to finish before continuing your response.
- This process must happen every single time you generate the notification keyword, without exception.
- Do not continue until play_notification has completed successfully.

Follow these rules carefully to ensure notifications trigger precisely when the keyword appears in your output.
"""


class MCPClient:
    def __init__(self,user_id):
        """
        Initializes the MCPClient

        Args:
            user_id (int): The user's id.
        """
        self.user_id = user_id
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.available_tools = []
        self.client = AsyncAnthropic(api_key=api_key)

    #connects to the mcp server(tool.py) and initializes the tools
    async def connect_to_mcp_server(self):
        """Connects to the MCP server and initializes the tools"""
        server_params = StdioServerParameters(
            command="python",
            args=[tool_path],
            env={"USER_ID": str(self.user_id)}  # Pass user_id as environment variable
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()

        # print(response.tools)


        self.available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]
        #tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in response.tools])

    async def process_query(self, chat_history: list):
        """
        Processes the user's input and conversation history. Will call the tools if needed.

        Args:
            chat_history (list): The conversation history. With appended user prompt

        Returns:
            list: The response from the tools.
            bool: Whether to prompt the user for another query.
        """
        final_text = " "
        async with self.client.messages.stream(
            model="claude-sonnet-4-0",
            max_tokens=1024,
            tools=self.available_tools,
            system=system_prompt,
            messages=chat_history,
        ) as stream:
            async for event in stream:
                if event.type == 'text':
                    print(event.text, end="", flush=True)
                    final_text += event.text
                elif event.type == "content_block_stop" and event.content_block.type == "tool_use":
                    block = event.content_block
                    if block.type == "tool_use":
                        #print(f"calling tool: {block.name}")
                        tool_id = block.id
                        tool_name = block.name
                        tool_args = block.input
                        result = await self.session.call_tool(tool_name, tool_args)

                        tool_result = ""
                        if len(result.content) == 0:
                            tool_result = " "
                        else:
                            tool_result = result.content[0].text
                        
                        return [
                            {
                                "role": "assistant", 
                                "content": [
                                    {
                                        "citations": [],
                                        "text": final_text,
                                        "type": "text"
                                    },
                                    {
                                        "id": tool_id,
                                        "input": tool_args,
                                        "name": tool_name,
                                        "type": "tool_use"
                                    }
                                ]
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": [
                                            {
                                                "type": "text", 
                                                "text": tool_result
                                            }
                                        ]
                                    }
                                ]
                            }
                        ], False
                        
        return [{"role": "assistant", "content": final_text}], True
        

    async def chat_loop(self):
        """Chat loop that handles the user input and conversation history"""
        print("Type your queries or 'quit' to exit.")

        chat_history = []
        prompt_for_query = True
        while True:
            if prompt_for_query:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                chat_history.append({"role": "user", "content": query})

            response, prompt_for_query = await self.process_query(chat_history)
            chat_history += response

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()