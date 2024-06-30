# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 19:42:22 2024

@author: tanoo
"""

import pandas as pd
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load keyword files for each category
def load_keywords(file_name):
    file_path = "C:/Users/tanoo/OneDrive/Desktop/project_erik-1/source/keyword_csv_files/"
    return pd.read_csv(file_path + file_name)['Name'].tolist()

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

# Function to preprocess the description
def preprocess_description(description):
    description = description.lower()  # Convert to lowercase
    description = re.sub(r"\'([a-zA-Z])", r"\1", description) # Remove single quotations followed by an alphabetical character
    description = re.sub(f'[{string.punctuation}]', '', description)  # Remove punctuation
    description = re.sub(r'\d+', '', description)  # Remove numbers
    description = re.sub(r'\s+', ' ', description).strip()  # Remove extra whitespace
    return description

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

# Read the input CSV file
input_file = "C:/Users/tanoo/OneDrive/Desktop/project_erik-1/source/raw_output.csv"  # Replace with your input file path
df = pd.read_csv(input_file)

# Filter out rows with a value in the "Credit" column
df = df[df['Credits'].isna()]

# Categorize the descriptions
df['Category'] = df['Description'].apply(categorize_description)

# Write the output to a new CSV file
output_file = "C:/Users/tanoo/OneDrive/Desktop/project_erik-1/source/categorized_output.csv" # Replace with your desired output file path
df.to_csv(output_file, index=False)

print(f"Categorized CSV file has been saved to {output_file}")