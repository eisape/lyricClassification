#Modified from https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/

import requests
import locale
from bs4 import BeautifulSoup
from song import Song

#Do not change!
base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer nmTRwnDzAujQLr3voLlJhjAfty-sDacg89_vyGhFC7seVLdi5oeKlurmQzB2J9hF'}

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics[h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_ = "lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics

def getSong(song_title='', artist_name ='', genres = [], notfound = 'ignore'):
#Returns Song object based on the search results for the song title,
#choosing the first result with the artist_name in the full artist string
    search_url = base_url + "/search"
    params = {'q': song_title + " " + artist_name}
    response = requests.get(search_url, params=params, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower(): #requires artist_name is substring of Genius's artist name
            song_info = hit
            song_title = hit["result"]["title"]
            artist_name = hit["result"]["primary_artist"]["name"]
            break
    #it looked like the strings were in bitwise format so I decoded them
    if song_info:
        #print(song_title.decode('utf-8'))
        song_api_path = song_info["result"]["api_path"]
# <<<<<<< HEAD
#         return Song(lyrics_from_song_api_path(song_api_path).decode('utf-8'), song_title.decode('utf-8'), artist_name.decode('utf-8'))
# =======
        return Song(lyrics_from_song_api_path(song_api_path), genres, str(song_title), str(artist_name), notfound)
    else:
        return None
