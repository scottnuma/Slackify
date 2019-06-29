"""Gunicorn Configuration File"""
import os
import dotenv

dotenv.load_dotenv()

if os.environ.get("FLASK_ENV") == "development":
    bind = "localhost:5000"
else:
    bind = "0.0.0.0:5000"
    ssl_dir = os.environ.get("SLACKIFY_SSL_DIR", "")
    keyfile = ssl_dir + "privkey.pem"
    certfile = ssl_dir + "cert.pem"
    ca_certs = ssl_dir + "chain.pem"
