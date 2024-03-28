"""Forms for playlist app."""

from wtforms import SelectField, StringField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, NoneOf


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField("Playlist Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    # Add the necessary code to use this form


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField("Song Title", validators=[InputRequired()])
    artist = StringField("Artist Name", validators=[InputRequired()])

    # Add the necessary code to use this form


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
# I added error functionality
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField("Song To Add", coerce=int, validators=[NoneOf([0], message='Please select a valid option')])
