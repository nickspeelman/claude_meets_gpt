import os
import requests
import sys

# Set ElevenLabs API key from environment variable
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech(text, voice_id):
    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    headers = {
        "Accept": "application/json",
        "xi-api-key": elevenlabs_api_key
    }

    # Define the data payload for the API request
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # Ensure this matches your requirements
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Debugging output to check what is being sent

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error with text-to-speech conversion: {response.status_code}, {response.text}")
        sys.exit(1)
