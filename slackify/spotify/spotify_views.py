from flask import (
    Blueprint,
    current_app,
    redirect,
    url_for,
    request,
    session,
    render_template,
)
import sqlite3
import spotipy

from .spotify_auth import create_spotify_oauth
from .spotify_database import (
    store_access_token,
    get_access_token,
    store_user_id,
    store_playlist_id,
    get_db,
    get_playlist_user,
)
from .spotify import get_username, get_playlists


spotify_routes = Blueprint("spotifyRoutes", __name__, template_folder="templates")


@spotify_routes.route("/auth/init/<string:id>")
def authorize(id):
    session["id"] = id
    current_app.logger.info("authorizing %s", id)
    spotify_oauth = create_spotify_oauth(id)
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)


@spotify_routes.route("/auth/finish")
def handle_auth():
    """Receive the token from a successful authorization."""
    channel_id = session.get("id")
    if channel_id is None:
        return redirect(url_for("spotifyRoutes.failure"))

    current_app.logger.info("handling Spotify auth callback for %s", id)
    spotify_oauth = create_spotify_oauth(id)

    try:
        code = spotify_oauth.parse_response_code(request.url)
        token_info = spotify_oauth.get_access_token(code)
        token = token_info["access_token"]

        sp = spotipy.Spotify(token)
        spotify_user_id = get_username(sp)
        store_user_id(get_db(), channel_id, spotify_user_id)
        store_access_token(get_db(), spotify_user_id, token)
        current_app.logger.info("successfully stored access token and username")

        return redirect(url_for("spotifyRoutes.select_playlist"))
    except Exception:
        current_app.logger.exception("Failed to authorize with code from URL")
        return redirect(url_for("spotifyRoutes.failure"))


@spotify_routes.route("/select_playlist/channel_id/<string:channel_id>")
def set_id_to_select_playlist():
    """Sets channel_id and redirects to select_playlist"""
    session["id"] = id
    current_app.logger.info("set id to %s or selecting playlist", id)
    return redirect(url_for("spotifyRoutes.select_playlist"))


@spotify_routes.route("/select_playlist", methods=["GET", "POST"])
def select_playlist():
    """Displays a bunch of playlists to choose from"""
    if request.method == "POST":
        try:
            # Discard the channel id
            channel_id = session.pop("id")
            playlist_id = request.form["playlist-id"]
        except KeyError:
            return redirect(url_for("spotifyRoutes.failure"))

        store_playlist_id(get_db(), channel_id, playlist_id)
        return redirect(url_for("spotifyRoutes.success"))

    channel_id = session.get("id")
    if channel_id is None:
        return redirect(url_for("spotifyRoutes.failure"))

    current_app.logger.info("select playlists for %s", channel_id)

    query = get_playlist_user(get_db(), channel_id)
    if query is None:
        return redirect(url_for("spotifyRoutes.failure"))
    _, spotify_user_id = query
    token = get_access_token(get_db(), spotify_user_id)
    if token is None:
        return redirect(url_for("spotifyRoutes.failure"))

    sp = spotipy.Spotify(token)

    playlists = get_playlists(sp, spotify_user_id)
    return render_template("select_playlists.html", playlists=playlists)


@spotify_routes.route("/auth/logout")
def logout():
    channel_id = session.pop("id", None)
    if channel_id is None:
        return "already logged out"
    else:
        return "successfully logged out"


@spotify_routes.route("/auth/success")
def success():
    # It might be nice to send a message to the Slack channel
    # indicating that the account has been linked
    return "success"


@spotify_routes.route("/auth/failure")
def failure():
    return "failure"
