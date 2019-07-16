#!/bin/bash
docker run \
    --name slackify-server \
    -p 0.0.0.0:5000:5000 \
    --env-file=.env \
    --rm \
    slackify
