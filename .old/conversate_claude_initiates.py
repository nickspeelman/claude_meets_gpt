from datetime import datetime
from time import sleep
import sys
import os
from io import BytesIO
from pydub import AudioSegment
from claude import AnthropicChat  # Import new class
from gpt import send_gpt_message  # Introduce GPT function
from text_to_speech import text_to_speech  # Import the TTS function

# Set models
gpt_model = "gpt-4-turbo"
claude_model = "claude-3-5-sonnet-20240620"
claude_max_tokens = 8192
sleep_param = 10 # Throttles API requests
temp = 1.0
iterations = 15 # Defines the number of back-and-forth cycles
generate_voice = False  # Set to True to generate voice, False to skip

# Define voice IDs for ElevenLabs TTS
claude_voice_id = "iP95p4xoKVk53GoZ742B"
gpt_voice_id = "XrExE9yKIg1WjnnlVkGX"

current_script_name = os.path.basename(__file__)

# Create an instance of AnthropicChat
claude_chat = AnthropicChat(model=claude_model, max_tokens=claude_max_tokens, temperature=temp)

# Set input and parameters

# Introduction to the first model
with open('inputs/claude_initial_input.txt', 'r', encoding='utf-8') as file:
    initial_input = file.read().strip()

# Notifies the first model the conversation is coming to an end
with open('inputs/claude_interupt_input.txt', 'r', encoding='utf-8') as file:
    interupt_input = file.read().strip()

# Final notice of conversation coming to an end
with open('inputs/claude_final_interupt_input.txt', 'r', encoding='utf-8') as file:
    final_interupt_input = file.read().strip()

# Create the topic
with open('inputs/claude_topic_input.txt', 'r', encoding='utf-8') as file:
    topic = file.read().strip()



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

# Create empty audio segment for final output if generating voice
if generate_voice:
    final_audio = AudioSegment.empty()

# Function to handle retries for Claude API
def send_message_with_retry(input_text, max_retries=5, backoff_factor=2):
    retry_count = 0
    while retry_count < max_retries:
        response = claude_chat.send_message(input_text)
        if "overloaded_error" not in response:
            return response
        print(f"Claude is overloaded. Retrying in {backoff_factor ** retry_count} seconds...")
        sleep(backoff_factor ** retry_count)
        retry_count += 1
    print("Failed to get a response from Claude after several retries. Exiting program.")
    sys.exit(1)

# Open the file in write mode with UTF-8 encoding
with open(text_filename, 'w', encoding='utf-8') as file:
    # Write header
    file.write(f"Script Name: {current_script_name}\n")
    file.write(f"Timestamp: {timestamp}\n")
    file.write(f"GPT Model: {gpt_model}\n")
    file.write(f"Claude Model: {claude_model}\n")
    file.write(f"Temperature: {temp}\n")
    file.write(f"Topic: {topic}\n")
    file.write(f"Generate Voice: {generate_voice}\n")
    file.write("\n")

    # Get first response from Claude with retry mechanism
    claude_response = send_message_with_retry(input_text)
    file.write(f"Claude:\n{claude_response}\n\n")
    print('Claude:', claude_response)

    # Convert Claude's response to speech and add to final audio if generating voice
    if generate_voice:
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

        # Convert GPT's response to speech and add to final audio if generating voice
        if generate_voice:
            gpt_audio = text_to_speech(gpt_response, gpt_voice_id)
            final_audio += AudioSegment.from_file(BytesIO(gpt_audio), format="mp3")

        # Pause
        sleep(sleep_param)

        # Get response from Claude with retry mechanism
        if counter == iterations - 2:
            claude_response = send_message_with_retry(interupt_input + ' ' + gpt_response)
        elif counter == iterations - 1:
            claude_response = send_message_with_retry(final_interupt_input + ' ' + gpt_response)
        else:
            claude_response = send_message_with_retry(gpt_response)

        # Write and print Claude's response
        file.write(f"Claude:\n{claude_response}\n\n")
        print('Claude:', claude_response)

        # Convert Claude's response to speech and add to final audio if generating voice
        if generate_voice:
            claude_audio = text_to_speech(claude_response, claude_voice_id)
            final_audio += AudioSegment.from_file(BytesIO(claude_audio), format="mp3")

        counter += 1

# Save final audio to file in the logs folder with the same base name as the text log if generating voice
if generate_voice:
    final_audio.export(audio_filename, format="mp3")
    print(f"Audio saved to {audio_filename}")

print(f"Conversation saved to {text_filename}")
