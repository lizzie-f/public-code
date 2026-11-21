import os 
import pandas as pd

from utils import (
    compare_two_columns)

user = os.getlogin()

data = pd.read_excel(f'C:/Users/{user}/Downloads/mock_data_epa.xlsx')

# create dictionary of paired columns to compare against each other
# values must contain a single entry or script will fail
columns_to_compare = {
    'title': 'second_title', 
    'description': 'second_description', 
    'tags': 'second_tags'
    }

# create dictionaries to enable conversion of domain acronyms and synonyms
acronyms = {
    'p2': ['pet pet'], 
    'p2s': ['pet pets'],
    'p3': ['pet pet pet'],
    'p3s': ['pet pet pets'],
    'np': ['neopoint'],
    'nps': ['neopoints'],
    'bd': ['battledome'],
    }

synonyms = {
    'monthly': ['once', 'a', 'month'], 
    'weekly': ['once', 'a', 'week'], 
    'daily': ['once', 'a', 'day'],
    'battledome': ['battle', 'dome'],
    'petpet': ['pet', 'pet'],
    'petpetpet': ['pet', 'pet', 'pet']
    }

# iterate over columns_to_compare dict to apply compare_two_columns function
for key in columns_to_compare:
    # initialise variables
    value = columns_to_compare.get(key)
    column_name = 'compare_' + key

    data[column_name] = compare_two_columns(
        df=data, 
        column_1=key, 
        column_2=value, 
        acronyms=acronyms, 
        synonyms=synonyms
        )
