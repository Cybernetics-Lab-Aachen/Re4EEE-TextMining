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
count = 0

# Download relevant texts
rand = randint(1, 18458000)
for i in range(rand, rand + 1000):
    if count > 1000:
        exit(0)
    title = lines[i].split(":")[2].strip("\n")
    if not any(title in file for file in os.listdir("..\\sample_set")):
        webpage = requests.get("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).content
        soup = bs4.BeautifulSoup(webpage, "lxml")
        text = soup.getText().lower()
        if ('learn' in text or 'educat' in text) and ('teach' in text or 'student' in text) \
                and ('method' in text or 'tool' in text or 'concept' in text or 'platform' in text or 'tech' in text):
            file = open('..\\sample_set\\' + re.sub("[^A-Za-z]", " ", title) + '.txt', 'w', encoding='utf-8')
            file.write(text)
            file.close()
    count += 1
    print(time.clock() - start_time, "seconds")

# First runtime: 113.6837302730916 seconds
# Second runtime: 124.2169789555012 seconds
# Third runtime: 111.41879792404077 seconds
# Fourth runtime: 111.0834045599835 seconds
# Fifth runtime: 98.12181727716322 seconds
>>>>>>> 0d932cc38b4ac73f5e8336d91e884224567c7d03
