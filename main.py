from flask import Flask
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    ablums = db.relationship('Album', backref='artist', lazy='dynamic')
    songs = db.relationship('Song', backref='song', lazy='dynamic')

    def __repr__(self):
        return f"Artist ID {self.id}, artist name {self.name}, albums are {self.albums}, songs of the artist are {self.songs}"

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    songs = db.relationship('Song', backref='album', lazy='dynamic')

    def __repr__(self):
        return f"Album ID {self.id}, album name {self.name}, artists on the album are {self.albums}, songs on said album are {self.songs}"

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

    def __repr__(self):
        return f"Song ID {self.id}, song name {self.name}, from artist {self.artist_id.name} on album {self.album_id.name}"

artist_post_args = reqparse.RequestParser()
artist_post_args.add_argument("name", type=str, help="Name of the artist", required=True)

album_post_args = reqparse.RequestParser()
album_post_args.add_argument("name", type=str, help="Name of the album", required=False)
album_post_args.add_argument('artist_id', type=int, help="ID of the artist", required=True)

song_post_args = reqparse.RequestParser()
song_post_args.add_argument("name", type=str, help="Title of the song", required=True)
song_post_args.add_argument("album_id", type=int, help="ID of the Album", required=True)
song_post_args.add_argument("artist_id", type=int, help="ID of the Artist", required=True)

song_get_args = reqparse.RequestParser()
song_get_args.add_argument("name", type=str, help="Title of the song", required=False)
song_get_args.add_argument("album_id", type=int, help="ID of the Album", required=True)
song_get_args.add_argument("artist_id", type=int, help="ID of the Artist", required=True)

artist_resource_fields = {
    'name': fields.String,
    'id': fields.Integer
}

album_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'artist_id': fields.Integer
}

song_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'artist_id': fields.Integer,
    'album_id': fields.Integer
}

class ArtistAPI(Resource):
    @marshal_with(artist_resource_fields)
    def get(self):
        args = artist_post_args.parse_args()
        result = Artist.query.filter_by(name=args['name']).first()
        if not result:
            abort(404, message="Could not find artist with this name.")
        return result
    
    @marshal_with(artist_resource_fields)
    def post(self):
        args = artist_post_args.parse_args()
        result = Artist.query.filter_by(name=args['name']).first()
        if result:
            abort(409, message="The artist name already exists.")
        artist = Artist(name=args['name'])
        db.session.add(artist)
        db.session.commit()
        return artist, 201

class AlbumAPI(Resource):
    @marshal_with(album_resource_fields)
    def get(self):
        args = album_post_args.parse_args()
        artist = Artist.query.filter_by(id=args['artist_id']).first()
        if not artist:
            abort(404, message="Artist ID does not exist.")
        result = Album.query.filter_by(artist_id=artist.id).all()
        if not result:
            abort(404, message="Could not find this Album")
        return result

    @marshal_with(album_resource_fields)
    def post(self):
        args = album_post_args.parse_args()
        artist = Artist.query.filter_by(id=args['artist_id']).first()
        if not artist:
            abort(404, message="Artist ID does not exist.")
        album = Album(name=args['name'], artist_id=artist.id)
        db.session.add(album)
        db.session.commit()
        return album

class SongAPI(Resource):
    @marshal_with(song_resource_fields)
    def get(self):
        args = song_get_args.parse_args()
        artist = Artist.query.filter_by(id=args['artist_id']).first()
        album = Album.query.filter_by(id=args['album_id']).first()
        if not artist and album:
            abort(404, message="Could not find an artist or album with this information")
        result = Song.query.filter_by(artist_id=artist.id, album_id=album.id).all()
        if not result:
            abort(404, message="Could not find this song")
        return result

    @marshal_with(song_resource_fields)
    def post(self):
        args = song_post_args.parse_args()
        artist = artist = Artist.query.filter_by(id=args['artist_id']).first()
        album = Album.query.filter_by(id=args['album_id']).first()
        if not artist and album:
            abort(404, message="Could not find an artist or album with this information")
        song = Song(name=args['name'], artist_id=artist.id, album_id=album.id)
        db.session.add(song)
        db.session.commit()
        return song
        
api.add_resource(ArtistAPI, "/artist")
api.add_resource(AlbumAPI, "/album")
api.add_resource(SongAPI, "/song")

if __name__ == "__main__":
    app.run(debug=True)
    
