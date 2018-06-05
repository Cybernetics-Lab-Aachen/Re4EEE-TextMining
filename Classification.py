# Class for handling classification algorithms
import numpy as np
import tensorflow as tf
import math

# Calculate term relevance for a document compared to all docs
def calculate_tfidf(corpusValue, corpusValues):
    # Compute tf for each word in doc(times appearing in doc/total num words in doc)
    tfdict = {}
    word_count = len(corpusValue)
    for word in corpusValue:
        if word in tfdict:
            tfdict.update({word: tfdict[word] + 1})
        else:
            tfdict.update({word: 1})
    for key in tfdict:
        tfdict.update({key: tfdict[key]/word_count})

    # Compute idf for each word(log(number of docs/number of docs with word w))
    idfdict = {}
    for word in corpusValue:
        docs_with_word = 0
        for item in corpusValues:
            if word in item:
                docs_with_word += 1
        idfdict.update({word: math.log(len(corpusValues) / docs_with_word)})

    # Compute tfidf for each word
    tfidfdict = {}
    for word in corpusValue:
        tfidfdict.update({word: tfdict[word]*idfdict[word]})
    return tfidfdict


# Get word2int translation. Return a word : integer dictionary given a string input
def word2int(words):
    words = words.split()
    words = set(words)
    word2int = {}
    for i, word in enumerate(words):
        word2int[word] = i
    return word2int


# Get word2vec representation
def compute_word2vec(corpus):
    print("hello")