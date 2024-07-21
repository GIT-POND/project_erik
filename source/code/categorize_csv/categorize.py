import pandas as pd
import string
import re
import os

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

"""
----------------------------
    READ SUPPORT FILES
----------------------------
"""

# Load keyword files for each category
def load_keywords(file_name):
    file_path = getFileDir(file_name)
    return pd.read_csv(file_path)['Name'].tolist()

food_keywords = load_keywords('htx_fast_food.csv')
clothes_keywords = load_keywords('htx_clothing_stores.csv')
supplies_keywords = load_keywords('htx_beauty_supply_stores.csv')
transport_keywords = load_keywords('htx_gas_stations.csv')

# Combine all keywords with their corresponding categories
keywords = {
    'food': food_keywords,
    'clothes': clothes_keywords,
    'supplies': supplies_keywords,
    'transport': transport_keywords
}

"""
----------------------------
    CLEAN INPUT DATA
----------------------------
"""

# Function to preprocess the description
def preprocess_description(description):
    description = description.lower()  # Convert to lowercase
    description = re.sub(r"\'([a-zA-Z])", r"\1", description) # Remove single quotations followed by an alphabetical character
    description = re.sub(f'[{string.punctuation}]', '', description)  # Remove punctuation
    description = re.sub(r'\d+', '', description)  # Remove numbers
    description = re.sub(r'\s+', ' ', description).strip()  # Remove extra whitespace
    return description

"""
----------------------------
    RUN CATEGORIZATION
----------------------------
"""

# Function to categorize the description using keyword similarity
# def categorize_description(description):
#     description = preprocess_description(description)
#     max_similarity = 0
#     best_category = 'other'
    
#     for category, words in keywords.items():
#         corpus = words + [description]
#         vectorizer = CountVectorizer().fit_transform(corpus)
#         vectors = vectorizer.toarray()
#         similarity_matrix = cosine_similarity(vectors)
#         similarity = similarity_matrix[-1][:-1].max()
        
#         if similarity > max_similarity:
#             max_similarity = similarity
#             best_category = category
            
#     return best_category

def categorize_description(description):
    description = preprocess_description(description)
    for category, words in keywords.items():
        for word in words:
            if word in description:
                return category
    return 'other'

def main():
    input_file = getFileDir("raw_output.csv")
    output_file = getOutputPath("categorized_output.csv")

    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Filter out rows with a value in the "Credit" column
    df = df[df['Credits'].isna()]

    # Categorize the descriptions
    df['Category'] = df['Description'].apply(categorize_description)

    # Write the output to a new CSV file

    df.to_csv(output_file, index=False)

    print(f"Categorized CSV file has been saved to {output_file}")