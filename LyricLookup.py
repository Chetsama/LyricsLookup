import csv
import urllib

import pandas as pd
import requests
import bs4
import lyricsgenius
import json
import sys
genius = lyricsgenius.Genius('BT4caXU5NGVr5IS0tYVueelDTCVF46_OKmF7mCx2z7S4ebk95mCaX-OHbkUC9dFn')

def myprint(string):
    return string.encode(sys.stdout.encoding, errors='replace')

def getSongPath(track, artist):
    searchTerm = "{} by {}".format(track, artist)
    data = genius.search(searchTerm, per_page=1)
    #print(json.dumps(data, indent=4))
    song_path = data['hits'][0]['result']['api_path']

    retVal = genius.song(song_id=song_path.split('/')[2])
    songPath = song_path.split('/')[2]

    #print(songPath)
    lyrics = genius.lyrics(songPath)
    #print(lyrics)
    retList = []
    retList.append(track)
    retList.append(artist)
    retList.append(myprint(lyrics))
    return retList

def writeFile(list):

    with open("Lyrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(list)

# def getLyrics(track,artist):
#     client_access_token = 'BT4caXU5NGVr5IS0tYVueelDTCVF46_OKmF7mCx2z7S4ebk95mCaX-OHbkUC9dFn'
#     base_url = 'https://api.genius.com'
#     path ='search'
#     request_uri = '/'.join([base_url, path])
#     params = {'q': "{} by {}".format(track,artist)}
#     token = 'Bearer {}'.format(client_access_token)
#     headers = {'Authorization': token}
#
#     r = requests.request(request_uri, params=params, headers=headers)
#
#     return r

def readCSV():
    csv = pd.read_csv('csv/songs.csv')
    return csv

def importCSV():
    data = readCSV()

    return data

def main():
    outputdict = [['Track', 'Artist', 'Lyrics']]
    csv = importCSV()
    df = pd.DataFrame(columns=['Track', 'Artist', 'Album', 'Duration', 'Explicit', 'Lyrics'])
    print(len(csv))
    print(csv.loc[1,:])
    colHead = ['Track', 'Artist', 'Album', 'Duration', 'Explicit']
    for i in range(len(csv)):
        row = csv.loc[i, :]
        try:
            print("{} by {}".format(row.loc['Track'], row.loc['Artist']))
            lyrics = getSongPath(row.loc['Track'],row.loc['Artist'])
            print(lyrics)
            #outputList = [row.loc['Track'],row.loc['Artist'],row.loc['Album'],row.loc['Duration'],row.loc['Explicit'],lyrics]
            outputdict.append(lyrics)

        except:
            print('nope')

    writeFile(outputdict)

if __name__ == "__main__":
    main()