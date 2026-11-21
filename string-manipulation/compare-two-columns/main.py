import pandas as pd
import os 

user = os.getlogin()

data = pd.read_excel(f'C:/Users/{user}/Downloads/mock_data_epa.xlsx')

from utils import (
    normalise_and_tokenise,
    replace_acronyms_and_synonyms, 
    remove_stopwords_keep_alphanumeric_only, 
    lemmatise_words,
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

# set up variables 
length = len(data)
column_1 = data['description']
column_2 = data['second_description']
lemmatised_match_rate = []

# loop through rows
for i in range(length):
    text = column_1[i]
    text_2 = column_2[i]

    # normalise and tokenise text
    text = normalise_and_tokenise(text)
    text_2 = normalise_and_tokenise(text_2)

    # replace acronyms and synonyms
    text = replace_acronyms_and_synonyms(text, acronyms, synonyms)
    text_2 = replace_acronyms_and_synonyms(text_2, acronyms, synonyms)

    # remove stopwords and any non-alphanumeric entries
    text = remove_stopwords_keep_alphanumeric_only(text)
    text_2 = remove_stopwords_keep_alphanumeric_only(text_2)

    # lemmatise 
    text = lemmatise_words(text)
    text_2 = lemmatise_words(text_2)

    # compare lists
    # turn word list 1 into a temp dataframe for easier comparison with word list 2
    lemmatised_dataframe = pd.DataFrame(data=text, columns=['words'])

    # compare list 1 against list 2 
    lemmatised_dataframe['match'] = lemmatised_dataframe.isin(text_2)

    # produce a "match" rate as a percent
    length = len(lemmatised_dataframe)
    matches = lemmatised_dataframe['match'].value_counts()
    match_rate = matches[True]
    match_rate_as_percent = round((match_rate / length) * 100, 2)

    # convert to float and add result to list
    lemmatised_match_rate.append(float(match_rate_as_percent))

# convert lemmatised_match_rate to column in 'data' dataframe 

data['compare_descriptions'] = lemmatised_match_rate

