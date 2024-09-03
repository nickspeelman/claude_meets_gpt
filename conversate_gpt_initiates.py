from datetime import datetime
from time import sleep
import sys
import os
from io import BytesIO
from pydub import AudioSegment
from claude import AnthropicChat  # Import new class
from gpt import send_gpt_message  # Import the GPT message function
from text_to_speech import text_to_speech  # Import the TTS function

# Set models and other varialbles
gpt_model = "gpt-4"
claude_model = "claude-3-5-sonnet-20240620"
claude_max_tokens = 8192
sleep_param = 10 # Throttles the API requests
temp = 1.0
iterations = 20 # Define the number of back-and-forth cycles
generate_voice = False  # Set to True to generate voice, False to skip


# Define voice IDs for ElevenLabs TTS
claude_voice_id = "iP95p4xoKVk53GoZ742B"
gpt_voice_id = "XrExE9yKIg1WjnnlVkGX"



# Get the name of the current script
current_script_name = os.path.basename(__file__)

# Create an instance of AnthropicChat
claude_chat = AnthropicChat(model=claude_model, max_tokens=claude_max_tokens, temperature=temp)

# Set input and parameters

# Introduces the chat to the first model
with open('inputs/gpt_initial_input.txt', 'r', encoding='utf-8') as file:
    initial_input = file.read().strip()

# Notifies the first model the conversation is nearing completion
with open('inputs/gpt_interupt_input.txt', 'r', encoding='utf-8') as file:
    interupt_input = file.read().strip()

# Final notice that conversatin is ending
with open('inputs/gpt_final_interupt_input.txt', 'r', encoding='utf-8') as file:
    final_interupt_input = file.read().strip()

# Claude refuses to talk to GPT unless a human introduces them
with open('inputs/gpt_claude_reassurance_input.txt', 'r', encoding='utf-8') as file:
    reassurance_input = file.read().strip()
with open('inputs/gpt_topic_input.txt', 'r', encoding='utf-8') as file:
    topic = file.read().strip()


# Combine initial input and topic for GPT's initial message
input_text = initial_input + ' ' + topic

# Get current timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M")

# Filename based on timestamp
base_filename = f"logs/{timestamp}_conversation"
text_filename = f"{base_filename}.txt"
audio_filename = f"{base_filename}.mp3"

# Initialize conversation history for GPT
gpt_messages = [{"role": "user", "content": input_text}]

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

    # Start with GPT sending the initial input
    gpt_response, gpt_messages = send_gpt_message(input_text, gpt_messages, gpt_model, temperature=temp)

    # Append reassurance input to GPT's first response for Claude
    first_response_for_claude = reassurance_input + ' ' + gpt_response

    file.write(f"GPT:\n{gpt_response}\n\n")
    print('GPT:', gpt_response)

    # Convert GPT's response to speech and add to final audio if generating voice
    if generate_voice:
        gpt_audio = text_to_speech(gpt_response, gpt_voice_id)
        final_audio += AudioSegment.from_file(BytesIO(gpt_audio), format="mp3")

    # Iteratively exchange messages between GPT and Claude
    counter = 0
    while counter < iterations:
        # Pause
        sleep(sleep_param)

        # Get response from Claude with retry mechanism
        if counter == 0:
            # For the first interaction, use the reassured response
            claude_response = send_message_with_retry(first_response_for_claude)
        else:
            claude_response = send_message_with_retry(gpt_response)

        file.write(f"Claude:\n{claude_response}\n\n")
        print('Claude:', claude_response)

        # Convert Claude's response to speech and add to final audio if generating voice
        if generate_voice:
            claude_audio = text_to_speech(claude_response, claude_voice_id)
            final_audio += AudioSegment.from_file(BytesIO(claude_audio), format="mp3")

        # Pause
        sleep(sleep_param)

        # Get response from GPT, maintaining conversation history
        if counter == iterations - 2:
            gpt_response, gpt_messages = send_gpt_message(interupt_input + ' ' + claude_response, gpt_messages, gpt_model, temperature=temp)
        elif counter == iterations - 1:
            gpt_response, gpt_messages = send_gpt_message(final_interupt_input + ' ' + claude_response, gpt_messages, gpt_model, temperature=temp)
        else:
            gpt_response, gpt_messages = send_gpt_message(claude_response, gpt_messages, gpt_model, temperature=temp)

        # Write and print GPT's response
        file.write(f"GPT:\n{gpt_response}\n\n")
        print('GPT:', gpt_response)

        # Convert GPT's response to speech and add to final audio if generating voice
        if generate_voice:
            gpt_audio = text_to_speech(gpt_response, gpt_voice_id)
            final_audio += AudioSegment.from_file(BytesIO(gpt_audio), format="mp3")

        counter += 1

# Save final audio to file in the logs folder with the same base name as the text log if generating voice
if generate_voice:
    final_audio.export(audio_filename, format="mp3")
    print(f"Audio saved to {audio_filename}")

print(f"Conversation saved to {text_filename}")
