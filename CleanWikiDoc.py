# A script for cleaning up wikipedia dump files and preprocessing
import re
import nltk
import contractions
import inflect
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer


# Remove brackets, punctuation etc.
def denoise(sample):
    index = sample.find("Text")
    sample = sample[index+4:].lower()
    sample = re.sub("\\\\n", " ", sample)
    return re.sub("[^a-z ]", " ", sample)


# Replace contractions with full words to prevent duplicates
def replace_contractions(sample):
    return contractions.fix(sample)


# Replace numbers with word equivalents
def replace_nums(words):
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


# Lemmatize verbs
def lemmatize(words):
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word)
        lemmas.append(lemma)
    return lemmas


# Replace unecessary words
def remove_stops(words):
    english_words = set(nltk.corpus.words.words())
    stops = set(stopwords.words("english"))
    filtered = []
    for word in words:
        if word not in stops and word in english_words and len(word) != 1:
            filtered.append(word)
    return filtered


# Get frequency for each word
def word_frequency(words):
    dictionary = dict()
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary


# Remove low frequency words with little effect on results
def remove_low_frequency(words):
    counts = word_frequency(words)
    items = counts.items()
    filtered = []
    for item in items:
        if item[0] in counts and counts[item[0]] != 1:
            filtered.append(item[0])
    return filtered


# Process a wiki document
def process(text):
    # Clean up the text
    text = denoise(text)
    text = replace_contractions(text)

    # Tokenize, normalize, lemmatize, remove low frequency words
    words = nltk.word_tokenize(text)
    words = replace_nums(words)
    words = remove_stops(words)
    words = lemmatize(words)
    words = remove_low_frequency(words)
    return ' '.join(words)



