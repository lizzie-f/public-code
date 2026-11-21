import os 
import pandas as pd

user = os.getlogin()

data = pd.read_excel(f'C:/Users/{user}/Downloads/mock_data_epa.xlsx')

from utils import (
    compare_two_columns
)

columns = ['ID', 'URL', 'title', 'description', 'tags', 'second_title', 'second_description', 'second_tags']

# create dictionary of paired columns to compare 
columns_to_compare = {
    'title': 'second_title', 
    'description': 'second_description', 
    'tags': 'second_tags'
}

# create dictionaries to enable conversion of acronyms and common synonyms
acronyms = {
    'p2': ['pet'], 
    'p2s': ['pet'],
    'p3': ['pet'],
    'p3s': ['pet'],
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

data['compare_titles'] = compare_two_columns(
    df=data, 
    column_1='title', 
    column_2='second_title', 
    acronyms=acronyms, 
    synonyms=synonyms
    )

data['compare_descriptions'] = compare_two_columns(
    df=data, 
    column_1='description', 
    column_2='second_description', 
    acronyms=acronyms, 
    synonyms=synonyms
    )

data['compare_tags'] = compare_two_columns(
    df=data, 
    column_1='tags', 
    column_2='second_tags', 
    acronyms=acronyms, 
    synonyms=synonyms
    )
