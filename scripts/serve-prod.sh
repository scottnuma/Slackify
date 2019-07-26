#!/bin/bash

# The staging script mounts the current director into the image to avoid
# having to rebuild the image for every change.

source .env

docker build -t slackify .

docker run \
	--name slackify-server \
	--env-file=.env \
	-p 0.0.0.0:80:5000 \
	slackify