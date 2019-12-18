import logging
import os

from slackify import celery
from slackify.app import create_app

ENVIRONMENT = os.getenv("FLASK_ENV", "production")

app = create_app(celery)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
