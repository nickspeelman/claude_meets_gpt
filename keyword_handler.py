def check_termination(response, termination_keyword):
    """
    Checks if the termination keyword is present in the response.
    If found, it logs and terminates the conversation.

    Args:
        response: The response from the agent.
        termination_keyword: The keyword indicating the conversation should end.

    Returns:
        bool: True if the termination keyword is found, False otherwise.
    """
    if termination_keyword in response:
        print(f"Termination keyword '{termination_keyword}' detected.")
        return True
    return False

def check_input(response, input_keyword):
    """
    Checks if the response contains the input keyword.

    Args:
        response (str): The response to check.
        input_keyword (str): The keyword to check for user input request.

    Returns:
        bool: True if the input keyword is found, False otherwise.
    """
    if response is None:
        return False  # If response is None, don't proceed further

    return input_keyword in response
