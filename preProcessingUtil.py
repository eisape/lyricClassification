import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing
#takes a list of strings as input, outputs a POS tag in plae of every word in the corpus
def lyrics2POS(songs):
    fullPOSList = []
    for song in songs:
        #tokenize each word usign nltk
        words = word_tokenize(song)
        posTags = nltk.pos_tag(words)
        justTags = [tag for word, tag in posTags]
        fullPOSList.append(" ".join(justTags))
    return fullPOSList

#takes a list of strings as input, outputs a TF - IDF feature representations of the input
def vectorize(tokenizedList, rang):
    tfidfVectorizer = TfidfVectorizer(ngram_range=(1, rang), stop_words='english', analyzer='word')
    vector = tfidfVectorizer.fit_transform(tokenizedList).todense()
    return vector
