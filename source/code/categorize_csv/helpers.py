import os
import re
import string

def getFileDir(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "support_files")

    return os.path.join(file_dir, file_name)

def getOutputPath(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "output_files")

    return os.path.join(file_dir, file_name)

# Function to preprocess the description
def format_string(description):
    description = description.lower()  # Convert to lowercase
    description = re.sub(r"\'([a-zA-Z])", r"\1", description) # Remove single quotations followed by an alphabetical character
    description = re.sub(f'[{string.punctuation}]', ' ', description)  # Remove punctuation
    description = re.sub(r'\d+', '', description)  # Remove numbers
    description = re.sub(r'\s+', ' ', description).strip()  # Remove extra whitespace
    return description

def format_strip_prefix_postfix(description):
    processed_words = []
    words = description.split()

    if len(words) > 5:
        processed_words = " ".join(words[2:-3])
    else:
        processed_words = " ".join(words)

    return processed_words