##############################################
# Script for classifying wikipedia articles of interest
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import CleanWikiDoc
import math
import os
import operator
import en_core_web_sm
import time
import re

# Initialize entity model
nlp = en_core_web_sm.load()

# Create blacklist/whitelist
title_blacklist = ['college', 'university', 'school', 'academy', 'institute', 'centre', 'association', 'center']
twitter_blacklist = ['inc.', 'app']
words_of_interest = ['educat', 'technolog', 'learn', 'teach' 'student', 'platform', 'program',
                  'learning platform', 'tool', 'software', 'comput']


# Calculate term relevance for a document compared to all docs. Returns sorted list of tuples
def compute_tfidf(doc_text, text_corpus):
    tfidfdict = {}
    # For each word in doc
    for word in doc_text:
        # Update tf values (times appearing in doc/total num words in doc)
        if word in tfidfdict:
            tfidfdict.update({word: tfidfdict[word] + (1 / len(doc_text))})
        else:
            tfidfdict.update({word: 1 / len(doc_text)})
        # Update idf values (log(number of docs/number of docs with word w))
        docs_with_word = 0
        # Have to use a different name from doc_text so variable naming doesn't mess up
        for doc_text2 in text_corpus:
            if word in doc_text2:
                docs_with_word += 1
        if docs_with_word != 0:
            tfidfdict.update({word: (math.log(len(text_corpus) / docs_with_word)) * tfidfdict[word]})
    return sorted(tfidfdict.items(), key=operator.itemgetter(1))


# Get top 25 words of an article given tfidf scores. Delete if not relevant to education
def filter_tfidf(corpus):
    iterate = corpus.copy()
    for key in iterate.keys():
        # Get current document word to tfidf tuple list
        curr_tuple_list = iterate[key]
        found = False
        # For each of top 25 scoring words
        for i in range(len(curr_tuple_list) - 1, len(curr_tuple_list) - 26, -1):
            if len(curr_tuple_list) < 25:
                break
            # Check if top 25 words contain keywords relating to education, if not, delete article from list
            if any(word in curr_tuple_list[i][0] for word in words_of_interest):
                found = True
                corpus.update({key: curr_tuple_list[len(curr_tuple_list) - 26: len(curr_tuple_list) -1]})
                break
        if not found:
            del corpus[key]
    return corpus


# Determine how many important words are in the text. Return true if over 80%
def majority_whitelist(text):
    count = 0
    for word in words_of_interest:
        if word in text:
            count += 1
    return float(count / len(words_of_interest)) >= 0.80


# Get the corpus from the sample files (returns a doc title : cleaned split string dictionary)
def generate_corpus():
    # Filter files and generate corpus
    corpus = {}
    for filename in os.listdir(".\\sample_set"):
        with open('.\\sample_set\\' + filename, 'r', encoding='utf-8') as myfile:
            text = myfile.read()
            title = filename.replace(".txt", "").strip()
            # Don't add a text unless it contains majority of whitelist worda
            if majority_whitelist(text.lower()):
                processed_title = nlp(title)
                # Make sure title not about school or person
                if not any(ent.label_ == "PERSON" or ent.label_ == "GPE" for ent in processed_title.ents) and \
                        not any(blacklist_word in title.lower() for blacklist_word in title_blacklist):
                    # Update corpus entry
                    corpus.update({title.lower(): CleanWikiDoc.process(text).split()})
    return corpus


# Count frequencies of e-learning in tweets
def count_elearning():
    # Get twitter data


# Get a count for how many corpus items are mentioned in twitter
t = time.clock()
corpus = generate_corpus()
print(corpus.keys())
print(time.clock() - t)
