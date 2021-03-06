import logging
import os

import slackify


ENVIRONMENT = os.getenv("FLASK_ENV", "production")

app = slackify.create_app()


if __name__ == "__main__":
    if ENVIRONMENT == "development":
        app.run(port=5000, host="0.0.0.0", debug=True, ssl_context="adhoc")
    else:
        app.run(port=5000, host="0.0.0.0", debug=True)
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
