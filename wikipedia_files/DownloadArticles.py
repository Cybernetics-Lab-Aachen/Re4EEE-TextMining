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

# Download relevant texts
rand = randint(1, 18453000)
for i in range(rand, rand + 5000):
    title = lines[i].split(":")[2].strip("\n")
    if not any(title in file for file in os.listdir("C:\\Users\\useradmin\\Documents\\Re4EEE-TextMining\\sample_set")):
        webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        file = open('C:\\Users\\useradmin\\Documents\\Re4EEE-TextMining\\sample_set\\' + re.sub("[^\w\d']", " ", title, re.UNICODE) + '.txt', 'w', encoding='utf-8')
        file.write(text)
        file.close()
        print("processed " + title)
print(time.clock() - start_time, "seconds")
