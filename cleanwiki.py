# A script for cleaning up wikipedia dumps and preprocessing
import re
file = open("testfile.txt", "r", encoding="utf8") 
text = file.read()
text = re.sub('[^a-zA-Z]+', '*', text).lower().replace("[", "").replace("]", "").replace("/", "")