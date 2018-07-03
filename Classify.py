##############################################
# Script for classifying wikipedia articles of interest
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import en_core_web_sm
import re
import json
import time
from xml.etree.cElementTree import iterparse


# Initialize entity model
nlp = en_core_web_sm.load()

# Create blacklist/whitelist
title_blacklist = ['college', 'university', 'school', 'academy', 'institute', 'centre', 'association', 'center']
twitter_blacklist = ['inc.', 'app', 'technologies', 'list of', ' of ', 'by type', ' by ', '.com', ' and ']
words_of_interest = ['educat', 'technolog', 'learn', 'teach' 'student', 'platform', 'program',
                  'learning platform', 'tool', 'software', 'comput']


# Determine how many important words are in the text. Return true if over 80%
def majority_whitelist(text):
    count = 0
    for word in words_of_interest:
        if word in text:
            count += 1
    return float(count / len(words_of_interest)) >= 0.80


# Get the corpus from the sample files
def generate_wikipedia_data():
    num_analyzed = 0
    on_topic = []
    title = ""
    text = ""
    # Go through XML
    for event, elem in iterparse(".\\wikipedia.xml"):
        # Try to get title and text
        if "title" in elem.tag:
            title = elem.text
        if "text" in elem.tag:
            text = elem.text
        # A title:text pair has been made
        if text != "" and title != "" and text is not None and title is not None:
            num_analyzed += 1
            if num_analyzed % 100000 == 0:
                print(num_analyzed)
            # Make sure it's not already been analyzed and that its text is relevant
            if majority_whitelist(text.lower()):
                # Make sure title is relevant
                processed_title = nlp(title)
                if not any(ent.label_ == "PERSON" or ent.label_ == "GPE" for ent in processed_title.ents) and \
                        not any(blacklist_word in title.lower() for blacklist_word in title_blacklist):
                    on_topic.append(title.lower())
            # Clear variables to keep going
            title = ""
            text = ""
        elem.clear()
    return on_topic


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
            titles[i] = re.sub(r'\(.*?\)', "", titles[i]).strip()
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
            if wiki in tweet.lower() or re.sub(r" ", "", wiki) in tweet.lower():
                counts.update({wiki: counts[wiki] + 1})
    return counts


# Get a count for how many corpus items are mentioned in twitter
t = time.clock()
wikis = fix_titles(generate_wikipedia_data())
tweets = generate_tweet_data()
counts = count_occurrences(wikis, tweets)
print(time.clock() - t)
print(counts)


