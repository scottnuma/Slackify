import os

import spotipy
import spotipy.util as util


token = util.prompt_for_user_token("newmascot")

def login(username):
    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    cache_dir = "caches"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_path = "{}/cache-{}".format(cache_dir, username)
    
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, 
        scope=scope, cache_path=cache_path)

    token_info = sp_oauth.get_cached_token()

    if token_info:
        # We're done early
        store_access_token(None, None, token_info['access_token'])
        # Return confirmation page
        return 200

    auth_url = sp_oauth.get_authorize_url()
    return auth_url

def process_spotify_auth_response(respones_url):
    code = sp_oauth.parse_response_code(response_url)
    token_info = sp_oauth.get_access_token(code)

    # Auth'ed API request
    if token_info:
        return token_info['access_token']

    return None

def store_access_token(id, username, access_token):
    """Stores an retrievable access token"""
    raise NotImplementedError