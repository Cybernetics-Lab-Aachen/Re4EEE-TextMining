##############################################
# Script for classifying wikipedia articles of interest
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import os
import en_core_web_sm
import re
import json

# Initialize entity model
nlp = en_core_web_sm.load()

# Create blacklist/whitelist
title_blacklist = ['college', 'university', 'school', 'academy', 'institute', 'centre', 'association', 'center']
twitter_blacklist = ['inc.', 'app', 'technologies']
words_of_interest = ['educat', 'technolog', 'learn', 'teach' 'student', 'platform', 'program',
                  'learning platform', 'tool', 'software', 'comput']


# Determine how many important words are in the text. Return true if over 80%
def majority_whitelist(text):
    count = 0
    for word in words_of_interest:
        if word in text:
            count += 1
    return float(count / len(words_of_interest)) >= 0.80


# Get the corpus from the sample files (returns a doc title : cleaned split string dictionary)
def generate_wikipedia_data():
    # Filter files and generate corpus
    list = []
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
                    list.append(title.lower())
    return list


# Get tweet data
def generate_tweet_data():
    # Get twitter data
    with open('.\\tweets.json', 'r', encoding='utf-8') as file:
        text = json.loads(file.read())
        list = []
        for p in text["Tweets"]:
            list.append(p["Text"])
    return list


# Process wikipedia article titles into forms better for twitter
def fix_titles(titles):
    for i in range(len(titles)):
        for twitter_blacklist_word in twitter_blacklist:
            titles[i] = re.sub(twitter_blacklist_word, "", titles[i])
    return titles


# Get counts of wikipedia topics mentioned on twitter
def count_occurrences(wikis, tweets):
    # Initialize each wiki concept to 0 count
    counts = {}
    for wiki in wikis:
        counts.update({wiki: 0})
    # Get counts of wiki topics showing in tweets
    for wiki in wikis:
        for tweet in tweets:
            if wiki in tweet.lower() or re.sub(" ", "", wiki) in tweet.lower():
                counts.update({wiki: counts[wiki] + 1})
    return counts


# Get a count for how many corpus items are mentioned in twitter
wikis = fix_titles(generate_wikipedia_data())
tweets = generate_tweet_data()
counts = count_occurrences(wikis, tweets)
print(counts)


