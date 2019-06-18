from flask import Blueprint, current_app, redirect, url_for, request
import sqlite3

from .spotify_auth import create_spotify_oauth, store_access_token, DB_FILE

spotify_routes = Blueprint('spotifyRoutes', __name__)

@spotify_routes.route('/auth/init')
def authorize():
    username = "newmascot"
    current_app.logger.info("authorizing %s", username)
    spotify_oauth = create_spotify_oauth(username)

    # Attempt for cached token
    cached_token_info = spotify_oauth.get_cached_token()

    if cached_token_info:
        current_app.logger.info("found cached token")
        conn = sqlite3.connect(DB_FILE)
        store_access_token(conn, b"newmascot_id", cached_token_info['access_token'])
        return redirect(url_for('spotifyRoutes.success'))

    current_app.logger.info("failed to find cached token")

    # Attempt full authorization
    auth_url = spotify_oauth.get_authorize_url()
    return redirect(auth_url)


@spotify_routes.route('/auth/finish')
def handle_auth():
    """Receive the token from a successful authorization."""
    username = "newmascot"
    current_app.logger.info("handling Spotify auth callback for %s", username)
    spotify_oauth = create_spotify_oauth(username)

    try:
        code = spotify_oauth.parse_response_code(request.url)
        token_info = spotify_oauth.get_access_token(code)
        conn = sqlite3.connect(DB_FILE)
        store_access_token(conn, b"newmascot_id", token_info['access_token'])
        return redirect(url_for('spotifyRoutes.success'))
    except Exception:
        current_app.logger.exception("Failed to authorize with code from URL")
        return redirect(url_for('spotifyRoutes.failure'))

@spotify_routes.route('/auth/success')
def success():
    # It might be nice to send a message to the Slack channel
    # indicating that the account has been linked
    return 'success'

@spotify_routes.route("/auth/failure")
def failure():
    return "failure"