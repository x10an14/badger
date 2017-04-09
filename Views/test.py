from flask import request, jsonify, make_response, abort

from __init__ import application, db

import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

consolelog = logging.StreamHandler()
consolelog.setLevel(logging.DEBUG)

logger.addHandler(consolelog)

logger.info("Loading test.py.")

@application.route('/', methods=["GET"])
def index():
    logger.info("Running test.py.")
    return "Hello, World!"
