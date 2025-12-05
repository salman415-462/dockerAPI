import sys
import os

# Add your app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from main import app

# This is the WSGI callable
application = app
