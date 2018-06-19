import bs4
import requests
import os
import urllib.parse
import re
import time
import random
import threading


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
        if not any(title in file for file in os.listdir("..\\sample_set")):
            webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
            soup = bs4.BeautifulSoup(webpage, "lxml")
            text = soup.getText().lower()
            file = open('..\\sample_set\\' + re.sub("[^\w\d]", " ", title, re.UNICODE) + '.txt', 'w', encoding='utf-8')
            file.write(text)
            file.close()

# Read index file
index = open("C:\\Users\\useradmin\\Desktop\\index.txt", "r", encoding="utf-8")
lines = index.readlines()

start_time = time.clock()
count = 0
my_randoms = random.sample(range(1, 1841800), 5000)
number_of_threads = 30
number_of_elements = 5000
num_elements_per_thread = int(number_of_elements/number_of_threads)
randomNumberListList = []
threadNameList = []
beginning_element = 0
ending_element = num_elements_per_thread
threadList = []
threadID = 1

for i in range (number_of_threads):
    thread_name = "Thread-".join(str(i))
    threadNameList.append(thread_name)

    list_to_add = list()

    for j in range(beginning_element, ending_element):
        list_to_add.append(my_randoms[j])

    beginning_element += num_elements_per_thread
    ending_element += num_elements_per_thread

    randomNumberListList.append(list_to_add)

for i in range(number_of_threads):
    thread = myThread(threadID, threadNameList[i], randomNumberListList[i], lines)
    thread.start()
    threadList.append(thread)
    threadID += 1

for t in threadList:
   t.join()
 
print(time.clock() - start_time, "seconds")

# 5000 articles: 566.347404 seconds: 0.1132 seconds per article
#                643.93     seconds: 0.128  seconds per article
#                722.51     seconds
#                816.5216356999999 seconds