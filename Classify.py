##############################################
# Script for classifying wikipedia articles of interest
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import en_core_web_sm
import re
import requests
import json
from xml.etree.cElementTree import iterparse
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

# Define named-entity model
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


# Generate education/technology related wikipedia articles from wikipedia dump file
def generate_wikipedia_data():
    on_topic = []  # Article titles that are relevant
    title = ""
    text = ""
    # Stream XML (MAKE SURE YOU HAVE WIKIPEDIA.XML DUMP FILE)
    for event, elem in iterparse("/home/enwiki-20170820-pages-articles-multistream.xml"):
        # Try to get title and text
        if "title" in elem.tag:
            title = elem.text
        if "text" in elem.tag:
            text = elem.text
        # If a title:text pair has been made
        if text != "" and title != "" and text is not None and title is not None:
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
    return on_topic


# Get tweet data from API
def generate_tweet_data():
    # Get the daily twitter dump and write to file
    response = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/twitter")
    text = json.loads(response.text)
    list = []
    for p in text["Tweets"]:
        list.append(p["Text"])
    return list


# Get counts of wikipedia topics mentioned on twitter, return sorted dict
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
        # Remove words with more than 2000 counts
        if wiki in counts and counts[wiki] >= 2000:
            del (counts[wiki])
    # Sort the dictionary by frequencies
    sorted_counts = OrderedDict(sorted(counts.items(), key=lambda x: x[1]))
    sorted_counts = {k: v for k, v in sorted_counts.items() if v != 0}
    return sorted_counts


# Output a graph of results (Co-author: Chris Bohlman)
def output_graph(counts):
    # Cut down to length 20
    keys = list(counts.keys())[len(counts) - 20: len(counts)]
    values = list(counts.values())[len(counts) - 20: len(counts)]

    # Display top 20
    plt.ylabel('Usage')
    plt.xlabel('Words')
    plt.title('Twitter Word Usage')
    y_pos = np.arange(len(keys))
    plt.xticks(y_pos, keys)
    plt.tick_params(axis='both', labelsize=3.5, rotation=30)
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.savefig('graph_out.png', bbox_inches='tight', dpi=1000)


# Send email with results
def send_email(counts):
    fromaddr = "python-server@elearning-finder.net"
    toaddr = ['cbohlmanaz@gmail.com']

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = "E-Learning Script Results: " + datetime.datetime.today().strftime('%d-%m-%Y')

    body = str(counts)
    msg.attach(MIMEText(body, 'plain'))
    filename = "graph_out.png"
    attachment = open(".\\graph_out.png", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    server = smtplib.SMTP('smtp.1und1.de', 587)
    server.starttls()
    server.login(fromaddr, input("Your email password: "))
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


wikis = generate_wikipedia_data()
tweets = generate_tweet_data()
counts = count_occurrences(wikis, tweets)
output_graph(counts)
send_email(counts)




