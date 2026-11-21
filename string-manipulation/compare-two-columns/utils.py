import re

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pandas as pd

try:
    nltk.data.find("taggers/averaged_perceptron_tagger_eng/")
except LookupError:
    nltk.download("averaged_perceptron_tagger_eng")


def normalise_and_tokenise(text):
    '''
    Normalise punctuation and tokenise text into lowercase words.

    Replaces hyphens, en dashes, em dashes, and forward slashes with spaces,
    converts characters to lowercase, and splits the result into tokens using
    ``word_tokenize``. Non-string inputs return an empty list.

    Parameters
    ----------
    text : str or Any
        Input value to normalise and tokenise. If ``text`` is not a ``str``,
        an empty list is returned.

    Returns
    -------
    list of str
        Lowercase tokens extracted from ``text``, or ``[]`` if ``text`` is
        not a string.
    '''
    # Handle non-string variables 
    if not isinstance(text, str):
        return []

    # Substitute hyphens, en dashes, em dashes, and forward slashes with a space
    cleaned = re.sub(r"[-–—/]", " ", text)

    # Tokenise and make lowercase
    return word_tokenize(cleaned.lower())

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
    list of str
        New list with replaced values from dict if applicable.
    '''
    for key, value in dict.items():
        if key in list_of_words:
            index = list_of_words.index(key)
            list_of_words[index:index+1] = value
    return list_of_words

def replace_acronyms_and_synonyms(list_of_words, *dicts):
    '''
    Replace acronyms and synonyms in a list of words in-place.

    Parameters
    ----------
    words : list of str
        The list of words to be modified in-place using predefined 
        acronym and synonym mappings.
    *dicts : dict of {str: str}
        One or more mapping dictionaries applied in order.

    Returns
    -------
    list of str
        New list with replaced values from *dicts if applicable.
    '''
    for dict in dicts:
            replace_values(list_of_words, dict)
    return list_of_words

def remove_stopwords_keep_alphanumeric_only(words):
    '''
    Remove English stopwords and non-alphanumeric tokens from a list of words.

    Parameters
    ----------
    words : list of str
        List of words to filter and lowercase.

    Returns
    -------
    list of str
        New list containing lowercased alphanumeric words not in the English
        stopword list.
        
    '''
    
    sw = stopwords.words('english')
    words_filtered = [word.lower() for word in words if word.lower() not in sw and word.isalnum()]
    return words_filtered

def remove_stopwords_keep_alphanumeric_only(words):
    '''
    Remove English stopwords and non-alphanumeric tokens from a list of words.

    Parameters
    ----------
    words : list of str
        List of words to filter and lowercase.

    Returns
    -------
    list of str
        New list containing lowercased alphanumeric words not in the English
        stopword list.
    '''
    
    sw = stopwords.words('english')
    words_filtered = [word.lower() for word in words if word.lower() not in sw and word.isalnum()]
    return words_filtered

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
    '''
    Lemmatise a list of words using WordNet part-of-speech tags.

    Parameters
    ----------
    words : list of str
        List of word tokens to lemmatise.

    Returns
    -------
    list of str
        New list of lemmatised words mapped according to their inferred
        WordNet part of speech.
    
    '''
    lemmatizer = WordNetLemmatizer()

    tagged_tokens = nltk.pos_tag(words)

    lemmatised_words = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag)) 
        for word, tag in tagged_tokens
    ]

    return lemmatised_words

def compare_two_columns(df, column_1, column_2, acronyms, synonyms):
    '''
    Compare lemmatised tokens between two columns in a DataFrame.

    Assumes ``column_1`` and ``column_2`` exist in ``df`` and share a
    0-based integer index from ``0`` to ``len(df) - 1``. For each row, the
    function normalises, tokenises, expands acronyms and synonyms, removes
    stopwords and non-alphanumeric tokens, and lemmatises both text values.
    It then calculates the percentage of lemmatised tokens from
    ``column_1`` present in ``column_2``.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing both ``column_1`` and ``column_2``.
    column_1 : hashable
        Name of the reference column in ``df``. Match percentages measure
        how many lemmatised tokens from this column appear in ``column_2``.
    column_2 : hashable
        Name of the target column in ``df`` to compare against.
    acronyms : Any
        Mapping or lookup structure passed to
        ``replace_acronyms_and_synonyms`` to expand acronyms.
    synonyms : Any
        Mapping or lookup structure passed to
        ``replace_acronyms_and_synonyms`` to standardise synonyms.

    Returns
    -------
    list of float
        Percentage match rate for each row in ``df``, rounded to 2 decimal
        places.

    Notes
    -----
    * Both columns must be in ``df`` and indexed sequentially from ``0`` to
      ``len(df) - 1`` because rows are accessed with ``column[i]``.
    * Each row's match rate is calculated as ``(matches[True] / len(text)) * 100``
      using the lemmatised tokens from ``column_1``.
    * The function currently returns a ``list`` rather than attaching the
      values to a DataFrame column.
    '''
    # set up variables 
    length = len(df)
    column_1 = df[column_1]
    column_2 = df[column_2]
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

    return lemmatised_match_rate
