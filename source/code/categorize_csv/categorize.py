import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from categorize_csv.helpers import getSupportFileDir, getOutputFilesPath, format_string, format_strip_prefix_postfix, get_keywords
from misc.main import print_loading_bar

# Load keyword files for each category
def load_keywords(file_name):
    file_path = getSupportFileDir(file_name)
    return pd.read_csv(file_path)['Name'].tolist()

food_keywords = load_keywords('fast_food_keywords.csv')
clothes_keywords = load_keywords('clothing_stores_keywords.csv')
supplies_keywords = load_keywords('beauty_supply_stores_keywords.csv')
transport_keywords = load_keywords('gas_stations_keywords.csv')
transfer_keywords = load_keywords('money_transfer.csv')

# Combine all keywords with their corresponding categories
keywords = {
    'transfer': transfer_keywords,
    'food': food_keywords,
    'transport': transport_keywords,
    'supplies': supplies_keywords,
    'clothes': clothes_keywords,
}


"""
----------------------------
    RUN CATEGORIZATION
----------------------------
"""
def tokenize(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

def categorize_description(description):
    processed_description = format_string(format_strip_prefix_postfix(description))

    tokens = tokenize(processed_description)
    best_category = None
    max_matches = 0

    for category, keyword_set in keywords.items():
        count = Counter(tokens)
        matches = sum(count[keyword] for keyword in keyword_set)

        if matches > max_matches:
            max_matches = matches
            best_category = category

    return best_category
    

"""
----------------------------
    RUN MAIN
----------------------------
"""
def main():
    input_file = getOutputFilesPath("raw_output.csv")
    output_file = getOutputFilesPath("categorized_output.csv")
    output_totals = getOutputFilesPath("categorized_Totals.csv")

    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Filter out rows with a value in the "Credit" column
    df = df[df['Credits'].isna()]

    # Categorize the descriptions
    total = len(df)
    df['Category'] = None

    for i, idx in enumerate(df.index):
        try:
            df.at[idx,'Category'] = categorize_description(df.at[idx,'Description'])
            print_loading_bar(i + 1, total, prefix='Categorizing:', suffix='Complete', length=50)
        except:
            print('')

    
    # Calculate Category Totals
    category_totals = df.groupby('Category')['Debits'].sum().reset_index()

    totals_row = pd.DataFrame({
        'Date': '',
        'Credits': category_totals['Category'] ,
        'Debits': ['Total'] * len(category_totals),
        'Balance': category_totals['Debits'],
        'Description': '',
        'Category': ''
    })

    # Write the output to a new CSV file

    final_df = pd.concat([df,totals_row], ignore_index=True)

    df.to_csv(output_file, index=False)
    final_df.to_csv(output_totals, index=False)

    # print(f"\n\nCategorized data written to: {output_file}\n\n")