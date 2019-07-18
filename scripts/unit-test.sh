source /home/scott/Dropbox/gDrive/programming-master/slack/spotify-playlist-manager/.env

docker run \
    --env FLASK_ENV=$FLASK_ENV \
    --env FLASK_APP=$FLASK_APP \
    --env SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID \
    --env SPOTIPY_REDIRECT_URI=$SPOTIPY_REDIRECT_URI \
    --env VAULT_TOKEN=$VAULT_TOKEN \
    --env VAULT_ADDR=$VAULT_ADDR \
    --env PRODUCTION_URL=$PRODUCTION_URL \
    --name slackify-testing \
    slackify \
    pipenv run python -m unittest
