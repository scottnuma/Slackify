source /home/scott/Dropbox/gDrive/programming-master/slack/spotify-playlist-manager/.env

docker build -t slackify .

docker run \
    --env FLASK_ENV=testing \
    --env FLASK_APP=$FLASK_APP \
    --env SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID \
    --env SPOTIPY_REDIRECT_URI=$SPOTIPY_REDIRECT_URI \
    --env VAULT_TOKEN=$VAULT_TOKEN \
    --env VAULT_ADDR=$VAULT_ADDR \
    --env PRODUCTION_URL=$PRODUCTION_URL \
    --env GCLOUD_PROJECT=$GCLOUD_PROJECT \
    --env GOOGLE_APPLICATION_CREDENTIALS=/app/service_account.json \
    --env VAULT_GCP_SERVICE_ACCOUNT_LEASE_NAME_FILE=/app/lease.txt \
    --name slackify-testing \
    --rm \
    slackify \
    pipenv run python -m unittest
