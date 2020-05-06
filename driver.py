# Functions to both pre-compute song lists for common moods and compute new queries
from emotion import SongList, Spotify, Artist, Rank, word_list, word_set
import os
import json
import thesaurus

def pre_compute(lst):
    sp = Spotify('auth.json').sp
    for i in lst:
        try:
            mlist = SongList(i, sp)
            mlist.search()
            mlist.save()
        except Exception as e:
            print(e)
            print('Error! ' + i + ' was the last attempted word')
            break
        

#Requires mood is lowercase
def CreateSongList(mood):
    sp = Spotify('auth.json').sp
    mlist = SongList(mood, sp)
    mlist.search()
    mlist.save()
    return mlist.getSongs()

def getSongList(mood, word_set, new_list = False):
    
    mood = mood.lower()
    assert(mood in word_set)
    if not new_list and mood in word_set:
        with open('moods/' + mood + '.json') as f:
            sl = json.load(f)
            return sl
    elif new_list:
        print('Creating new list for existing query...')
        return CreateSongList(mood)
    else:
        #Case 1: look through thesaurus to see if synonym exists 
        #Case 2: perform new query and save it

        #Case 1
        print('Checking thesaurus for new query...')
        root_and_syns = thesaurus.findRootandSynonyms(mood)

        for i in root_and_syns:
            i = i.lower()
            if i in word_set:
                with open('moods/' + i + '.json') as f:
                    return json.load(f)

        #Case 2
        print('Creating new list for new query...')
        with open('word_list.txt', 'a') as f:
            f.write(mood)
        word_set.add(mood)
        return CreateSongList(mood)


from itertools import groupby
def remove_duplicates(data):
    data.sort(reverse = True, key = lambda x: x[1])
    return [k for k, v in groupby(data)]


def getSongs(mood, start_index = 0, num_songs = 5, word_set = word_set('word_list.txt')):
    #Bad place to remove duplicates.... 
    #sl = getSongList(mood, word_set)
    #sl.sort(reverse = True, key = lambda x : x[1])
    sl = getSongList(mood, word_set)
    sl = remove_duplicates(sl)
    end = start_index + num_songs
    while(start_index < end):
        if start_index >= len(sl):
            break
        print(sl[start_index][0])
        start_index += 1

def RankSong(song, sp = Spotify('auth.json').sp):
    q = sp.search(song, type='track')
    q = q['tracks']['items'][0]
    artist = Artist(q['artists'][0]['id'], q['artists'][0]['name'], sp)
    rank = Rank(q['id'], q['name'], artist, sp)
    return rank.score()
    
def fix_moods():
    #Rename initally named files with '?' suffix
    os.chdir('moods/')
    for f in os.listdir():
        if f == 'morose.json' or f == 'love.json':
            continue
        f_new = ''
        for i in range(0, len(f)-1):
            if f[i+1] == '.':
                continue
            else:
                f_new += f[i]
        f_new += 'n'
        print(f_new)
        os.rename(f, f_new)

def remove_duplicates_from_all_moods():
    pass

if __name__ == '__main__':

    input_file = str(input('Enter file to pre-compute song lists: '))

    wl = word_list(input_file)

    pre_compute(wl)
