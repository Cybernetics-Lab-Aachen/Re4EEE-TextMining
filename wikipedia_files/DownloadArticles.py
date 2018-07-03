# Downloads 5000 random wikipedia articles from server sequentially
# NOTE: Runtime is about 498 seconds

import time
import bs4
import requests
import os
import urllib.parse
import re
import random

list_of_files = os.listdir("..\\sample_set")

# Read index file
index = open("C:\\Users\\useradmin\\Desktop\\index.txt", "r", encoding="utf-8")
lines = index.readlines()

# Seperate random number list into two lists
my_randoms = random.sample(range(1, 18458000), 5000)
input = []
for num in my_randoms:
    input.append(lines[num].split(":")[2].strip("\n"))

start_time = time.clock()

for title in input:
    if not any(title in file for file in list_of_files):
        webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        file = open('..\\sample_set\\' + re.sub("[^\w\d]", " ", title, re.UNICODE) + '.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()

print(time.clock() - start_time, "seconds")