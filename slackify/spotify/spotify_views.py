from flask import Blueprint, current_app, redirect, url_for, request

from .spotify_auth import create_spotify_oauth, store_access_token

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
        store_access_token(None, None, cached_token_info['access_token'])
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
        store_access_token(None, None, token_info['access_token'])
        return redirect(url_for('spotifyRoutes.success'))
    except Exception:
        current_app.logger.exception("Failed to authorize with code from URL")
        return redirect(url_for('spotifyRoutes.failure'))

@spotify_routes.route('/auth/success')
def success():
    return 'success'

@spotify_routes.route("/auth/failure")
def failure():
    return "failure"