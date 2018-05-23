# TODO: Get JSON directly from web
# TODO: Check with Thorsten about deleting any URLs to other tweets (deleting anything after https)
# TODO: Should I replace any other punctuation besides hyphens?
# TODO: Remove most frequent words?
# TODO: Remove least frequent words?

import urllib.request               # lib that handles the url code
import json                         # lib for json code
import re                           # lib for regular expressions
import pandas as pd                 # lib for data processing
from nltk.corpus import stopwords   # lib for stop words

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

# Prints least frequent words used in all tweets of passed dictionary
def least_freq(data):
    freq_list = []
    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[-10:]
    print(freq)


""" # Open website URL to read data
data = urllib.request.urlopen("http://triton.zlw-ima.rwth-aachen.de:50001/twitter") # it's a file like object and works just like a file
for line in data: # files are iterable
    print (line) """

# Parse tweets from JSON file
with open('tweets2205.json', encoding="utf8") as json_file:
    data = json.load(json_file)
    stop = stopwords.words('english')

    # Iterate through every tweet
    for p in data['Tweets']:
        #-----------------------Tweet analytics-----------------------#
        p['word_count'] = len(str(p['Text']).split(" "))
        p['char_count'] = len(p['Text'])
        p['avg_word_length'] = avg_word(p['Text'])
        p['stopwords'] = len([x for x in p['Text'].split() if x in stop])
        p['hashtags'] = len([x for x in p['Text'].split() if x.startswith('#')])
        p['numerics'] = len([x for x in p['Text'].split() if x.isdigit()])
        p['uppercase'] = len([x for x in p['Text'].split() if x.isupper()])

        #-----------------------Text Preprocessing----------------------#
        # Replace hyphes with spaces
        p['Text'] = p['Text'].lower()
        if p['Text'] in "-":
            p['Text'].replace("-"," ")
    
        # Replace punctuation with spaces
        p['Text'] = re.sub(r'[^\w\s]',' ',p['Text'])

        # Remove excess whitespace from string
        string = ""
        for x in p['Text'].split():
            if x == "":
                continue
            elif x == " ":
                continue
            elif x == "\n":
                continue
            elif x not in stop:
                string = string + x + " "
        
        # Remove hyperlinks in string by removing anything after https
        if "https" in string:
            string = string[:string.index("https")]

        p['Text'] = string 

    #lemmatizing(data)
    #stemming(data)

    print (json.dumps(data, indent=4, sort_keys=True))

    #most_freq(data)
    #least_freq(data)