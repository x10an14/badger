#!flask/bin/python
from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import logging, datetime, json
from collections import OrderedDict, Iterable
from functools import wraps

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

consolelog = logging.StreamHandler()
consolelog.setLevel(logging.DEBUG)


application = Flask(__name__)
application.config.from_object('config')

db = SQLAlchemy(application)

API_PATH = "/api/v0.1/badge/"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_type = db.Column(db.String(64))
    user_id = db.Column(db.Integer, index=True)
    serial_number = db.Column(db.String(14), index=True)
    creation_date = db.Column(db.TimeDelta)
    valid_from = db.Column(db.TimeDelta)
    valid_until = db.Column(db.TimeDelta)
    revoked = db.Column(db.Boolean)

def json_badge(entry):
    json_entry = OrderedDict()

    json_entry['id'] = entry.id
    json_entry['badge_type'] = entry.badge_type
    json_entry['user_id'] = entry.user_id
    json_entry['serial_number'] = entry.serial_number
    json_entry['creation_date'] = entry.creation_date.strftime('%Y-%m-%d-%H-%M-%S')
    json_entry['valid_from'] = entry.valid_from.strftime('%Y-%m-%d-%H-%M-%S')
    json_entry['valid_until'] = entry.valid_until.strftime('%Y-%m-%d-%H-%M-%S')
    json_entry['revoked'] = entry.revoked
    json_entry['_self'] = API_PATH + "id/" + entry.id
    return json_entry

def jsonify_result(entry):
    if isinstance(entry, Iterable):
        return list(map(json_badge, entry))
    else:
        return json_badge(entry)

def json_response(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        response, code = func(*args, **kwargs)
        if isinstance(response, tuple):
            response, code = response, code
        dump = json.dumps(response, indent=2, sort_keys=False)
        return dump, code, {'Content-Type': 'application/json; charset=utf-8'}
    return wrapped

def validate_post_request(json_input):
    required_fields = ("badge_type", "user_id", "serial_number")

    for element in required_fields:
        if element not in json_input:
            return False

    return True

@application.route(API_PATH + "id/<int:card_id>/", methods=["GET"])
@json_response
def get_badge_from_id(card_id):
    """Henter badge informasjon fra DB ID felt"""
    logger.debug("Fetching from ID: {}".format(card_id))
    result = Card.query.get(card_id)

    if not result:
        abort(404)

    return jsonify_result(result), 200


@application.route(API_PATH + "serial/<string:serial_number>/", methods=["GET"])
@json_response
def get_badge_from_serial(serial_number):
    """Henter badge informasjon basert på NFC serienummer"""
    result = Card.query.filter(Card.serial_number == serial_number)

    if not result:
        abort(404)

    return jsonify_result(result), 200


@application.route(API_PATH + "wannabe/<string:wannabe_id>/", methods=["GET"])
@json_response
def get_wannabe_user_badges(wannabe_id):
    """Henter ut en brukers ID kort fra Wannabe ID"""
    result = Card.query.filter(Card.user_id == wannabe_id, Card.badge_type == "wannabe")

    if not result:
        abort(404)

    return jsonify_result(result), 200


@application.route(API_PATH, methods=["POST"])
@application.route(API_PATH + "<int:card_id>/", methods=["POST"])
@json_response
def add_card(card_id = None):
    """Legger inn et nytt kort eller oppdaterer kortet med iden spesifisert i post

    Feiler dersom requesten ikke inneholder badge type, serienummer og en bruker ID.
    Den returnerer da HTTP 400 (Bad Request)
    
    Dersom post request inneholder en ID så vil metoden oppdatere feltene til objektet.
    Returnerer kortobjektet og HTTP 201 (Created) ved opprettelse eller HTTP 200 dersom
    objektet kun endres.
    """

    if not request.json:
        abort(400)

    # Om kortet kun skal opppdateres
    if request.json['id'] or card_id:
        result = Card.query.get(request.json["id"] or card_id)

        #Oppdater feltene som er ment for redigering
        result.revoked = request.json["revoked"]
        result.valid_until = request.json["valid_until"]

        status_code = 200

    # Ellers, lag kort.
    else:
        # Abort om kortet allerede finnes i database
        if Card.query.filter(Card.badge_type == request.json["badge_type"],
                             Card.serial_number == request.json["serial_number"]):
            abort(409)

        # Abort om det mangler informasjon for å lage kortet
        if not validate_post_request(request.json):
            abort(400)

        result = Card(badge_type=request.json["badge_type"],
                    user_id=request.json["user_id"],
                    serial_number=request.json["serial_number"],
                    creation_date=datetime.datetime.utcnow(),
                    valid_from=datetime.datetime.utcnow(),
                    valid_until=0,
                    revoked=False)

        db.session.add(result)
        status_code = 201

    db.session.commit()
    return jsonify_result(result), status_code

@application.route(API_PATH, methods=["DELETE"])
@application.route(API_PATH + "<int:card_id>/", methods=["DELETE"])
@json_response
def revoke_card(card_id = None):
    """Setter revoke til true på et kort basert på IDen til kortet
    """
    result = Card.query.get(request.json["id"] or card_id)

    if not result:
        abort(404)

    result.revoked = True

    db.session.commit()

    return jsonify_result(result), 200

if __name__ == "__main__":
    application.run()
