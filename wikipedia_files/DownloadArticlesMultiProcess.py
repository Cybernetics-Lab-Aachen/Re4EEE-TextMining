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

def runThroughArticles(numbers, lines):
    for i in numbers:
        title = lines[i].split(":")[2].strip("\n")
        if not any(title in file for file in os.listdir("..\\sample_set")):
           webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
           readArticle(webpage, title)
        print(time.clock() - start_time, "seconds")

def readArticle(webpage, title):
    soup = bs4.BeautifulSoup(webpage, "lxml")
    text = soup.getText().lower()
    if ('learn' in text or 'educat' in text) and ('teach' in text or 'student' in text) \
            and ('method' in text or 'tool' in text or 'concept' in text or 'platform' in text or 'tech' in text):
        file = open('..\\sample_set\\' + re.sub("[^A-Za-z]", " ", title) + '.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()

def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]

# Read index file
index = open("C:\\Users\\useradmin\\Desktop\\index.txt", "r", encoding="utf-8")
lines = index.readlines()

my_randoms = random.sample(range(1, 18458000), 1000)
x, y = split_list(my_randoms)
list_nums = [x, y]

start_time = time.clock()

if __name__ == '__main__':
    pool = mp.Pool(processes=2)
    results = pool.map(partial(runThroughArticles, lines=lines), list_nums)

# First attempt 2 processes: 173.67093533933854 seconds
# Second attempt 2 processes: 194.74739417197685 seconds

# First attempt 4 processes: > 228.62999951557669 seconds