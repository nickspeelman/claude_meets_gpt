import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("ANTHROPHIC_API_KEY")

API_URL = "https://api.anthropic.com/v1/messages"

headers = {
    "x-api-key": API_KEY,
    "content-type": "application/json",
    "anthropic-version": "2023-06-01"
}

class AnthropicChat:
    def __init__(self, model="claude-3-sonnet-20240229", max_tokens=4096, temperature=0.5):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.conversation_history = []

    def send_message(self, message):
        # Format the new user message correctly as per API requirements
        user_message = {"role": "user", "content": [{"type": "text", "text": message}]}

        # Add the new user message to the conversation history
        self.conversation_history.append(user_message)

        # Prepare the data payload for the API
        data = {
            "messages": self.conversation_history,
            "model": self.model,
            "max_tokens": self.max_tokens
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            # Extract the assistant's message correctly
            assistant_message_content = response.json()['content']

            # Check if the response content is in the expected format
            if isinstance(assistant_message_content, list) and len(assistant_message_content) > 0:
                assistant_message = assistant_message_content[0]['text']

                # Format the assistant's response
                assistant_message_obj = {"role": "assistant", "content": [{"type": "text", "text": assistant_message}]}

                # Add Claude's response to the conversation history
                self.conversation_history.append(assistant_message_obj)
                return assistant_message
            else:
                return "Error: Received unexpected response format from Claude."
        else:
            return f"Error: {response.status_code}, {response.text}"

    def clear_history(self):
        self.conversation_history = []
