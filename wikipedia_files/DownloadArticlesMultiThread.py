import bs4
import requests
import os
import urllib.parse
import re
import time
import random
import threading
import shutil
import bz2

# Thread class
class myThread (threading.Thread):
   def __init__(self, threadID, name, numbers, lines):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.numbers = numbers
      self.lines = lines
   def run(self):
      runThroughArticles(self.numbers, self.lines)

# Runs through random number list, and reads in that specific article from server
def runThroughArticles(numbers, lines):
    for i in numbers:
        title = lines[i].split(":")[2].strip("\n")
        if not any(title in file for file in os.listdir("/home/sample_set/.")):
            try:
                webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
            except Exception:
                print("Connection error regarding ", urllib.parse.quote_plus(title))

            soup = bs4.BeautifulSoup(webpage, "lxml")
            text = soup.getText().lower()
            file = open('/home/sample_set/' + re.sub("[^\w\d]", " ", title, re.UNICODE) + '.txt', 'w', encoding='utf-8')
            file.write(text)
            file.close()

# Command line argument for number of threads
""" if len(sys.argv) >= 2:
    number_of_threads = sys.argv[1]
else:
    number_of_threads = 30 """

# Read index file from online
url = "https://dumps.wikimedia.org/enwiki/20180501/enwiki-20180501-pages-articles-multistream-index.txt.bz2"
local_filename = url.split('/')[-1]
r = requests.get(url, stream=True)
with open(local_filename, 'wb') as f:
    shutil.copyfileobj(r.raw, f)
filepath = os.path.join("./", "enwiki-20180501-pages-articles-multistream-index.txt.bz2")
newfilepath = os.path.join("./", 'index.txt')
with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
    for data in iter(lambda : file.read(100 * 1024), b''):
        new_file.write(data)

# Read index file from computer
index = open("./index.txt", "r", encoding="utf-8")
lines = index.readlines()

# Get start time and set up variables
start_time = time.clock()
count = 0
number_of_elements = 5000
my_randoms = random.sample(range(1, 1841800), number_of_elements)
number_of_threads = 2
num_elements_per_thread = int(number_of_elements/number_of_threads)
randomNumberListList = []
threadNameList = []
beginning_element = 0
ending_element = num_elements_per_thread
threadList = []
threadID = 1

# Create thread name and random number lists for each thread
for i in range (number_of_threads):
    thread_name = "Thread-".join(str(i))
    threadNameList.append(thread_name)

    list_to_add = list()

    for j in range(beginning_element, ending_element):
        list_to_add.append(my_randoms[j])

    beginning_element += num_elements_per_thread
    ending_element += num_elements_per_thread

    randomNumberListList.append(list_to_add)

# Create and start every thread and add them all to thread list
for i in range(number_of_threads):
    thread = myThread(threadID, threadNameList[i], randomNumberListList[i], lines)
    thread.start()
    threadList.append(thread)
    threadID += 1

# Join threads so they all terminate at the same time
for t in threadList:
   t.join()

# Print exit time 
print(time.clock() - start_time, "seconds")

# 5000 articles: 566.347404 seconds: 0.1132 seconds per article
#                643.93     seconds: 0.128  seconds per article
#                722.51     seconds
#                816.5216356999999 seconds
# Note: these tests were done sucsessively, so the hardware heating problems could have played a role in the steadility increasing program time.