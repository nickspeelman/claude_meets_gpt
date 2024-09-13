from time import sleep
def send_message_with_retry(chat_instance, conversation, max_retries=3, backoff_factor=2):
    """
    Sends a message to the Claude API with retry logic for handling errors or unsuccessful responses.

    Args:
        chat_instance (AnthropicChat): The Claude chat instance to use for sending messages.
        conversation (list): The conversation history to send.
        max_retries (int): Maximum number of retry attempts. Defaults to 3.
        backoff_factor (int): Factor for exponential backoff in retries. Defaults to 2.

    Returns:
        str: The response from the Claude API, or None if unsuccessful after retries.
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = chat_instance.send_message(conversation)
            if response:
                return response
            else:
                print(f"Attempt {retry_count + 1}: Received empty or unsuccessful response.")
        except Exception as e:
            print(f"Attempt {retry_count + 1}: Error sending message to Claude - {e}")

        # Exponential backoff
        sleep(backoff_factor ** retry_count)
        retry_count += 1

    print("Exceeded maximum retries. Exiting conversation.")
    return None
