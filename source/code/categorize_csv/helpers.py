import os
import re
import nltk
import string
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def getSupportFileDir(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "support_files")

    return os.path.join(file_dir, file_name)

def getOutputFilesPath(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "output_files")

    return os.path.join(file_dir, file_name)

def getOutputSupportFilesPath(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "support_files")

    return os.path.join(file_dir, file_name)

# Function to preprocess the description
def format_string(description):
    description = description.lower()  # Convert to lowercase
    description = re.sub(r"\'([a-zA-Z])", r"\1", description) # Remove single quotations followed by an alphabetical character
    description = re.sub(f'[{string.punctuation}]', ' ', description)  # Remove punctuation
    description = re.sub(r'\d+', ' ', description)  # Remove numbers
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

def preprocess(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text

def get_keywords(file_name, output_file_name='',top_n=100):
    nltk.download('punkt')
    nltk.download('stopwords')

    file_path = getSupportFileDir(file_name)

    df = pd.read_csv(file_path)

    df['processed_text'] = df.iloc[:, 0].apply(preprocess)
    df['tokens'] = df['processed_text'].apply(word_tokenize)

    stop_words = set(stopwords.words('english'))
    df['keywords'] = df['tokens'].apply(lambda x: [word for word in x if word not in stop_words])

    all_keywords = [word for keywords in df['keywords'] for word in keywords]
    keyword_counts = Counter(all_keywords)

    most_common_keywords = keyword_counts.most_common(top_n)

    #output to file
    if output_file_name != '':
        new_df = pd.DataFrame([keyword for keyword,count in most_common_keywords], columns=['keyword'])
        output_file_path = getOutputSupportFilesPath(output_file_name)
        new_df.to_csv(output_file_path, index=False)

    return [keyword for keyword, count in most_common_keywords]