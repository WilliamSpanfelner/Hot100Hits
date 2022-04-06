from login import AddKeysAndValues as AKAV
import requests
import os
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

pp = pprint.PrettyPrinter(indent=4)


def get_hot_100_hits(date):
    # Returns a list of 100 hits for a user entered date in ascending order
    base_url = "https://www.billboard.com/charts/hot-100/"

    url = base_url + date + "/"

    # print(URL)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    chart_results = soup.find_all(name="div", class_="o-chart-results-list-row-container")

    return [result.h3.getText().strip() for result in chart_results]


def create_spotify_uri_song_list(date, song_list):
    year = date[:4]
    song_uri_list = []
    for song in song_list:
        results = spotify.search(q=f"track: {song} year:{year}", type="track")
        try:
            uri = results['tracks']['items'][0]['uri']
        except IndexError:
            print(f"'{song}' not found on Spotify")
        else:
            song_uri_list.append(uri)

    return song_uri_list

try:
    AKAV().setup_environment()
except KeyError:
    print("Unable to setup credentials")
else:
    SPOTIPY_CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
    SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
    SPOTIPY_REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']

    # Step 2 Authentication with Spotify
    # If multiple scopes are required separate them with %20 []
    # (https://stackoverflow.com/questions/51795449/spotify-api-token-scope-issue?rq=1)
    # scope = "user-library-read%20playlist-modify-private"
    modify_scope = "playlist-modify-private"

    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=modify_scope,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            show_dialog=True,
            cache_path="token.txt"
        )
    )
    user_id = spotify.current_user()["id"]
    print(f"user_id: {user_id}")

    # End - Step 2 Authentication with Spotify

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

hot_100 = get_hot_100_hits(date)
# print(hot_100)

# Step 3 - Search Spotify for the songs in hot_100
hit_uris = create_spotify_uri_song_list(date=date, song_list=hot_100)
# pp.pprint(hit_uris)
# End Step 3 - Search Spotify for the songs in hot_100

# Step 4 - Creating and Adding to a Spotify Playlist
playlist_name = f"{date} Billboard 100"
playlist = spotify.user_playlist_create(user=user_id, name=playlist_name, public=False)
# print(playlist)
play_id = playlist["id"]

spotify.playlist_add_items(playlist_id=play_id, items=hit_uris)

# End Step 4 - Creating and Adding to a Spotify Playlist


# spotify = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
# redirect_uri=SPOTIPY_REDIRECT_URI)

# results = spotify.current_user_saved_tracks()
# results = spotify.get_auth_response()
# results = spotify.search("Hooked On A Feeling")
# print(results)


# Create a playlist
# user = spotify.me()['id']
# print(user)
#
# token = util.prompt_for_user_token(
#     username=user,
#     scope=scope,
#     client_id=SPOTIPY_CLIENT_ID,
#     client_secret=SPOTIPY_CLIENT_SECRET,
#     redirect_uri=SPOTIPY_REDIRECT_URI
# )
#
#
# playlist = spotipy.Spotify(auth=token).user_playlist_create(user=user, name=playlist_name)
#
#
# # playlist = spotify.user_playlist_create(user=user, name=f"Hot-100-Hits-{date}",
# #                                         description=f"Boogie to the Hot-100-Hits of {date}")

