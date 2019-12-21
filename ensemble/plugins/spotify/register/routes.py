import logging

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_wtf import Form
from spotipy import Spotify
from wtforms import RadioField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from ensemble.config import Config
from ensemble.plugins.spotify.auth import create_spotify_oauth
from ensemble.plugins.spotify.database import get_spotify_db
from ensemble.plugins.spotify.register.database import delete_channel
from ensemble.plugins.spotify.register.database import get_access_token
from ensemble.plugins.spotify.register.database import get_playlist_user
from ensemble.plugins.spotify.register.database import store_access_token
from ensemble.plugins.spotify.register.database import store_playlist_id
from ensemble.plugins.spotify.register.database import store_user_id
from ensemble.plugins.spotify.register.database import verify_token
from ensemble.plugins.spotify.spotify import get_playlists
from ensemble.plugins.spotify.spotify import get_username

logger = logging.getLogger(__name__)

spotify_routes = Blueprint("spotifyRoutes", __name__)


@spotify_routes.route("/unlink/<string:channel_id>/<string:token>")
def unlink(channel_id, token):
    """Disassociates a channel and a playlist"""
    if not verify_token(get_spotify_db(), channel_id, token):
        if Config.ENVIRONMENT == "development":
            current_app.logger.info("Skipping invalid token")
        else:
            return redirect(url_for("spotifyRoutes.failure"))
    delete_channel(get_spotify_db(), channel_id)
    current_app.logger.info("unlinked channel %s", channel_id)
    return redirect(url_for("spotifyRoutes.success"))


@spotify_routes.route("/link/<string:id>/<string:token>")
def authorize(id, token):
    """
    Creates a session linking to the channel
    and redirects to the Spotify authorization URL
    which will redirect to handle_auth
    """
    if not verify_token(get_spotify_db(), id, token):
        if Config.ENVIRONMENT == "development":
            current_app.logger.info("Skipping invalid token")
        else:
            return redirect(url_for("spotifyRoutes.failure"))

    session["id"] = id
    current_app.logger.info("authorizing %s", id)
    spotify_oauth = create_spotify_oauth(id)
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)


@spotify_routes.route("/auth/finish")
def handle_auth():
    """
    Receive the token from a successful authorization.
    Stores the Spotify information and directs the user
    to select their playlist.
    """
    channel_id = session.get("id")
    if channel_id is None:
        return redirect(url_for("spotifyRoutes.failure"))

    current_app.logger.info("handling Spotify auth callback for %s", id)
    spotify_oauth = create_spotify_oauth(id)

    try:
        code = spotify_oauth.parse_response_code(request.url)
        token_info = spotify_oauth.get_access_token(code)
        token = token_info["access_token"]

        sp = Spotify(token)
        spotify_user_id = get_username(sp)
        store_user_id(get_spotify_db(), channel_id, spotify_user_id)
        store_access_token(get_spotify_db(), spotify_user_id, token)
        current_app.logger.info("successfully stored access token and username")

        return redirect(url_for("spotifyRoutes.select_playlist"))
    except Exception:
        current_app.logger.exception("Failed to authorize with code from URL")
        return redirect(url_for("spotifyRoutes.failure"))


@spotify_routes.route("/select_playlist", methods=["GET", "POST"])
def select_playlist():
    """
    Displays a bunch of playlists to choose from.
    """
    channel_id = session.get("id")
    if channel_id is None:
        return redirect(url_for("spotifyRoutes.failure"))

    current_app.logger.info("select playlists for %s", channel_id)

    query = get_playlist_user(get_spotify_db(), channel_id)
    if query is None:
        return redirect(url_for("spotifyRoutes.authorize", id=channel_id))
    spotify_user_id = query[1]
    token = get_access_token(get_spotify_db(), spotify_user_id)
    if token is None:
        return redirect(url_for("spotifyRoutes.authorize", id=channel_id))

    sp = Spotify(token)

    form = PlaylistForm()
    form.playlist_id.choices = get_playlists(sp, spotify_user_id)

    if request.method == "POST":
        if not form.validate():
            flash("Please select a playlist.")
            return render_template("select_playlist.html", form=form)
        current_app.logger.info("chose playlist: %s", form.playlist_id.data)
        store_playlist_id(get_spotify_db(), channel_id, form.playlist_id.data)
        if "id" in session:
            session.pop("id")
        return redirect(url_for("spotifyRoutes.success"))

    return render_template("select_playlist.html", form=form)


class PlaylistForm(Form):
    playlist_id = RadioField(
        "Select playlist to connect:", choices=[], validators=[DataRequired()]
    )
    submit = SubmitField("Send")
