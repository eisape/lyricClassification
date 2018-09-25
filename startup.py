import song
from loadsongs import *
from classifier import *
from nHotEncoder import *
from preProcessingUtil import *

#This file provides some basic code to get started with.

folder = 'data/larkin1000_v2' #Replace with a folder of .pkl files containg Song objects


#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loadDataFromAlbums(getLarkin1000(), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling
songs = load(folder, song.GENRES)
songs = clusteredSample(songs, 500, song.GENRES)

#Print the info for the first 10 songs:
for s in songs[:10]:
    print(s.title, 'by', s.artist+':',s.genres)
print()

#Print the genre frequencies
genreDistribution(songs)

# Instead of including models weights which sized in the hundreds of megabytes, here
# we provide a quick tutorial to quickly train and deploy a text classifier

# First, transform your song list into a list of simple lyrics stripped of punctuation
# and auxilary characters
lyricsList  = [song.simpleLyrics() for song in songs]

#Vectorize using functions from preProcessUtil.py
data = vectorize(lyricsList, 1).tolist()
inputLayerLength = len(data[0])

#Computes nhot labels based on the genre distribution of each given song
nhotLabels = nHotEncoder(songs)

# modelBuilder returns a model with parameters describe in our write up
# here is an example of our most standard model
model = modelBuilder(inputLayerLength, 10)
model.fit(np.array(data), np.array(nhotLabels), n_epoch=20, batch_size=50, show_metric=True)

#returns a probabilty distribution over each of our possible genres
print model.predict(np.array([data[0]]))
