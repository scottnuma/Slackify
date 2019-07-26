"""Gunicorn Configuration File"""
import os
import dotenv

dotenv.load_dotenv()

bind = "0.0.0.0:5000"
