FROM kennethreitz/pipenv as env

ADD Pipfile.lock /app
WORKDIR /app

RUN pipenv sync

FROM env

COPY . /app

ENTRYPOINT ["pipenv", "run", "gunicorn"]
CMD ["-c", "gunicorn_config.py", "main:app"]