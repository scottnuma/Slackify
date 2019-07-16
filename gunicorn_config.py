"""Gunicorn Configuration File"""
import os
import dotenv

dotenv.load_dotenv()

bind = "0.0.0.0:5000"

if os.environ.get("FLASK_ENV") != "development":
    _ssl_dir = os.environ.get("SLACKIFY_SSL_DIR", "")
    keyfile = _ssl_dir + "privkey.pem"
    certfile = _ssl_dir + "cert.pem"
    ca_certs = _ssl_dir + "chain.pem"
