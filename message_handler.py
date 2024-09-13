from utils import get_model_name

def handle_message(agent, message, history, model_config, temperature):
    """
    Handles sending a message to an agent and updating the message history.
    """
    # Check if the agent is a callable (function) like send_gpt_message

    model_name = get_model_name(model_config)

    if callable(agent):
        # For ChatGPT, pass model-specific parameters
        response, history = agent(message, history, model_config['model_id'], temperature=temperature)
    else:
        # For Claude, just call send_message without the extra parameters
        response = agent.send_message(message)
        # Update history manually, if necessary
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})


    print(f"{model_name} response: {response}")

    return response, history
