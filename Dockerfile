FROM kennethreitz/pipenv

ADD Pipfile.lock /app
WORKDIR /app

RUN pipenv sync

ADD . /app

ENTRYPOINT ["pipenv", "run", "flask", "run"]
CMD ["--host", "0.0.0.0", \
     "--port", "5000"]