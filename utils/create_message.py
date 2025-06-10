def create_message(role, content):
    """
    Creates a message for the chat history.

        Args:
            role (str): The role of the message.
            content (str): The content of the message.

        Returns:
            dict: The message.
    """
    if content == "":
        content = "no result"
    return {"role": role, "content": content}

def create_tool_message(tool, result, prev_message):
    """
    Creates a message for the chat history for the tool call.

        Args:
            tool (dict): The tool object.
            result (dict): The result of the tool call.
            prev_message (str): The previous message.

        Returns:
            list(dict): The tool call and result.
    """
    tool_result = ""
    if len(result.content) == 0:
        tool_result = "no result"
    else:
        tool_result = result.content[0].text
    
    if prev_message == "":
        prev_message = "no result"
    return [
        {
            "role": "assistant", 
            "content": [
                {
                    "citations": [],
                    "text": prev_message,
                    "type": "text"
                },
                {
                    "id": tool.id,
                    "input": tool.input,
                    "name": tool.name,
                    "type": "tool_use"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool.id,
                    "content": [
                        {
                            "type": "text", 
                            "text": tool_result
                        }
                    ]
                }
            ]
        }
    ]
