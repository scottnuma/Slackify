from flask import Flask

from ensemble.blueprints.basics import basics
from ensemble.config import Config
from ensemble.slack import register_slack


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = Config.FLASK_SESSION_KEY

    app.register_blueprint(basics)
    register_slack(app)
    return app
