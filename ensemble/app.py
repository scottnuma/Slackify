from flask import Flask

from ensemble import celery
from ensemble.blueprints.basics import basics
from ensemble.config import Config
from ensemble.slack import register_slack


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = Config.FLASK_SESSION_KEY

    app.register_blueprint(basics)
    register_slack(app)

    init_celery(celery, app)
    return app


def init_celery(celery, app: Flask):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.Flask.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
