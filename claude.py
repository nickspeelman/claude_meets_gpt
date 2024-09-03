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
        self.conversation_history = []

    def send_message(self, message):
        # Add the new user message to the conversation history
        self.conversation_history.append({"role": "user", "content": message})

        data = {
            "messages": self.conversation_history,
            "model": self.model,
            "max_tokens": self.max_tokens
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            assistant_message = response.json()['content'][0]['text']
            # Add Claude's response to the conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        else:
            return f"Error: {response.status_code}, {response.text}"

    def clear_history(self):
        self.conversation_history = []

