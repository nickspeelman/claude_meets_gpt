from retry_handler import send_message_with_retry
from claude import AnthropicChat  # Add this import to fix the issue

def send_message(agent, message, history, model_id, max_tokens, temperature):
    """
    Sends a message to either GPT or Claude.

    Args:
        agent (str): The agent to send the message to (e.g., "Claude", "ChatGPT").
        message (str): The message to send.
        history (list): The conversation history.
        model_id (str): The specific model ID for the agent.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): The temperature for response generation.

    Returns:
        tuple: The response and updated conversation history.
    """

    # Check if agent is Claude, and create AnthropicChat instance if necessary
    if agent == "Claude":
        chat_instance = AnthropicChat(model=model_id, max_tokens=max_tokens, temperature=temperature)
        response = send_message_with_retry(chat_instance, message)
    else:
        # Handle ChatGPT (or other agents) here if needed
        response = send_message_with_retry(agent, message)

    # Append the response to the history
    history.append({"role": "assistant", "content": response})

    return response, history
