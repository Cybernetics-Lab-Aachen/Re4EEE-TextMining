import threading
import time
import bs4
import requests
import os
import urllib.parse
import re
import random
import shutil
import bz2
from requests.exceptions import ConnectionError


# import sqlite3
# # Connect to sqlite
# connection = sqlite3.connect('wikiarticles.db')
# c = connection.cursor()

class myThread (threading.Thread):
   def __init__(self, threadID, name, numbers, lines):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.numbers = numbers
      self.lines = lines
   def run(self):
      runThroughArticles(self.numbers, self.lines)

def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    return local_filename

def runThroughArticles(numbers, lines):
    for i in numbers:
        title = lines[i].split(":")[2].strip("\n")
        if not any(title in file for file in os.listdir("./sample_set")):
            try:
                webpage = requests.get("http://re4eee-data-proxy:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
            except ConnectionError as e:  # This is the correct syntax
                print(e)
                exit(1)
            readArticle(webpage, title)
            print(time.clock() - start_time, "seconds")

def readArticle(webpage, title):
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        if ('learn' in text or 'educat' in text) and ('teach' in text or 'student' in text) \
                and ('method' in text or 'tool' in text or 'concept' in text or 'platform' in text or 'tech' in text):
            file = open('./sample_set/' + re.sub("[^A-Za-z]", " ", title) + '.txt', 'w', encoding='utf-8')
            file.write(text)
            file.close()
    
def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]

my_randoms = random.sample(range(1, 18458000), 1000)

try:
    download_file("https://dumps.wikimedia.org/enwiki/20180501/enwiki-20180501-pages-articles-multistream-index.txt.bz2")
except ConnectionError as e:  # This is the correct syntax
    print(e)
    exit(1)

filepath = os.path.join("./", "enwiki-20180501-pages-articles-multistream-index.txt.bz2")
newfilepath = os.path.join("./", 'index.txt')
with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
    for data in iter(lambda : file.read(100 * 1024), b''):
        new_file.write(data)
print("Index file read and written")
# Read index file
index = open("./index.txt", "r", encoding="utf-8")
lines = index.readlines()

x, y = split_list(my_randoms)

first, second = split_list(x)
third, fourth = split_list(y)

one, two = split_list(first)
three, four = split_list(second)
five, six = split_list(third)
seven, eight = split_list(fourth)

A, B = split_list(one)
C, D = split_list(two)
E, F = split_list(three)
G, H = split_list(four)
I, J = split_list(five)
K, L = split_list(six)
M, N = split_list(seven)
O, P = split_list(eight)

listsList = [A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]
threadNameList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5","Thread-6",
                "Thread-7","Thread-8","Thread-9","Thread-10","Thread-11","Thread-12",
                "Thread-13","Thread-14","Thread-15","Thread-16"]
threadList = []
threadID = 1

start_time = time.clock()

for i in range(16):
    thread = myThread(threadID, threadNameList[i], listsList[i], lines)
    thread.start()
    threadList.append(thread)
    threadID += 1

for t in threadList:
   t.join()

print ("Exiting Main Thread")

# First attempt 2 threads: 68.29056655360719 seconds
# Second attempt 2 threads: 64.14474363742802 seconds

# First attempt 4 threads: 44.99423248871253 seconds
# Second attempt 4 threads: 45.05058939539863 seconds

# First attempt 8 threads: 30.3525312760942 seconds
# Second attempt 8 threads: 34.02615105961444 seconds

# First attempt 16 threads: 29.629705987882847 seconds
# Second attempt 16 threads: 29.743744575895587 seconds