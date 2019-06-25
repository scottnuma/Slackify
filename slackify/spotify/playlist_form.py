from flask_wtf import Form
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired


class PlaylistForm(Form):
    playlist_id = RadioField(
        "Select playlist to connect:", choices=[], validators=[DataRequired()]
    )
    submit = SubmitField("Send")
