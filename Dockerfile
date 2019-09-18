FROM kennethreitz/pipenv as env

ADD Pipfile.lock /app
WORKDIR /app

RUN pipenv sync

FROM env

COPY . /app

CMD ["bash", "/app/scripts/serve.sh"]