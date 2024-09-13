from gpt import send_gpt_message

def get_agent_handler(agent_name, claude_chat_instance=None):
    """
    Determines the correct agent handler based on the agent name.

    Args:
        agent_name (str): The name of the agent (e.g., "Claude" or "ChatGPT").
        claude_chat_instance (AnthropicChat, optional): An instance of the AnthropicChat class for Claude.

    Returns:
        callable: The appropriate handler for sending messages to the agent.
    """
    if agent_name == "Claude":
        if claude_chat_instance is None:
            raise ValueError("Claude instance must be provided for Claude as an agent.")
        return claude_chat_instance  # Return the Claude instance (AnthropicChat)
    elif agent_name == "ChatGPT":
        return send_gpt_message  # Return the function to handle GPT messages
    else:
        raise ValueError(f"Unsupported agent: {agent_name}")
