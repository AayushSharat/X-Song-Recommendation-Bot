import tweepy
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import datetime
import time
import schedule


load_dotenv()


def get_client_tw():
    return tweepy.Client(
        consumer_key=os.getenv("TW_CONSUMER_KEY"),
        consumer_secret=os.getenv("TW_CONSUMER_SECRET"),
        access_token=os.getenv("TW_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TW_ACCESS_TOKEN_SECRET"),
    )

client_tw = get_client_tw()


client_sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SP_CLIENT_ID"),
    client_secret=os.getenv("SP_CLIENT_SECRET"),
))


def post_song_of_the_day():
    playlist_id = "4XzA7ssmE4Z4IMynLBM0Q2"  
    results = client_sp.playlist_tracks(playlist_id)


    song_item = random.choice(results['items'])
    track = song_item['track']
    name = track['name']
    artist = track['artists'][0]['name']
    url = track['external_urls']['spotify']


    today = datetime.date.today().strftime("%d %b %Y")
    tweet_text = f"🎵 Song of the Day ({today}):\n{name} by {artist}\nListen: {url}\n#SongRecommendations"


    try:
        client_tw.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
    except Exception as e:
        print("Error:", e)

# Schedule at 9:00 AM daily
schedule.every().day.at("11:30").do(post_song_of_the_day)

print("Bot started... waiting for schedule")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(30)
