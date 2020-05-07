import json
from json.decoder import JSONDecodeError
import os
import spotipy
import spotipy.util as util
import random



def word_set(in_file):
    common_emotions = set()
    with open(in_file) as f:
        for line in f:
            common_emotions.add(line.rstrip('\n'))
    return common_emotions

def word_list(in_file):
    common_emotions = []
    with open(in_file) as f:
        for line in f:
            common_emotions.append(line.rstrip('\n'))
    return common_emotions

class Spotify:
    def __init__(self, auth):
        username = 'NSTHE1'
        with open(auth) as f:
            data = json.load(f)
            id = data['id']
            secret = data['secret']
            uri = data['redirect']
            
        scope = 'playlist-modify-public'
        try:
            token = util.prompt_for_user_token(username, scope, id,secret,uri)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope, id, secret, uri)
        assert token
        self.sp = spotipy.Spotify(auth=token)  

#Only create this class when needing to compute a new song_list
class SongList:
    
    def __init__(self, mood, sp=None, num_playlists = 5, spp=20, DEBUG = True):
        self.sp = sp #spotify api object
        self.spp = spp #songs per playlist
        self.DEBUG = DEBUG
        self.rand = []
        self.playlist_ids = []
        self.songs = []
        self.mood = mood
        self.num_playlists = num_playlists

    def genRand(self):
        for _ in range(0, self.num_playlists):
            if(self.DEBUG):
                random.seed(10)
            #self.rand.append(random.randrange(0, self.num_playlists))
            self.rand.append(random.randrange(0, 50))

    def search(self):
        if(self.sp is None):
            print('To create a new songlist, you must pass in a Spotify object')
            return
        
        
        #query = self.sp.search(self.mood, type='playlist', limit=self.num_playlists)
        query = self.sp.search(self.mood,type='playlist',limit=50)
        #playlist_samples = random.sample(query['playlists']['items'], self.num_playlists)

        #self.num_playlists = len(query['playlists']['items'])
        self.genRand()

        for i in range(0, self.num_playlists):
            self.playlist_ids.append(query['playlists']['items'][self.rand[i]]['id'])
    
        
        for i in range(0, len(self.playlist_ids)):
            #get playlists tracks --> class Rank, with artist data
            #compute Rank
            #sort by rank, and keep top 100
            #Store in JSON
            s = self.sp.playlist_tracks(self.playlist_ids[i], fields='items')
            

            tracks = random.sample(s['items'], min(len(s['items']), self.spp))
            #print('pass2')
            #print(len(tracks))

            for j in range(0, len(tracks)):
                try:
                    song_name = tracks[j]['track']['name']
                    song_id = tracks[j]['track']['id']
                    #print('pass3')
                    primary_artist = tracks[j]['track']['artists'][0]['name']
                    primary_artist_id = tracks[j]['track']['artists'][0]['id']
                    #print('pass4')
                    artist = Artist(primary_artist_id, primary_artist, self.sp)
                    rank = Rank(song_id, song_name, artist, self.sp)
                    self.songs.append((song_name, rank.score()))
                except:
                    pass

    def getSongs(self):
        return self.songs

    def save(self):
        with open('moods/' + self.mood + '.json', 'w+') as f:
            json.dump(self.songs, f, indent=4)
        print('Successfully saved ' + self.mood  + '.json')



class Artist:
    
    def __init__(self, _id, name, sp = None):
        self.sp = sp
        self.name = name
        self.id = _id
        #self.loaded = False
        if os.path.exists("artists/" + self.id + ".json"):
            print("Loading artist from file")
            with open('artists/' + self.id + '.json') as f:
                self.data = json.load(f)
            #self.loaded = True
        else:
            print("Creating new artist")
            self.data = dict()
            self.data['class'] = 'Artist'
            self.data['name'] = name
            self.data['id'] = self.id
            self.discover_data()
            with open('artists/' + self.id + '.json', 'w+') as f:
                json.dump(self.data, f, indent=4)

    def discover_data(self):
        artist = self.sp.artist(self.id)
        self.data['followers'] = artist['followers']['total']
        self.data['popularity'] = artist['popularity']


class Rank:

    #Artist popularity, followers, etc.
    def __init__(self, song_id, song_name, Artist, sp, debug = True):
        #if rank exists load from json
        self.sp = sp
        self.id = song_id
        self.name = song_name
        self.artist = Artist

        if os.path.exists("songs/" + self.id + ".json"):
            print("Loading song from file")
            with open('songs/' + self.id + '.json') as f:
                self.data = json.load(f)
                self.rank = self.data['rank']

        else:
            print("Creating new song")
            self.data = dict()
            self.data['class'] = 'Song'
            self.data['name'] = self.name
            self.data['id'] = self.id
            self.rank = self.computeRank()
            self.data['rank'] = self.rank
            self.data['artist'] = self.artist.data
            with open('songs/' + self.id + '.json', 'w+') as f:
                json.dump(self.data, f, indent=4)


    def computeRank(self):
        tr = self.sp.track(self.id)
        song_popularity = tr['popularity']
        self.data['popularity'] = song_popularity
        artist_popularity = self.artist.data['popularity']
        artist_followers = self.artist.data['followers']
        import create_eqn as t
        return t.EQ1(artist_popularity, artist_followers, song_popularity)

    def score(self):
        return self.rank

