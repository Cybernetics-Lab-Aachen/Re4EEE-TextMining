# A script for handling the larger set of pre-processed wikipedia documents (driver)
import CleanWikiDoc
import Classification

# Get files from database and clean and split them. Makes a title : split/cleaned string dictionary


# Compute tfidf for each doc. Makes a title : (word:tfidf score dictionary) dictionary
# tfidf = {}
# for docTitle in corpus:
#     tfidf.update({docTitle: Classification.calculate_tfidf(corpus[docTitle], corpus.values())})


# Compute word2vec representation of each doc.
# Classification.compute_word2vec(corpus.items())
