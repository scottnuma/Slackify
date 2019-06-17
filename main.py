import slackify
import os

ENVIRONMENT = os.getenv("SLACK_MUSIC_ENVIRONMENT", "prod")

app = slackify.create_app()

if ENVIRONMENT == "dev":
    app.run(port=5000, host='0.0.0.0', debug=True, ssl_context='adhoc')