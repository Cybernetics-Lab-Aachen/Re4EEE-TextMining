# Class for handling classification algorithms
from wikipedia_files import CleanWikiDocs
import math
import os
import operator
import en_core_web_sm
import time

# Initialize entity model
nlp = en_core_web_sm.load()

# Create blacklist/whitelist
title_blacklist = ['college', 'university', 'school', 'academy', 'institute', 'centre']
text_whitelist = ['educat', 'technolog', 'learn', 'student']

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
        tfidfdict.update({word: (math.log(len(text_corpus) / docs_with_word)) * tfidfdict[word]})
    return sorted(tfidfdict.items(), key=operator.itemgetter(1))


# Get top 25 words of an article given tfidf scores. Delete if not relevant to education
def filter_tfidf(corpus):
    iterate = corpus.copy()
    for key in iterate.keys():
        # Get current document word to tfidf tuple list
        curr_tuple_list = iterate[key]
        found = False
        # For each of top 15 scoring words
        for i in range(len(curr_tuple_list) - 1, len(curr_tuple_list) - 26, -1):
            if len(curr_tuple_list) < 25:
                break
            # Check if top 15 words contain keywords relating to education, if not, delete article from list
            if any(whitelist_word in curr_tuple_list[i][0] for whitelist_word in text_whitelist):
                found = True
                corpus.update({key: curr_tuple_list[len(curr_tuple_list) - 26: len(curr_tuple_list) -1]})
                break
        if not found:
            del corpus[key]
    return corpus


# Get word2int translation. Return a word : integer dictionary given a string input
def word2int(words):
    words = words.split()
    words = set(words)
    word2int = {}
    for i, word in enumerate(words):
        word2int[word] = i
    return word2int


# Get word2vec representation (returns word vector given word)
def compute_word2vec(corpus):
    data = []
    window_size = 2
    # For each text in the corpus
    for text in corpus.values():
        # Enumerate text
        for word_index, word in enumerate(text):
            # Apply the window to the text, add neighbouring pairs to the data list (ensures no out of bounds)
            for neighbour in text[max(word_index - window_size, 0): min(word_index + window_size, len(text)) + 1]:
                if neighbour != word:
                    data.append([word, neighbour])
    # Convert the word pairs into numbers
    return ''


# Get the corpus from the sample files (returns a doc title : cleaned split string dictionary)
def generate_corpus():
    corpus = {}
    files = os.listdir(".\\sample_set")
    number_of_threads = 30
    num_elements_per_thread = int(len(files)/number_of_threads)
    if num_elements_per_thread < 1:
        import sys
        sys.exit("Number of files is less than amount of threads. Didn't want to write catch code, so program will exit")
    listsList = []
    threadNameList = []
    beginning_element = 0
    ending_element = num_elements_per_thread

    for i in range (0, number_of_threads):
        thread_name = "Thread-" + str(i)
        threadNameList.append(thread_name)

        list_to_add = list()

        for j in range(beginning_element, ending_element):
            list_to_add.append(files[j])

        beginning_element += num_elements_per_thread
        ending_element += num_elements_per_thread

        listsList.append(list_to_add)

    threadList = []
    threadID = 1

    for i in range(number_of_threads):
        thread = myThread(threadID, threadNameList[i], listsList[i], lines)
        thread.start()
        threadList.append(thread)
        threadID += 1

    for t in threadList:
        t.join()


    for filename in os.listdir(".\\sample_set"):
        with open('.\\sample_set\\' + filename, 'r', encoding='utf-8') as myfile:
            text = myfile.read()
            title = filename.replace(".txt", "").strip()
            # Make sure title not about school or person/Don't add a text unless it contains some education keywords
            if all(whitelist_word in text.lower() for whitelist_word in text_whitelist):
                processed_title = nlp(title)
                if not any(ent.label_ == "PERSON" or ent.label_ == "GPE" for ent in processed_title.ents) and \
                        not any(blacklist_word in title.lower() for blacklist_word in title_blacklist):
                    corpus.update({title: CleanWikiDocs.process(text).split()})
    return corpus


# Generate corpus (apply filter)
t = time.clock()
corpus = generate_corpus()
print(corpus.keys())
print(time.clock() - t)