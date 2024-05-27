import re


def remove_text_in_angle_brackets(text):
    # Define the regular expression pattern
    pattern = r'<([^>]*)>'
    # Use re.sub() to replace text within angle brackets with an empty string
    return re.sub(pattern, '', text)
