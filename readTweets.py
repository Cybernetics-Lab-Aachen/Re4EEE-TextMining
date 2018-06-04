#  -*- coding: utf-8 -*-

# TODO: Get JSON directly from web
# TODO: Hashtag/Hyphen handling

# Imports for program
import urllib.request               # lib that handles the url code
import json                         # lib for json code
import re                           # lib for regular expressions
import pandas as pd                 # lib for data processing
import numpy as np                  # lib for idf log
from nltk.corpus import stopwords   # lib for stop words
from collections import OrderedDict
from textblob import TextBlob
import matplotlib.pyplot as plt



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


# Finding whole words in a string
# Author: Hugh Bothwell
# https://stackoverflow.com/questions/5319922/python-check-if-word-is-in-a-string
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


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

# Executes stemming on every tweet in passed dictionary
def stemming(data):
    from nltk.stem import PorterStemmer
    st = PorterStemmer()
    for p in data['Tweets']:
        string = ""
        for word in p['Text'].split(): 
            string = string + st.stem(word) + " "
        string = string.strip()
        p['Text'] = string

# Executes lemmatizing on every tweet in passed dictionary
def lemmatizing(data):
    from textblob import Word
    for p in data['Tweets']:
        string = ""
        for word in p['Text'].split(): 
            string = string + Word(word).lemmatize() + " "
        string = string.strip()
        p['Text'] = string

# Prints most frequent words used in all tweets of passed dictionary
def most_freq(data):
    freq_list = []
    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[:10]
    print(freq)

# Prints least frequent words used in all tweets of passed dictionary
def least_freq(data):
    freq_list = []
    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[-10:]
    print(freq)

# Calculates term frequency of word in a tweet
# Outputs number
def term_freq(x, tweet):
    return tweet.count(x)/len(tweet.split())

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
        count = 0
        for q in data['Tweets']:
            boolean = findWholeWord(x)(q['Text'])
            if boolean is not None:
                count = count + 1 
        if count == 0:
            print("THIS IS A CRITICAL ERROR",x,"DOES NOT SHOW UP IN ANY TWEETS")
        else:
            new_dict[x] = np.log(num_tweets/count)
    return new_dict

# Determines whether given string is a number through attempting a float cast
# Author: Daniel Goldberg
# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def analyze_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


""" # Open website URL to read data
data = urllib.request.urlopen("http://triton.zlw-ima.rwth-aachen.de:50001/twitter") # it's a file like object and works just like a file
for line in data: # files are iterable
    print (line) """

# Parse tweets from JSON file
with open('tweets2205.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    stop = list(stopwords.words('english'))
    stop.append("new")
    stop.append("one")
    stop.append("mine")
    for p in data['Tweets']:

        #-----------------------Tweet analytics BEFORE PREPROCESSING-----------------------#
        p['hashtags'] = len([x for x in p['Text'].split() if x.startswith('#')])

        #-----------------------Text Preprocessing----------------------#
        tweet_str = ""
        p['Text'] = expandContractions(p['Text'])
        tokens = preprocess(p['Text'])
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
 
    sa_list = [0, 0, 0]
    new_tweets = []
    iterator = 0
    for x in data['Tweets'] :
        if len(x['Text'].split()) < 3 or x['Text'] == "":
            continue
        else:
            new_tweets.append(x)
            num = analyze_sentiment(x['Text'])
            x['SA'] = num
            if num == -1:
                sa_list[0] += 1
            elif num == 0:
                sa_list[1] += 1
            elif num == 1:
                sa_list[2] += 1
    data['Tweets'] = new_tweets

    #stemming(data)
    lemmatizing(data)
    
    # Make dictionary of tweets: key is number of tweet, value is dictionary of words and tf values
    tweet_dict = OrderedDict()
    tweet_num = 0
    for p in data['Tweets']:
        tf_dict = {}
        for x in p['Text'].split():
            tf_dict[x] = term_freq(x, p['Text'])
        tweet_dict[tweet_num] = tf_dict
        tweet_num += 1

    # Make idf dictionary
    idf_dict = inv_doc_freq(data)

    #print(json.dumps(data, indent=4, sort_keys=True))

    tuple_list = []

    for x in tweet_dict:
        single_tweet_dict = tweet_dict.get(x)
        for y in single_tweet_dict:
            tup = (y, single_tweet_dict.get(y)*idf_dict[y])
            tuple_list.append(tup)
            #print('{:>20}  {:>20}  {:>20}  {:>20}'.format(y,"{0:.4f}".format(single_tweet_dict.get(y)), "{0:.4f}".format(idf_dict.get(y)), "{0:.4f}".format(single_tweet_dict.get(y)*idf_dict[y])))

    printed_words = set()
    sorted_by_value = sorted(tuple_list, key=lambda tup: tup[1], reverse=True)
    numPrinted = 0
    x = 0
    arr1 = range(0,500)

    arr2 = []
    while (numPrinted < 500):
        tupleToPrint = sorted_by_value[x]
        if tupleToPrint[0] in printed_words:
            x += 1
            continue
        else:
            print(tupleToPrint)
            printed_words.add(tupleToPrint[0])
            arr2.append(tupleToPrint[1])
            numPrinted += 1
            x += 1

    plt.scatter(arr1, arr2, marker='o')
    plt.show()

    print(sa_list)