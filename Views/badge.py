from flask import request, jsonify, make_response, abort, Blueprint

from __init__ import db
# from __init__ import application
from Models.card import Card

import datetime
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

consolelog = logging.StreamHandler()
consolelog.setLevel(logging.DEBUG)

logger.addHandler(consolelog)

logger.info("Loading badge.py.")

badge_view = Blueprint('badge_view', __name__)


@badge_view.route("/test/", methods=["GET"])
@badge_view.route("/api/v0.1/badge/<int:card_id>/", methods=["GET"])
def get_badge_from_id(card_id):
    """Henter badge informasjon fra DB ID felt"""
    logger.debug("Fetching from ID: {}".format(card_id))
    result = Card.query.get(card_id)

    if len(result) == 0:
        logger.debug("No results found.")
        abort(400)

    return jsonify(result)

@badge_view.route("/api/v0.1/badge/<string:serial_number>/", methods=["GET"])
def get_badge_from_serial(serial_number):
    """Henter badge informasjon basert på NFC serienummer"""
    result = Card.query.filter(Card.serial_number == serial_number)

    if len(result) == 0:
        abort (404)

    return jsonify(result)

@badge_view.route("/api/v0.1/badge/wannabe/<string:wannabe_id>/", methods=["GET"])
def get_wannabe_user_badges(wannabe_id):
    """Henter ut en brukers ID kort fra Wannabe ID"""
    result = Card.query.filter(Card.user_id == wannabe_id, Card.badge_type == "wannabe")

    if len(result) == 0:
        abort (404)

    return jsonify(result)


@badge_view.route("/api/v0.1/badge/", methods=["POST"])
def add_card():
    """Legger inn et nytt kort
    
    Feiler dersom requesten ikke inneholder badge type, serienummer og en bruker ID.
    Den returnerer da HTTP 400 (Bad Request)
    Returnerer kortobjektet og HTTP 201 (Created) ved success.
    """

    if not request.json or not check_post_request(request.json):
        abort(400)

    new_card = Card(badge_type = request.json["badge_type"],
                    user_id = request.json["user_id"],
                    serial_number = request.json["serial_number"],
                    creation_date = datetime.datetime.utcnow(),
                    valid_from = datetime.datetime.utcnow(),
                    valid_until = datetime.datetime.max)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(get_badge_from_id(new_card.id)), 201

def check_post_request(json_input):
    required_fields = ("badge_type", "user_id", "serial_number")

    for element in json_input:
        if element not in required_fields:
            return False

    return True