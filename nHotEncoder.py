def nHotEncoder(songs):
    genresIndeces = {
    'pop' : 0,
    'rap' : 1,
    'rock' : 2,
    'r&b' : 3,
    'country' : 4,
    'jazz' : 5,
    'blues' : 6,
    'gospel' : 7,
    'reggae' : 8,
    'electronic' : 9
    }
    encodings = []
    for song in songs:
        hotVal = 1.0/len(song.genres)
        zeros  = [0 for i in range(len(genresIndeces))]
        for genre in song.genres:
            zeros[genresIndeces[genre]] = hotVal
        encodings.append(zeros)
    return encodings
