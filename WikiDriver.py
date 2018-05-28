# A script for handling the larger set of pre-processed wikipedia documents (driver)
import CleanWikiDoc
import bs4
import urllib.request
import Classification

# Get files from dump
def get_texts():
    to_return = {}
    index = open("C:\\Users\\useradmin\\Desktop\\index.txt", "r", encoding="utf-8")
    lines = index.readlines()
    for i in range (49636, 49645):
        title = lines[i].split(":")[2].strip("\n")
        webpage = str(urllib.request.urlopen("http://triton.zlw-ima.rwth-aachen.de:50001/wikipedia/getArticleByTitle?title=" + urllib.parse.quote_plus(title)).read())
        soup = bs4.BeautifulSoup(webpage, "lxml")
        to_return.update({title: CleanWikiDoc.process(soup.getText()).split()})
    return to_return


# Get all files and clean them. Makes a title : split/processed string dictionary
corpus = get_texts()

# Compute tfidf for each doc. Makes a title : (word:tfidf score dictionary) dictionary
tfidf = {}
for docTitle in corpus:
    tfidf.update({docTitle: Classification.calculate_tfidf(corpus[docTitle], corpus.values())})

# Compute word2vec representation of each doc.
for docTitle in corpus:
    Classification.compute_word2vec(corpus)
