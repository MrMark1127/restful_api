# MrMark1127
Functional Flask RESTful API to sort artists, albums and songs within a relational database.

## Features
- Create and deploy a relational database with references to the artist, album and song.
- Use POST, GET, PATCH, etc methods to add, retrieve, or update the database as necessary.

## Dependencies
As illustrated in the *requirements.txt* file the dependencies for this API are:
- aniso8601==8.0.0
- click==7.1.2
- Flask==1.1.2
- Flask-RESTful==0.3.8
- Flask-SQLAlchemy==2.4.3
- itsdangerous==1.1.0
- Jinja2==2.11.2
- MarkupSafe==1.1.1
- pytz==2020.1
- six==1.15.0
- SQLAlchemy==1.3.18
- Werkzeug==1.0.1

## Usage
For example, we could use the following code to retrieve all songs from the given artist ID under that specific album.
`response = requests.get(BASE + "song", {"artist_id":2, "album_id":1})`

We could use the same code as above but modified for a post request to add an entry to the database with the song name, artist and album.
`response = requests.post(BASE + "song", {"name":"Mark's Song", "artist_id":2, "album_id":1})`

Adding artists to the database via `response = requests.post(BASE + "/artist", {"name":"Brennan"})`

Creating an album under the new artist given ID 3 in response would go as follows `response = requests.post(BASE + "/album", {"name":"Brennan's Album", "artist_id":3})`

## Changelog
v1.0 Initial Release | Base functionality of backend services

## Todo
- Adding monthly plays to artist table
- Adding a brief biography of said artist
- Adding a place for featured artists in the database relationship
- Pushing changes to the database via frontend-backend communication

#### Thank you's
- Tech With Tim
- Mdp18
- Brennan08512
