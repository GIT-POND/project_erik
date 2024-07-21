import pandas as pd
import re
from categorize_csv.helpers import getFileDir, getOutputPath, format_string, format_strip_prefix_postfix


# Load keyword files for each category
def load_keywords(file_name):
    file_path = getFileDir(file_name)
    return pd.read_csv(file_path)['Name'].tolist()

food_keywords = load_keywords('htx_fast_food.csv')
clothes_keywords = load_keywords('htx_clothing_stores.csv')
supplies_keywords = load_keywords('htx_beauty_supply_stores.csv')
transport_keywords = load_keywords('htx_gas_stations.csv')
transfer_keywords = load_keywords('money_transfer.csv')

# Combine all keywords with their corresponding categories
keywords = {
    'transfer': transfer_keywords,
    'food': food_keywords,
    'clothes': clothes_keywords,
    'supplies': supplies_keywords,
    'transport': transport_keywords
}


"""
----------------------------
    RUN CATEGORIZATION
----------------------------
"""

def find_pattern(description, keyword):
    regex_pattern = re.escape(keyword).replace(r'\*', '.*')
    return bool(re.search(regex_pattern, description))

def categorize_description(description):
    description = format_string(format_strip_prefix_postfix(description))
    print('::> ',description)
    for category, words in keywords.items():
        for word in words:
            if find_pattern(description, word):
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