from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from nltk.corpus import stopwords
import numpy as np

try:
    nltk.data.find("taggers/averaged_perceptron_tagger_eng/")
except LookupError:
    nltk.download("averaged_perceptron_tagger_eng")

text = "I enjoy battling my pets in the bd once a day, its a good strategy to earn your nps. you can battle your P2s in the p2 arena but we are waiting for a way to battle p3s!"
text_2 = "I am enjoying my daily battle with my pet in the battle dome! the battledome is a great approach to earn neopoints. You can also battle pet pets in the p2 arena! you are not able to battle petpetpets yet though, but I am happy to wait"

# tokenize and make lowercase
words = word_tokenize(text.lower())
words_2 = word_tokenize(text_2.lower())

# create dictionaries to enable conversion of acronyms and common synonyms, 
# then replace values 
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


def replace_values(list_of_words, dict): 
    '''
    Replace specific elements in a list with new items based on a dictionary mapping.

    Parameters
    ----------
    tokenised_text : list
        The list of tokens to be modified in place.
    dict : dict
        A dictionary where:
         - keys are items to search for 
         - values are lists of items to insert

    Returns
    -------
    None
        The function modifies the input list directly and does not return a new list.
    '''
    for key, value in dict.items():
        if key in list_of_words:
            index = list_of_words.index(key)
            list_of_words[index:index+1] = value


def replace_acronyms_and_synonyms(list_of_words):
    '''
    Replace acronyms and synonyms in a list of words in-place.

    Parameters
    ----------
    words : list of str
        The list of words to be modified in-place using predefined 
        acronym and synonym mappings.

    Returns
    -------
    None
        The function modifies the input list directly.
    '''
    replace_values(list_of_words, acronyms)
    replace_values(list_of_words, synonyms)


replace_acronyms_and_synonyms(words)
replace_acronyms_and_synonyms(words_2)

# remove stopwords and non alphanumeric (e.g. punctuation, and make lowercase) 
sw = stopwords.words('english')
words_filtered = [word.lower() for word in words if word.lower() not in sw and word.isalnum()]
words_filtered_2 = [word.lower() for word in words_2 if word.lower() not in sw and word.isalnum()]

def get_wordnet_pos(treebank_tag):
    '''
    Map a Penn treebank part-of-speech (POS) tag to a WordNet POS constant.

    This is to counteract the default behaviour of get_wordnet_pos which 
    is used later in this package and will defaults to tagging words as 
    nouns, leading to issues with lemmatisation whereby words that are not 
    nouns are not lemmatised. 

    Parameters
    ----------
    treebank_tag : str
        The Penn treebank part-of-speech tag.

    Returns
    -------
    str
        The corresponding WordNet POS constant (adjective, verb, noun, or adverb).
    '''

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatise_words(words): 
    lemmatizer = WordNetLemmatizer()

    tagged_tokens = nltk.pos_tag(words)

    lemmatised_words = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag)) 
        for word, tag in tagged_tokens
    ]

    return lemmatised_words


lemmatised_words = lemmatise_words(words_filtered)
lemmatised_words_2 = lemmatise_words(words_filtered_2)

# remove duplicated words before comparison
lemmatised_words = np.unique(lemmatised_words).tolist()
lemmatised_words_2 = np.unique(lemmatised_words_2).tolist()

# compare lists
# turn word list 1 into a series for easier comparison against word list 2
lemmatised_dataframe = pd.DataFrame(data=lemmatised_words, columns=['words'])

# compare list 1 against list 2 
lemmatised_dataframe['match'] = lemmatised_dataframe.isin(lemmatised_words_2)

# produce a "match" rate
length = len(lemmatised_dataframe)
matches = lemmatised_dataframe['match'].value_counts()
match_rate = matches[True]

# convert match rate to a percent
match_rate_as_percent = round((match_rate / length) * 100, 2)

# format and print
print(f'Match rate: {match_rate_as_percent}%')
print(lemmatised_dataframe)
