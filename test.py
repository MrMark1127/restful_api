import requests

BASE = "http://127.0.0.1:5000/"

""" response = requests.post(BASE + "song", {"name":"Max's Song", "artist_id":2, "album_id":1})
print(response.json())
input() """
response = requests.get(BASE + "song", {"artist_id":2, "album_id":1})
print(response.json())