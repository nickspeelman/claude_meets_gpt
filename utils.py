import config

import config

def get_model_name(model_config):
    # Access the actual config dictionary inside the `config` module
    config_data = config.config

    # Iterate through the config dictionary
    for agent_name, agent_data in config_data.items():
        # Iterate through the models under each agent ("Claude" or "ChatGPT")
        for model_key, model_data in agent_data['models'].items():
            # If the model_config matches the model details, return the agent name
            if model_config == model_data:
                return agent_name

    return None  # If no match is found

