# logging_handler.py

def initialize_log_file(filename, initiator, interlocutor, temperature, topic, generate_voice):
    """
    Initializes a log file with the appropriate headers and metadata.
    """
    file = open(filename, 'w', encoding='utf-8')
    file.write(f"Initiator: {initiator}\n")
    file.write(f"Interlocutor: {interlocutor}\n")
    file.write(f"Temperature: {temperature}\n")
    file.write(f"Topic: {topic}\n")
    file.write(f"Generate Voice: {generate_voice}\n")
    file.write("\n")
    return file

def write_to_log(file, agent, response):
    """
    Writes the conversation to the log file.
    """
    file.write(f"{agent}:\n{response}\n\n")

def close_log_file(file):
    """
    Closes the log file after writing all the conversation data.
    """
    file.close()

def check_termination(response, termination_keyword):
    """
    Checks if the response contains the termination keyword.
    """
    return termination_keyword in response
