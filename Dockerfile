FROM kennethreitz/pipenv

ADD Pipfile.lock /app
WORKDIR /app

RUN pipenv sync

ADD . /app

ENTRYPOINT ["pipenv", "run", "gunicorn"]
CMD ["-c", "gunicorn_config.py", "main:app"]