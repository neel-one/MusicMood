# Mood-based Music Recommendations using crowdsourcing and ranking

**Table of Contents**
1. App
2. Usage

**App**

Home Page
![](static/home_page.png)
Results for 'agitated'
![](static/rec_ex.png)
Example of scoring the song 'Electricity'
![](static/rank_ex.png)
Page showing a basic overview of how recommendations work
![](static/flow_page.png)


**Usage**

Clone the repository
```
$git clone https://github.com/neel-one/MusicMood.git
```
Install the necessary packages
```
$pip install spotipy
$pip install flask
```

Optional:
Pre-compute song lists for common moods
```
$python driver.py
$word_list.txt
```

Set up flask
```
$export FLASK_ENV=app.py
```

Run the program!
```
$flask run
```

Go to your favorite port to see the app (don't use this for production!)
