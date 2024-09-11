def load_template(file_path, replacements):
    """
    Load a template file and replace placeholders with actual values.

    Args:
        file_path (str): The path to the template file.
        replacements (dict): A dictionary of replacements to be made in the file.

    Returns:
        str: The content of the file with replacements made.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Debug: Print the original content
    # print(f"Original content from {file_path}:")
    # print(content)

    for key, value in replacements.items():
        # Debug: Print the current replacement being made
        # print(f"Replacing {{{{{key}}}}} with {value}")
        content = content.replace(f'{{{key}}}', value)

    # Debug: Print the final content
    # print("Content after replacements:")
    # print(content)

    return content
