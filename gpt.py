from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  # Ensure the variable name matches your .env file

def send_gpt_message(prompt, messages, model="gpt-4", temperature=0.5):
    # Ensure messages is a list
    if not isinstance(messages, list):
        raise ValueError("The 'messages' parameter must be a list.")

    # Add the new user message to the message history
    messages.append({"role": "user", "content": prompt})

    # Create a streaming completion
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    # Collect the full response content
    response_content = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            response_content += chunk.choices[0].delta.content

    # Add the assistant's response to the message history
    messages.append({"role": "assistant", "content": response_content})

    return response_content, messages

