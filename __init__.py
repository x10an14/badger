#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)

logger.info("Importing views and models.")
from Views.badge import badge_view
import Models.card
import Views.test

application.register_blueprint(badge_view)

if __name__ == "__main__":
    application.run(debug=True)

