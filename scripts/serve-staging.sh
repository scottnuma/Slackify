#!/bin/bash

# The staging script mounts the current director into the image to avoid
# having to rebuild the image for every change.

source .env

docker run \
	--name slackify-server \
	--env-file=.env \
	-p 0.0.0.0:443:5000 \
	--mount type=bind,source=$(pwd),target=/app \
	--mount type=bind,source="${SLACKIFY_SSL_DIR}",target="${SLACKIFY_SSL_DIR}" \
	--mount type=bind,source="${SLACKIFY_SSL_ARCHIVE}",target="${SLACKIFY_SSL_ARCHIVE}" \
	--rm \
	slackify