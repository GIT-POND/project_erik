# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 19:01:44 2024

@author: tanoo
"""

import pandas as pd
import string
import re

def clean_string(s):
    # Remove single quotations followed by an alphabetical character
    s = re.sub(r"\'([a-zA-Z])", r"\1", s)
    # Remove punctuation
    s = s.translate(str.maketrans('', '', string.punctuation))
    # Remove non-alphabetical characters
    s = re.sub(r'[^a-zA-Z\s]', '', s)
    # Set all strings to lowercase
    s = s.lower()
    # Remove extra spaces
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def clean_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Apply the cleaning function to each string in the dataframe
    for col in df.select_dtypes(include=[object]).columns:
        df[col] = df[col].apply(lambda x: clean_string(str(x)))

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Write the cleaned dataframe back to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Cleaned data has been saved to {output_file}")

path = "C:/Users/tanoo/"
file_dict = {"houston_beauty_supply.csv": "htx_beauty_supply_stores.csv",
             "houston_clothing_stores.csv": "htx_clothing_stores.csv",
             "houston_fast_food.csv": "htx_fast_food.csv",
             "houston_gas_stations.csv": "htx_gas_stations.csv",
             "houston_grocery_stores.csv": "htx_grocery_stores.csv",
             "houston_resturants.csv": "htx_resturants.csv"
            }

for input_file, output_file in file_dict.items():
    clean_csv(path + input_file, path + output_file)
