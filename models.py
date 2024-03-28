"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Playlist(db.Model):
    """Playlist."""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)

    songs = db.relationship("Song", secondary="playlists_songs", backref="playlists")

    def __repr__(self):
        """Show information about the playlist."""
        return f"<Playlist id: {self.id} name: {self.name} description: {self.description}>"


class Song(db.Model):
    """Song."""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Show information about the song."""
        return f"<Playlist id: {self.id} title: {self.title} artist: {self.artist}>"


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "playlists_songs"

    playlist_id = db.Column(
        db.Integer, db.ForeignKey("playlists.id"), primary_key=True, nullable=False
    )
    song_id = db.Column(
        db.Integer, db.ForeignKey("songs.id"), primary_key=True, nullable=False
    )


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
