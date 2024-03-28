from flask import Flask, redirect, render_template, url_for

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///playlist-app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
with app.app_context():
    db.create_all()

app.config["SECRET_KEY"] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 page."""
    return render_template("404.html"), 404


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Playlist.query.get_or_404(playlist_id)

    return render_template("playlist.html", playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()

    if form.validate_on_submit():
        process_new_forms(Playlist(), form)
        return redirect("/playlists")

    else:
        redirect_url = url_for("show_all_playlists")
        return render_template("form_base.html", redirect_url=redirect_url, form=form)


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    song = Song.query.get_or_404(song_id)

    return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    form = SongForm()

    if form.validate_on_submit():
        process_new_forms(Song(), form)
        return redirect("/songs")

    else:
        redirect_url = url_for("show_all_songs")
        return render_template("form_base.html", redirect_url=redirect_url, form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    form.song.choices = set_song_choices(playlist)

    if form.validate_on_submit():

        song = Song.query.get_or_404(form.song.data)

        playlist.songs.append(song)

        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")
    else:
        redirect_url = url_for("show_playlist", playlist_id=playlist.id)
        return render_template(
            "form_base.html",
            redirect_url=redirect_url,
            form=form,
        )


##############################################################################
# Tools


def process_new_forms(db_obj, form) -> None:
    for field in form:
        setattr(db_obj, field.name, field.data)
    db.session.add(db_obj)
    db.session.commit()


def set_song_choices(playlist: Playlist) -> list[tuple[int, str]]:
    if playlist.songs != None:
        curr_on_playlist = {song.id for song in playlist.songs}
        songs = Song.query.all()
        if songs != None:
            return_list = [
                (song.id, song.title)
                for song in songs
                if song.id not in curr_on_playlist
            ]
            if return_list == []:
                return [(0, "All songs are already in this playlist!")]
            else:
                return_list.insert(0,(0, "Select an option"))
                return return_list
