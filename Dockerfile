FROM kennethreitz/pipenv as env

ADD Pipfile.lock /app
WORKDIR /app

RUN pipenv sync

FROM env

COPY . /app

CMD ["pipenv", "run", "gunicorn", "-c", "gunicorn_config.py", "main:app"]