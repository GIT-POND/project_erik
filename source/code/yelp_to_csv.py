# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 05:34:47 2024

@author: tanoo
"""

import re
import spacy
import nltk
from nltk.corpus import wordnet

# Download NLTK wordnet corpus
#nltk.download('wordnet')

import requests
import pandas as pd

API_KEY = 'your_key'  # Replace this with your Yelp API key
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_LIMIT = 50  # Maximum number of results per request

def search_businesses(api_key, location, term, limit=SEARCH_LIMIT, offset=0):
    url = f'{API_HOST}{SEARCH_PATH}'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'term': term,
        'location': location,
        'limit': limit,
        'offset': offset,
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_business_names(api_key, location, term, max_results=100):
    offset = 0
    business_names = []
    while len(business_names) < max_results:
        response = search_businesses(api_key, location, term, offset=offset)
        businesses = response.get('businesses', [])
        if not businesses:
            break
        for business in businesses:
            business_names.append(business['name'])
        offset += SEARCH_LIMIT
        if len(businesses) < SEARCH_LIMIT:
            break
    return business_names[:max_results]

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Name'])
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    location = 'Houston, TX'
    max_results = 1000
    categories = {
        'beauty_supply': 'Beauty Supply',
        'fast_food': 'Fast Food',
        'gas_stations': 'Gas Stations',
        'clothing_stores': 'Clothing Stores',
        'grocery_stores': 'Grocery Stores'
    }

    for category, term in categories.items():
        business_names = get_business_names(API_KEY, location, term, max_results)
        filename = f'houston_{category}.csv'
        save_to_csv(business_names, filename)
    
    print("done")