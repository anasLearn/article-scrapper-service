import re


def remove_text_in_angle_brackets(text):
    # Define the regular expression pattern
    pattern_1 = r'<([^>]*)>'
    # Use re.sub() to replace text within angle brackets with an empty string
    cleaned_text = re.sub(pattern_1, '', text)

    return cleaned_text


def remove_figure_tags(html_content):
    # Regular expression to match everything between <figure> and </figure> tags
    cleaned_content = re.sub(r'<figure.*?</figure>', '', html_content, flags=re.DOTALL)
    return cleaned_content
