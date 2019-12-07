import slack
from flask import Blueprint
from flask import current_app
from flask import request

from slackify.settings import Config

oauth = Blueprint("oauth", __name__)


@oauth.route("/oauth", methods=["GET", "POST"])
def install():
    if request.args.get("error") is not None:
        return "oh no"

    auth_code = request.args["code"]

    client = slack.WebClient(token="")

    # Request the auth tokens from Slack
    response = client.oauth_access(
        client_id=Config.SLACK_CLIENT_ID,
        client_secret=Config.SLACK_CLIENT_SECRET,
        code=auth_code,
    )

    current_app.logger.info(response)
    return "auth complete"
