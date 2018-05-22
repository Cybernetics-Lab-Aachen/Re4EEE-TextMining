# A script for cleaning up wikipedia dumps and preprocessing
import re
import nltk
import contractions
import inflect
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

# Remove brackets, punctuation etc.
def denoise(sample):
    index = sample.find("Text")
    sample = sample[index:].lower()
    return re.sub("[^a-z ]", " ", sample)


# Replace contractions with full words to prevent duplicates
def replace_contractions(sample):
    return contractions.fix(sample)


# Replace numbers with word equivalents
def replace_nums(list):
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
# TODO not working
def lemmatize_verbs(words):
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, 'v')
        lemmas.append(lemma)
    return lemmas


# Replace unecessary words
def remove_unecessary(words):
    english_words = set(nltk.corpus.words.words())
    stops = set(stopwords.words("english"))
    filtered = []
    for word in words:
        if word not in stops and word in english_words and len(word) != 1:
            filtered.append(word)
    return filtered


# Get the text
file = open("testfile.txt", "r", encoding="utf8")
text = file.read()

# Clean up the text
text = denoise(text)
text = replace_contractions(text)

# Tokenize, normalize
words = nltk.word_tokenize(text)
words = replace_nums(words)
words = remove_unecessary(words)
print(words)


