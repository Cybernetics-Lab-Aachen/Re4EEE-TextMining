import threading
import time
import bs4
import requests
import os
import urllib.parse
import re
import random
import sys

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

def runThroughArticles(numbers, lines):
    for i in numbers:
        title = lines[i].split(":")[2].strip("\n")
        if not any(title in file for file in os.listdir("./sample_set")):
            webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
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

number_of_threads = 0

if len(sys.argv) >= 2:
    number_of_threads = sys.argv[1]
else:
    number_of_threads = 10

num_elements_per_thread = 1000/number_of_threads

my_randoms = random.sample(range(1, 18458000), 1000)

# Read index file
index = open("./index.txt", "r", encoding="utf-8")
lines = index.readlines()

listsList = []
threadNameList = []
beginning_element = 0
ending_element = num_elements_per_thread

for i in range (0, number_of_threads):
    thread_name = "Thread-" + i
    threadNameList[i] = thread_name

    list_to_add = list()

    for j in range(beginning_element, ending_element):
        list_to_add.append(my_randoms[j])

    beginning_element += num_elements_per_thread
    ending_element += num_elements_per_thread

    listsList.append(list_to_add)

threadList = []
threadID = 1

start_time = time.clock()

for i in range(number_of_threads):
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