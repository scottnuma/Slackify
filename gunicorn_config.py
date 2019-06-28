"""Gunicorn Configuration File"""
import os
import dotenv

dotenv.load_dotenv()

if os.environ.get("FLASK_ENV") == "development":
    bind = "localhost:5000"
else:
    bind = "0.0.0.0:5000"
