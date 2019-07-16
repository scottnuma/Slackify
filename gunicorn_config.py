"""Gunicorn Configuration File"""
import os
import dotenv

dotenv.load_dotenv()

bind = "0.0.0.0:5000"

if os.environ.get("FLASK_ENV") != "development":
    ssl_dir = os.environ.get("SLACKIFY_SSL_DIR", "")
    keyfile = ssl_dir + "privkey.pem"
    certfile = ssl_dir + "cert.pem"
    ca_certs = ssl_dir + "chain.pem"
