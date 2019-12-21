import logging

from ensemble.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
