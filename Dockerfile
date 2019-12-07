FROM python:3.7 as requirements

RUN pip install pipfile-requirements

ADD Pipfile.lock /app/Pipfile.lock
WORKDIR /app

RUN pipfile2req Pipfile.lock > requirements.txt

FROM python:3.7 as runtime-image

WORKDIR /app
COPY --from=requirements /app/requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

CMD ["bash", "/app/scripts/serve.sh"]
