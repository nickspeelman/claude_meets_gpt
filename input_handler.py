from keyword_handler import check_input
from inputs import  input_keyword
from logging_handler import write_to_log
from message_handler import  handle_message

# ** Check for input keyword in initiator's response and handle it **
def handle_input_response(agent_response, agent, agent_handler, message_history, model_config, log_file, temp):
    """
    Handles input requests from the agent.

    If the agent uses the input keyword, prompt the user for input and append the response to the conversation.

    Args:
        agent_response: The current response from the agent.
        agent: The name of the agent requesting input.
        agent_handler: The function or class handling the agent's requests.
        message_history: The conversation history to update.
        model_config: Configuration details for the model.
        log_file: The log file to record the conversation.

    Returns:
        Updated agent response and message history after user input is handled.
    """
    # Check for the input keyword in the agent's response
    if check_input(agent_response, input_keyword):
        # Log and print the response before asking for input
        write_to_log(log_file, agent, agent_response)
        print(f"{agent} is requesting input.")

        # Ask for user input and handle it
        user_input = input("Please provide input: ")
        write_to_log(log_file,"User", user_input)

        # Send the user input back to the agent and get a new response
        agent_response, message_history = handle_message(agent_handler, f"Response from input: {user_input}, please repeat my response for the other agent. Please do not ask for input again on your next message as it will cut the other agent out of the conversation and we want to make sure they can participate.", message_history, model_config, temp)


        # Log and print the new response after the input
        write_to_log(log_file, agent, agent_response)


        # Return the updated response and history; ensure the input keyword is no longer present
        return agent_response, message_history

    # If no input is required, return the original response and history
    return agent_response, message_history

