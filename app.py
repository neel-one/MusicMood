from flask import Flask, redirect, url_for, request, render_template
import driver


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def display_songs():
    mood = request.form['mood']
    num = request.form['num']
    songs = driver.getSongs(mood, int(num)*5)
    return render_template('index.html', song_list = songs, _len = len(songs), mood = mood)

@app.route('/rank')
def rank_page():
    return render_template('rank.html')

@app.route('/rank', methods=['POST'])
def rank():
    song = request.form['song']
    score = driver.RankSong(song)
    return render_template('rank.html', score = score, song = song.upper() )

@app.route('/how')
def how():
    return render_template('how.html')

if __name__ == '__main__':

    app.run()