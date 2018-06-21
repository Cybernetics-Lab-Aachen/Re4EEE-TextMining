# NOTE: This code should be considered depracated. It seems as if my machine is unable to handle multiprocessing programs, 
# as for any mp, the machine takes longer with mp than with the regular version of the program.
import time
import bs4
import requests
import os
import urllib.parse
import re
import random
from multiprocessing import Process
from functools import partial
import multiprocessing as mp

# Runs through random number list, and reads in that specific article from server
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

# Seperate random number list into two lists
my_randoms = random.sample(range(1, 18458000), 1000)
x = my_randoms[:len(my_randoms)/2]
y = my_randoms[len(my_randoms)/2:]
list_nums = [x, y]

start_time = time.clock()

# Start multiprocessing of data
if __name__ == '__main__':
    for i in list_nums:
        """ pool = mp.Pool(processes=2)
        results = pool.map(partial(runThroughArticles, lines=lines), list_nums) """
        p = Process(target=runThroughArticles, args=(i, lines))
        p.Daemon = True
        p.start()
    
    
    for i in list_nums:
        p.join()

    print(time.clock() - start_time, "seconds")

# First attempt 2 processes: 173.67093533933854 seconds
# Second attempt 2 processes: 194.74739417197685 seconds
# First attempt 4 processes: > 228.62999951557669 seconds
# 435.0994541 seconds, 345.4183772 seconds, 405.8439787 seconds
# 405.8439787 seconds, 424.70200040000003 seconds, 378.7717576 seconds