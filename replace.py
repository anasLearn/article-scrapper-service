import re


def remove_text_in_angle_brackets(text):
    # Define the regular expression pattern
    pattern = r'<([^>]*)>'
    # Use re.sub() to replace text within angle brackets with an empty string
    return re.sub(pattern, '', text)


def main():
    file_path = 'article.txt'  # Path to your text file
    try:
        with open(file_path, 'r') as file:
            # Read the contents of the file
            content = file.read()

        # Remove text within angle brackets
        modified_content = remove_text_in_angle_brackets(content)

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)

        print("Text within angle brackets removed successfully!")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")


if __name__ == "__main__":
    main()
