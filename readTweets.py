# TODO: Shift stemming/lemmatization into functions
# TODO: Get JSON directly from web
# TODO: Check with Thorsten about deleting any URLs to other tweets (deleting anything after https)
# TODO: Should I replace any other punctuation besides hyphens?
# TODO: Comment code out

def avg_word(sentence):
    words = sentence.split()
    if (len(words) == 0): 
        return 0
    else :
        return (sum(len(word) for word in words)/len(words))

import urllib.request  # the lib that handles the url stuff
import json
from nltk.corpus import stopwords
stop = stopwords.words('english')
import re
import pandas as pd
from textblob import TextBlob


""" # Open website URL to read data
data = urllib.request.urlopen("http://triton.zlw-ima.rwth-aachen.de:50001/twitter") # it's a file like object and works just like a file
for line in data: # files are iterable
    print (line) """

# Parse tweets from JSON file
with open('tweets2205.json', encoding="utf8") as json_file:
    i = 0 
    data = json.load(json_file)
    for p in data['Tweets']:
        
        # Tweet analytics

        p['word_count'] = len(str(p['Text']).split(" "))
        p['char_count'] = len(p['Text'])
        p['avg_word_length'] = avg_word(p['Text'])
        p['stopwords'] = len([p['Text'] for x in p['Text'].split() if x in stop])
        p['hashtags'] = len([p['Text'] for x in p['Text'].split() if x.startswith('#')])
        p['numerics'] = len([p['Text'] for x in p['Text'].split() if x.isdigit()])
        p['uppercase'] = len([p['Text'] for x in p['Text'].split() if x.isupper()])

        # Text preprocessing
        p['Text'] = p['Text'].lower()
        if p['Text'] in "-":
            p['Text'].replace("-"," ")
        
        p['Text'] = re.sub(r'[^\w\s]',' ',p['Text'])
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
        
        if "https" in string:
            string = string[:string.index("https")]

        p['Text'] = string 

    
    """ print (json.dumps(data, indent=4, sort_keys=True))

    from nltk.stem import PorterStemmer
    st = PorterStemmer()
    for p in data['Tweets']:
        string = ""
        for word in p['Text'].split(): 
            string = string + st.stem(word) + " "
        p['Text'] = string """


    from textblob import Word
    for p in data['Tweets']:
        string = ""
        for word in p['Text'].split(): 
            string = string + Word(word).lemmatize() + " "
        p['Text'] = string

    print (json.dumps(data, indent=4, sort_keys=True))

    freq_list = []
    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[:10]

    print(freq)

    for p in data['Tweets']:
        freq_list.append(p['Text'])
    freq = pd.Series(' '.join(freq_list).split()).value_counts()[-10:]

    print(freq)


   

    #data['word_count'] = data['Text'].apply(lambda x: len(str(x).split(" ")))
    #data[['Tweets','word_count']].head()


""" # Parse wikipedia article from JSON file
with open('wikipedia2205.json', encoding="utf8") as json_file: 
    data = json.load(json_file)
    print('Error: ' +data['Error'])
    print('Title: ' + data['Title'])
    print('ArticleID: ' + data['ArticleID'])
    print('Text: ' + data['Text'])
    print('') """
