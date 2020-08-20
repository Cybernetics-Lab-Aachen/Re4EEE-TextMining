##############################################
# Script with old methods for calculating and filtering a TFIDF dictionary
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import math
import operator

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