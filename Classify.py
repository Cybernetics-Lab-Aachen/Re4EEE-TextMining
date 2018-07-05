##############################################
# Script for classifying wikipedia articles of interest
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import en_core_web_sm
import re
import json
import time
from xml.etree.cElementTree import iterparse
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import time
time.sleep(5)

# Initialize entity model
nlp = en_core_web_sm.load()

# Create blacklist/whitelist
title_blacklist = ['college', 'university', 'school', 'academy', 'institute', 'centre', 'association', 'center']
twitter_blacklist = ['inc.', 'app', 'technologies', 'list of', ' of ', 'by type', ' by ', '.com', ' and ', '\(.*?\)']
words_of_interest = ['educat', 'technolog', 'learn', 'teach' 'student', 'platform', 'program',
                  'learning platform', 'tool', 'software', 'comput']


# Determine how many important words are in the text. Return true if over 80%
def majority_whitelist(text):
    count = 0
    for word in words_of_interest:
        if word in text:
            count += 1
    return float(count / len(words_of_interest)) >= 0.80


# Generate education/technology related wikipedia articles
def generate_wikipedia_data():
    num_analyzed = 0
    on_topic = []
    title = ""
    text = ""
    # Go through XML
    for event, elem in iterparse("/home/enwiki-20170820-pages-articles-multistream.xml"):
        if num_analyzed == 50000:
            break
        # Try to get title and text
        if "title" in elem.tag:
            title = elem.text
        if "text" in elem.tag:
            text = elem.text
        # A title:text pair has been made
        if text != "" and title != "" and text is not None and title is not None:
            num_analyzed += 1
            if num_analyzed % 1000000 == 0:
                print(num_analyzed)
            # Make sure it's not already been analyzed and that its text is relevant
            if majority_whitelist(text.lower()):
                # Make sure title is relevant
                processed_title = nlp(title)
                if not any(ent.label_ == "PERSON" or ent.label_ == "GPE" for ent in processed_title.ents) and \
                        not any(blacklist_word in title.lower() for blacklist_word in title_blacklist):
                    # Clean up for twitter and add to final list
                    for twitter_blacklist_word in twitter_blacklist:
                        title = re.sub(twitter_blacklist_word, "", title.lower()).strip()
                    on_topic.append(title)
            # Clear variables to keep going
            title = ""
            text = ""
        elem.clear()
    return on_topic


# Get tweet data
def generate_tweet_data():
    # Get twitter data
    import urllib.request, json 
    with urllib.request.urlopen("http://triton.zlw-ima.rwth-aachen.de:50001/twitter") as url:
        text = json.loads(url.read().decode())
        list = []
        for p in text["Tweets"]:
            list.append(p["Text"])
    return list


# Get counts of wikipedia topics mentioned on twitter
def count_occurrences(wikis, tweets):
    counts = {}
    # Get counts of wiki topics showing in tweets
    for wiki in wikis:
        for tweet in tweets:
            if wiki in tweet.lower() or re.sub(r" ", "", wiki) in tweet.lower():
                if wiki in counts:
                    counts.update({wiki: counts[wiki] + 1})
                else:
                    counts.update({wiki: 1})
        if wiki in counts and counts[wiki] >= 1000:
            del (counts[wiki])
    return counts


# Output a graph of results (Co-author: Chris Bohlman)
def output_graph(counts):
    # Sort the counts
    sorted_counts = OrderedDict(sorted(counts.items(), key=lambda x: x[1]))
    sorted_counts = {k: v for k, v in sorted_counts.items() if v != 0}
    keys = list(sorted_counts.keys())[len(sorted_counts) - 20: len(sorted_counts)]
    values = list(sorted_counts.values())[len(sorted_counts) - 20: len(sorted_counts)]
    # Display top 20
    plt.ylabel('Usage')
    plt.xlabel('Words')
    plt.title('Twitter Word:Usage')
    y_pos = np.arange(len(keys))
    plt.xticks(y_pos, keys)
    plt.tick_params(axis='both', labelsize=3.5, rotation=30)
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.savefig('graph_out.png', bbox_inches='tight', dpi=1000)


# Get a count for how many corpus items are mentioned in twitter
t = time.clock()
wikis = generate_wikipedia_data()
tweets = generate_tweet_data()
counts = count_occurrences(wikis, tweets)
output_graph(counts)
print(counts)
print(time.clock() - t)



