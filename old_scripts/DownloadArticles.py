##############################################
# Simple script for downloading wikipedia articles
# Author: Devin Johnson, RWTH Aachen IMA/IFU
##############################################

import bs4
import requests
import os
import urllib.parse
import re
import time
from random import randint

# Read index file
index = open("C:\\Users\\useradmin\\Desktop\\index.txt", "r", encoding="utf-8")
lines = index.readlines()
start_time = time.clock()

# Download texts
for i in range(0, 18433834):
    rand = randint(1, 18459094)
    title = lines[rand].split(":")[2].strip("\n")
    if not any(title in file for file in os.listdir("..\\sample_set")):
        webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        file = open('..\\sample_set\\' + re.sub("[^\w\d_',\-\(\).]", " ", title, re.UNICODE) + '.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()
<<<<<<< HEAD:wikipedia_files/DownloadArticles.py
    count += 1
 
print(time.clock() - start_time, "seconds")

# 5000 articles: 1283.7004358 seconds: 0.2567 seconds per article

=======
    else:
        i -= 1
    print("Downloaded: " + title)
print(time.clock() - start_time, "seconds")
>>>>>>> devin:old_scripts/DownloadArticles.py
