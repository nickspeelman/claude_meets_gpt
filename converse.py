from datetime import datetime
import sys
import os
from io import BytesIO
from time import sleep
from pydub import AudioSegment
from text_to_speech import text_to_speech  # Import TTS function
from config_loader import get_model_config  # Import configuration loader function
from template_loader import load_template  # Import template loader function
from message_sender import send_message  # Import send_message function
from claude import AnthropicChat  # Import AnthropicChat class

# Define the initiator and interlocutor
initiator = "ChatGPT"  # Change as needed or pass as an argument
interlocutor = "Claude"  # Change as needed or pass as an argument

# Set parameters
sleep_param = 10  # Adjust as necessary
temp = 1.0  # Pass this as needed
iterations = 10  # Number of back-and-forth cycles
human = 'Nick'  # Your name goes here
generate_voice = False  # Change to True to enable voice generation

######## Nothing under here should need to be adjusted #########

# Load configurations for both models
initiator_config = get_model_config(initiator)
interlocutor_config = get_model_config(interlocutor)

# Extract specific model details and set some parameters
initiator_model = initiator_config['models'][initiator_config['models']['default']]
interlocutor_model = interlocutor_config['models'][interlocutor_config['models']['default']]
initiator_model_id = initiator_model['model_id']
interlocutor_model_id = interlocutor_model['model_id']
initiator_max_tokens = initiator_model['max_tokens']
interlocutor_max_tokens = interlocutor_model['max_tokens']

# Define voice IDs for ElevenLabs TTS
initiator_voice_id = initiator_config['voice_id']
interlocutor_voice_id = interlocutor_config['voice_id']

# Load template files and replace placeholders
initial_input = load_template('inputs/initial_input.txt', {'initiator': initiator, 'interlocutor': interlocutor, 'human': human})
interupt_input = load_template('inputs/interupt_input.txt', {'initiator': initiator, 'interlocutor': interlocutor, 'human': human})
final_interupt_input = load_template('inputs/final_interupt_input.txt', {'initiator': initiator, 'interlocutor': interlocutor, 'human': human})
topic = load_template('topic_input.txt', {'initiator': initiator, 'interlocutor': interlocutor, 'human': human})
reassurance_input = load_template('inputs/reassurance_input.txt', {'initiator': initiator, 'interlocutor': interlocutor, 'human': human}) # Claude won't talke to ChatGPT unless a human tells him it's okay.

# Combine input and topic
input_text = initial_input + ' ' + topic

# Get current timestamp for file naming
timestamp = datetime.now().strftime("%Y%m%d%H%M")

# Define file names based on timestamp
base_filename = f"logs/{timestamp}_conversation_{human}"
text_filename = f"{base_filename}.txt"
audio_filename = f"{base_filename}.mp3"

# Initialize conversation history for GPT
message_history = []

# Prepare audio segment for final output if voice generation is enabled
if generate_voice:
    final_audio = AudioSegment.empty()

# Create an instance of AnthropicChat for Claude if it is the initiator or interlocutor
claude_chat_instance = None
if initiator == "Claude":
    claude_chat_instance = AnthropicChat(model=initiator_model_id, max_tokens=initiator_max_tokens, temperature=temp)
elif interlocutor == "Claude":
    claude_chat_instance = AnthropicChat(model=interlocutor_model_id, max_tokens=interlocutor_max_tokens, temperature=temp)

# Open the log file for writing
with open(text_filename, 'w', encoding='utf-8') as file:
    # Write header information
    file.write(f"Timestamp: {timestamp}\n")
    file.write(f"{initiator} Model: {initiator_model_id}\n")
    file.write(f"{interlocutor} Model: {interlocutor_model_id}\n")
    file.write(f"Temperature: {temp}\n")
    file.write(f"Topic: {topic}\n")
    file.write(f"Generate Voice: {generate_voice}\n")
    file.write("\n")

    # Start conversation with initiator
    initiator_response, message_history = send_message(
        initiator, claude_chat_instance, input_text, message_history,
        model_id=initiator_model_id,
        max_tokens=initiator_max_tokens,
        temperature=temp
    )

    if not initiator_response:
        print("Conversation terminated due to repeated unsuccessful responses from initiator.")
        if generate_voice:
            final_audio.export(audio_filename, format="mp3")
            print(f"Partial audio saved to {audio_filename}")
        print(f"Partial conversation saved to {text_filename}")
        sys.exit(1)

    file.write(f"{initiator}:\n{initiator_response}\n\n")
    print(f"{initiator}:", initiator_response)

    # Convert response to speech if enabled
    if generate_voice:
        initiator_audio = text_to_speech(initiator_response, initiator_voice_id)
        final_audio += AudioSegment.from_file(BytesIO(initiator_audio), format="mp3")

    # First interaction for interlocutor with reassurance input appended
    first_interlocutor_message = reassurance_input + ' ' + initiator_response

    # Iterate conversation between models
    counter = 0
    while counter < iterations:
        # Pause to throttle requests
        sleep(sleep_param)

        # Send response to interlocutor (with reassurance input on the first iteration)
        if counter == 0:
            interlocutor_response, message_history = send_message(
                interlocutor, claude_chat_instance, first_interlocutor_message,
                message_history,
                model_id=interlocutor_model_id,
                max_tokens=interlocutor_max_tokens,
                temperature=temp
            )
        else:
            interlocutor_response, message_history = send_message(
                interlocutor, claude_chat_instance, initiator_response,
                message_history,
                model_id=interlocutor_model_id,
                max_tokens=interlocutor_max_tokens,
                temperature=temp
            )

        if not interlocutor_response:
            print("Conversation terminated due to repeated unsuccessful responses from interlocutor.")
            break

        file.write(f"{interlocutor}:\n{interlocutor_response}\n\n")
        print(f"{interlocutor}:", interlocutor_response)

        # Convert interlocutor response to speech if enabled
        if generate_voice:
            interlocutor_audio = text_to_speech(interlocutor_response, interlocutor_voice_id)
            final_audio += AudioSegment.from_file(BytesIO(interlocutor_audio), format="mp3")

        # Pause again for throttling
        sleep(sleep_param)

        # Determine next message
        if counter == iterations - 2:
            next_message = interupt_input + ' ' + interlocutor_response
        elif counter == iterations - 1:
            next_message = final_interupt_input + ' ' + interlocutor_response
        else:
            next_message = interlocutor_response

        initiator_response, message_history = send_message(
            initiator, claude_chat_instance, next_message,
            message_history,
            model_id=initiator_model_id,
            max_tokens=initiator_max_tokens,
            temperature=temp
        )

        if not initiator_response:
            print("Conversation terminated due to repeated unsuccessful responses from initiator.")
            break

        # Write initiator's response to the log
        file.write(f"{initiator}:\n{initiator_response}\n\n")
        print(f"{initiator}:", initiator_response)

        # Convert initiator's response to speech if enabled
        if generate_voice:
            initiator_audio = text_to_speech(initiator_response, initiator_voice_id)
            final_audio += AudioSegment.from_file(BytesIO(initiator_audio), format="mp3")

        counter += 1

# Save the final audio if voice generation is enabled and conversation was not terminated early
if generate_voice and counter == iterations:
    final_audio.export(audio_filename, format="mp3")
    print(f"Audio saved to {audio_filename}")

print(f"Conversation saved to {text_filename}")
