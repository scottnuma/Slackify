from flask import Blueprint, current_app, render_template

basics = Blueprint("simplepage", __name__, template_folder="templates")


@basics.route("/healthcheck")
def healthy():
    """Provide quick affirmation of that the server is online"""
    current_app.logger.info("healthcheck ping")
    return "ok"


@basics.route("/")
def homepage():
    return render_template("index.html")


@basics.errorhandler(500)
def server_error(e):
    current_app.logger.error("An error occurred during a request.")
    return "An internal error occurred.", 500
