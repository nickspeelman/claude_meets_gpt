import os
import sys
from config import config  # Import the configuration dictionary
def get_model_config(model_name):
    """
    Retrieve the configuration for a given model name.

    Args:
        model_name (str): The name of the model to retrieve configuration for.

    Returns:
        dict: The model configuration.
    """
    if model_name in config:
        return config[model_name]
    else:
        print(f"Model {model_name} not found in the configuration.")
        sys.exit(1)
