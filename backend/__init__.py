from flask import Flask

application = Flask(__name__)

# load configuration
application.config.from_object('config')

# import routes
from backend import routes