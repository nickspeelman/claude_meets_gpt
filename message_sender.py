from retry_handler import send_message_with_retry
from gpt import send_gpt_message

def send_message(model, chat_instance, message, message_history=None, model_id=None, max_tokens=None, temperature=1.0):
    """
    Sends a message to the specified model and returns the response.

    Args:
        model (str): The model name ('Claude' or 'ChatGPT').
        chat_instance (AnthropicChat or similar): The instance of the chat model to send messages.
        message (str): The message to send.
        message_history (list, optional): The conversation history for the model. Defaults to None.
        model_id (str, optional): The model ID to use. Defaults to None.
        max_tokens (int, optional): The maximum number of tokens to use. Defaults to None.
        temperature (float, optional): The temperature to use for the model response. Defaults to 1.0.

    Returns:
        tuple: The response and updated message history.
    """
    if message_history is None:
        message_history = []

    if model == "Claude":
        # Send the message using the provided instance
        response = send_message_with_retry(chat_instance, message)

        if response:
            # Append Claude's response to the history
            message_history.append({"role": "assistant", "content": response})
        else:
            print("Received an unsuccessful response from Claude.")

        return response, message_history

    elif model == "ChatGPT":
        response, message_history = send_gpt_message(
            message, message_history,
            model_id,
            temperature=temperature
        )
        return response, message_history

    else:
        raise ValueError(f"Unsupported model: {model}")
