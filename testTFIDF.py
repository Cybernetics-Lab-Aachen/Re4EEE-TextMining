import math
from textblob import TextBlob as tb

import urllib.request               # lib that handles the url code
import json                         # lib for json code
import re                           # lib for regular expressions
import pandas as pd                 # lib for data processing
import numpy as np                  # lib for idf log
from nltk.corpus import stopwords   # lib for stop words
from collections import OrderedDict


# Tokenization/parsing of tweets: methods and code
# Author: Marco Bonzanini
# https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]   

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


# Replacing contractions in tweets, modified for program
# Author: arturomp
# https://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "i'd": "i would",
  "i'd've": "i would have",
  "i'll": "i will",
  "i'll've": "i will have",
  "i'm": "i am",
  "i've": "i have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text.lower())


# Code for processing text tweets, adapted from online tutorial
# Author: Chris Bohlman
# Author: Shubham Jaim
# https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/

# Returns the average word length in the passed string
# Handles tweets of 0 length by returning 0
def avg_word(sentence):
    words = sentence.split()
    if (len(words) == 0): 
        return 0
    else :
        return (sum(len(word) for word in words)/len(words))

# Executes stemming on every tweet in passed dictionary
def stemming(data):
    from nltk.stem import PorterStemmer
    st = PorterStemmer()
    for p in data['Tweets']:
        string = ""
        for word in p['Text'].split(): 
            string = string + st.stem(word) + " "
        string.strip()
        p['Text'] = string

# Executes lemmatizing on every tweet in passed dictionary
def lemmatizing(data):
    from textblob import Word
    for p in data['Tweets']:
        string = ""
        for word in p['Text'].split(): 
            string = string + Word(word).lemmatize() + " "
        string.strip()
        p['Text'] = string

# Prints most frequent words used in all tweets of passed dictionary
def most_freq(data):
    freq_list = []
    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[:10]
    print(freq)
    remove_words(freq, data)

# Prints least frequent words used in all tweets of passed dictionary
def least_freq(data):
    freq_list = []
    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[-10:]
    print(freq)
    remove_words(freq, data)

# Removes words in freq from data tweets
def remove_words(freq, data):
    for p in data['Tweets']:
        string = ""
        for x in p['Text'].split():
            if x not in freq:
                string = string + x + " "
        string.strip()
        p['Text'] = string

# Calculates term frequency of word in a tweet
# Outputs number
def term_freq(x, tweet):
    return tweet.count(x)/len(tweet.split())
    """ new_dict = {}
    s = ""
    for p in data['Tweets']:
        s = s + p['Text'].lstrip('#') + " " 
    series = pd.value_counts(s.split())
    num_terms = sum(series.tolist())
    for q in series.axes[0]:
        new_dict[q] = series[q]/num_terms
    return new_dict """

# Calculates inverse frequency per word
# Outputs dictionary of word and idf value
def inv_doc_freq(data):
    new_dict = {}
    num_tweets = len(data['Tweets'])
    s = ""
    for p in data['Tweets']:
        s = s + p['Text'] + " "
    s = s.strip()
    series = pd.value_counts(s.split())
    for x in series.axes[0]:
        #print(x)
        count = 0
        for q in data['Tweets']:
            if x in q['Text']:
                count = count + 1 
        if count == 0:
            print("THIS IS A CRITICAL ERROR",x,"DOES NOT SHOW UP IN ANY TWEETS")
        else:
            new_dict[x] = np.log(num_tweets/count)
    return new_dict

# Determines whether given string is a number
# If float casting works, returns true
# Else, return false
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    num = tf(word, blob) * idf(word, bloblist)
    print(word, num)
    return num

with open('tweets2205.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    stop = stopwords.words('english')
    # Iterate through every tweet
    for p in data['Tweets']:

        #-----------------------Tweet analytics BEFORE PREPROCESSING-----------------------#
        p['word_count'] = len(str(p['Text']).split(" "))
        p['char_count'] = len(p['Text'])
        p['avg_word_length'] = avg_word(p['Text'])
        p['stopwords'] = len([x for x in p['Text'].split() if x in stop])
        p['hashtags'] = len([x for x in p['Text'].split() if x.startswith('#')])
        p['numerics'] = len([x for x in p['Text'].split() if x.isdigit()])
        p['uppercase'] = len([x for x in p['Text'].split() if x.isupper()])

        #-----------------------Text Preprocessing----------------------#
        tweet_str = ""
        p['Text'] = expandContractions(p['Text'])
        tokens = preprocess(p['Text'])
        if len(tokens) != 0:
            for x in tokens:
                x = x.encode('ascii', 'ignore').decode()
                x = x.strip()
                x = x.lstrip('#')
                x = x.lower()
                if "https" in x:
                    continue
                elif x in stop:
                    continue
                elif is_number(x):
                    continue
                elif "@" in x:
                    continue
                elif "rt" == x:
                    continue
                elif "," in x:
                    continue
                elif ":" in x:
                    continue
                elif "#" == x:
                    continue
                elif "|" == x:
                    continue
                elif ";" == x:
                    continue
                elif "!" == x:
                    continue
                elif "'" == x:
                    continue
                elif '/n' == x:
                    continue
                elif "" == x:
                    continue
                elif " " == x:
                    continue
                elif "/" == x:
                    continue
                elif "?" == x:
                    continue
                elif "&" == x:
                    continue
                elif '"' == x:
                    continue
                elif '-' == x:
                    continue
                elif '_' == x:
                    continue
                elif '.' == x:
                    continue
                elif '%' == x:
                    continue
                elif '(' == x:
                    continue
                elif ')' == x:
                    continue
                elif '$' == x:
                    continue
                elif '[' == x:
                    continue
                elif ']' == x:
                    continue
                elif '*' == x:
                    continue
                elif '-' in x:
                    x = x.replace('-',' ')
                elif len(x) < 3:
                    continue
                elif "'s" in x:
                    x = x[:-2]
                else:
                    tweet_str = tweet_str + x + " "
            tweet_str = tweet_str.strip()
            tweet_str = tweet_str.lower()
            p['Text'] = tweet_str
            p['word_count'] = len(str(p['Text']).split(" "))

bloblist = []
for p in data['Tweets']:
    bloblist.append(tb(p['Text']))

for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #for word, score in sorted_words[:3]:
        #print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))