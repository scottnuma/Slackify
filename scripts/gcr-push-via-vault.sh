#!/bin/bash
set -e

docker tag slackify gcr.io/slack-spotify-playlist-226804/slackify
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request GET \
    $VAULT_ADDR/v1/gcp/token/gcr-pusher |\
    jq '.data.token' |\
    docker login -u oauth2accesstoken --password-stdin https://gcr.io
docker push gcr.io/slack-spotify-playlist-226804/slackify

