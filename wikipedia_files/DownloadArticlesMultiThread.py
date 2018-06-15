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
        if not any(title in file for file in os.listdir("../sample_set")):
            try:
                webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
            except ConnectionError as e:  # This is the correct syntax
                print(e)
                exit(1)
            readArticle(webpage, title)           

def readArticle(webpage, title):
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        file = open('..\\sample_set\\' + re.sub("[^\w\d]", " ", title, re.UNICODE) + '.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()
    
def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]

my_randoms = random.sample(range(1, 1841800), 5000)

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

number_of_threads = 30
num_elements_per_thread = int(5000/number_of_threads)
listsList = []
threadNameList = []
beginning_element = 0
ending_element = num_elements_per_thread

for i in range (0, number_of_threads):
    thread_name = "Thread-" + str(i)
    threadNameList.append(thread_name)

    list_to_add = list()

    for j in range(beginning_element, ending_element):
        list_to_add.append(my_randoms[j])

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

start_time = int(time.process_time())

for t in threadList:
   t.join()


print(int(time.process_time() - start_time), "seconds")
print ("Exiting Main Thread")

# First attempt 2 threads: 68.29056655360719 seconds
# Second attempt 2 threads: 64.14474363742802 seconds

# First attempt 4 threads: 44.99423248871253 seconds
# Second attempt 4 threads: 45.05058939539863 seconds

# First attempt 8 threads: 30.3525312760942 seconds
# Second attempt 8 threads: 34.02615105961444 seconds

# First attempt 16 threads: 29.629705987882847 seconds
# Second attempt 16 threads: 29.743744575895587 seconds