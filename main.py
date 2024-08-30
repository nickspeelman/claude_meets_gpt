from datetime import datetime
from time import sleep
import sys
from io import BytesIO
from pydub import AudioSegment
from claude import AnthropicChat  # Import our new class
from gpt import send_gpt_message  # Assuming this function exists in a gpt.py file
from text_to_speech import text_to_speech  # Import the TTS function from the separate module

# Set models
gpt_model = "gpt-4-turbo"
claude_model = "claude-3-5-sonnet-20240620"
claude_max_tokens = 8192
sleep_param = 10
temp = 1.0
iterations = 6
topic = "I'd like you two to get to know each other and discuss the future of AI."

# Define voice IDs for ElevenLabs TTS
claude_voice_id = "iP95p4xoKVk53GoZ742B"  # Replace with the actual voice ID
gpt_voice_id = "XrExE9yKIg1WjnnlVkGX"  # Replace with the actual voice ID

# Create an instance of AnthropicChat
claude_chat = AnthropicChat(model=claude_model, max_tokens=claude_max_tokens, temperature=temp)

# Set input and parameters
with open('initial_input.txt', 'r', encoding='utf-8') as file:
    initial_input = file.read().strip()
with open('interupt_input.txt', 'r', encoding='utf-8') as file:
    interupt_input = file.read().strip()
with open('final_interupt_input.txt', 'r', encoding='utf-8') as file:
    final_interupt_input = file.read().strip()

# Combine input and topic
input_text = initial_input + ' ' + topic

# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M")

# Filename based on timestamp
base_filename = f"logs/{timestamp}_conversation"
text_filename = f"{base_filename}.txt"
audio_filename = f"{base_filename}.mp3"

# Initialize conversation history for GPT
gpt_messages = []

# Create empty audio segment for final output
final_audio = AudioSegment.empty()

# Open the file in write mode with UTF-8 encoding
with open(text_filename, 'w', encoding='utf-8') as file:
    # Write header
    file.write(f"Timestamp: {timestamp}\n")
    file.write(f"GPT Model: {gpt_model}\n")
    file.write(f"Claude Model: {claude_model}\n")
    file.write(f"Temperature: {temp}\n")
    file.write(f"Topic: {topic}\n")
    file.write("\n")

    # Get first response from Claude
    claude_response = claude_chat.send_message(input_text)
    # Check for error in Claude's response
    if "Error: 500" in claude_response and "Internal server error" in claude_response:
        print('Claude returned an internal server error. Exiting program.')
        sys.exit(1)

    file.write(f"Claude:\n{claude_response}\n\n")
    print('Claude:', claude_response)

    # Convert Claude's response to speech and add to final audio
    claude_audio = text_to_speech(claude_response, claude_voice_id)
    final_audio += AudioSegment.from_file(BytesIO(claude_audio), format="mp3")

    # Iteratively exchange messages between Claude and GPT
    counter = 0
    while counter < iterations:
        # Pause
        sleep(sleep_param)

        # Get response from GPT, maintaining conversation history
        gpt_response, gpt_messages = send_gpt_message(claude_response, gpt_messages, gpt_model, temperature=temp)
        file.write(f"GPT:\n{gpt_response}\n\n")
        print('GPT:', gpt_response)

        # Convert GPT's response to speech and add to final audio
        gpt_audio = text_to_speech(gpt_response, gpt_voice_id)
        final_audio += AudioSegment.from_file(BytesIO(gpt_audio), format="mp3")

        # Pause
        sleep(sleep_param)

        # Get response from Claude
        if counter == iterations - 2:
            claude_response = claude_chat.send_message(interupt_input + ' ' + gpt_response)
        elif counter == iterations - 1:
            claude_response = claude_chat.send_message(final_interupt_input + ' ' + gpt_response)
        else:
            claude_response = claude_chat.send_message(gpt_response)

        # Check for error in Claude's response
        if "Error: 500" in claude_response and "Internal server error" in claude_response:
            print('Claude returned an internal server error. Exiting program.')
            sys.exit(1)

        # Write and print Claude's response
        file.write(f"Claude:\n{claude_response}\n\n")
        print('Claude:', claude_response)

        # Convert Claude's response to speech and add to final audio
        claude_audio = text_to_speech(claude_response, claude_voice_id)
        final_audio += AudioSegment.from_file(BytesIO(claude_audio), format="mp3")

        counter += 1

# Save final audio to file in the logs folder with the same base name as the text log
final_audio.export(audio_filename, format="mp3")
print(f"Conversation saved to {text_filename}")
print(f"Audio saved to {audio_filename}")
