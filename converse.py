import sys
from datetime import datetime
from config_loader import get_model_config
from message_handler import handle_message
from logging_handler import initialize_log_file, write_to_log, close_log_file
from audio_handler import process_audio_if_enabled
from agent_handler import get_agent_handler
from keyword_handler import check_termination
from inputs import human, initiator, interlocutor, initial_input, interupt_input, final_interupt_input, reassurance_input, termination_keyword, input_keyword
from time import sleep
from claude import AnthropicChat
from input_handler import handle_input_response

# Set parameters
sleep_param = 10
temp = 1.0
iterations = 12
generate_voice = False

# Load configurations for both models
initiator_config = get_model_config(initiator)
interlocutor_config = get_model_config(interlocutor)

# Extract specific model details for the initiator and interlocutor
initiator_model_name = initiator_config['models']['default']
interlocutor_model_name = interlocutor_config['models']['default']

# Get model details for both initiator and interlocutor
initiator_model = initiator_config['models'][initiator_model_name]
interlocutor_model = interlocutor_config['models'][interlocutor_model_name]

# Access voice_id directly from the top-level config, not from the models
initiator_voice_id = initiator_config['voice_id']
interlocutor_voice_id = interlocutor_config['voice_id']

# Ensure we have voice_id for both models
if initiator_voice_id is None:
    raise KeyError(f"Voice ID is missing for initiator model: {initiator_model_name}")
if interlocutor_voice_id is None:
    raise KeyError(f"Voice ID is missing for interlocutor model: {interlocutor_model_name}")

# Create chat instance for Claude if necessary
claude_chat_instance = None
if initiator == "Claude":
    claude_chat_instance = AnthropicChat(model=initiator_model['model_id'], max_tokens=initiator_model['max_tokens'], temperature=temp)
elif interlocutor == "Claude":
    claude_chat_instance = AnthropicChat(model=interlocutor_model['model_id'], max_tokens=interlocutor_model['max_tokens'], temperature=temp)

# Get user input for topic
topic = "I'd like the two of you to discuss " + input("What would you like them to discuss? ")

# Combine input and topic for the initial message to the initiator
input_text = initial_input + ' ' + topic

# Initialize log file
text_filename = f"logs/{datetime.now().strftime('%Y%m%d%H%M')}_conversation_{human}.txt"
log_file = initialize_log_file(text_filename, initiator, interlocutor, temp, topic, generate_voice)

# Initialize conversation history
message_history = []

# Start the conversation with the initiator
initiator_handler = get_agent_handler(initiator, claude_chat_instance)  # Pass claude_chat_instance for Claude
initiator_response, message_history = handle_message(
    initiator_handler, input_text, message_history, initiator_model, temp
)




# Handle initiator's input keyword if present
initiator_response, message_history = handle_input_response(initiator_response, initiator, initiator_handler, message_history, initiator_model, log_file, temp)

# Write to log and process audio for the initiator's response
write_to_log(log_file, initiator, initiator_response)
initiator_audio = process_audio_if_enabled(initiator_response, initiator_voice_id, generate_voice)

# Check for termination after the first response
if check_termination(initiator_response, termination_keyword):
    print(f"Termination keyword found in initiator's response, exiting after logging.")
    close_log_file(log_file)
    sys.exit(0)

# Main conversation loop
counter = 0
while counter < iterations:
    sleep(sleep_param)

    # Prepare next message
    if counter == 0:
        next_message = reassurance_input + ' ' + initiator_response
    elif counter == iterations - 2:
        next_message = interupt_input + ' ' + initiator_response
    elif counter == iterations - 1:
        next_message = final_interupt_input + ' ' + initiator_response
    else:
        next_message = initiator_response

    # Interlocutor's turn
    interlocutor_handler = get_agent_handler(interlocutor, claude_chat_instance)  # Ensure the correct handler is returned
    interlocutor_response, message_history = handle_message(
        interlocutor_handler, next_message, message_history, interlocutor_model, temp
    )

    # Handle interlocutor's input keyword if present
    interlocutor_response, message_history = handle_input_response(interlocutor_response, interlocutor, interlocutor_handler, message_history, interlocutor_model, log_file, temp)

    # Write to log and process audio for the interlocutor's response
    write_to_log(log_file, interlocutor, interlocutor_response)
    interlocutor_audio = process_audio_if_enabled(interlocutor_response, interlocutor_voice_id, generate_voice)

    # Check for termination
    if check_termination(interlocutor_response, termination_keyword):
        print(f"Termination keyword found in interlocutor's response, exiting after logging.")
        close_log_file(log_file)
        break

    # Initiator's turn
    initiator_response, message_history = handle_message(
        initiator_handler, interlocutor_response, message_history, initiator_model, temp
    )

    # Handle initiator's input keyword if present
    initiator_response, message_history = handle_input_response(initiator_response, initiator, initiator_handler, message_history, initiator_model, log_file, temp)

    # Write to log and process audio for the initiator's response
    write_to_log(log_file, initiator, initiator_response)
    initiator_audio = process_audio_if_enabled(initiator_response, initiator_voice_id, generate_voice)

    # Check for termination
    if check_termination(initiator_response, termination_keyword):
        print(f"Termination keyword found in new initiator's response, exiting after logging.")
        close_log_file(log_file)
        break

    counter += 1

# Close log file
close_log_file(log_file)
print(f"Conversation saved to {text_filename}")
