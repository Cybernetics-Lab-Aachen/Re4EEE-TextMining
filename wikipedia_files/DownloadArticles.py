import bs4
import requests
import os
import urllib.parse
import re
import time
from random import randint
import sqlite3


# # Connect to sqlite
# connection = sqlite3.connect('wikiarticles.db')
# c = connection.cursor()

# Read index file
index = open("C:\\Users\\useradmin\\Desktop\\index.txt", "r", encoding="utf-8")
lines = index.readlines()
start_time = time.clock()

# Download relevant texts
rand = randint(1, 18458000)
for i in range(rand, rand + 1000):
    title = lines[i].split(":")[2].strip("\n")
    if not any(title in file for file in os.listdir(".\\files_of_interest")):
        webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        if ('learn' in text or 'educat' in text) and ('teach' in text or 'student' in text) \
                and ('method' in text or 'tool' in text or 'concept' in text or 'platform' in text or 'tech' in text):
            file = open('.\\files_of_interest\\' + re.sub("[^A-Za-z]", " ", title) + '.txt', 'w', encoding='utf-8')
            file.write(text)
            file.close()
print(time.clock() - start_time, "seconds")
