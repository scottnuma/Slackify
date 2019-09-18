#!/bin/bash
pipenv run gunicorn -b 0.0.0.0:5000 main:app
