from __init__ import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_type = db.Column(db.String(64))
    user_id = db.Column(db.Integer, index=True)
    serial_number = db.Column(db.String(14), index=True)
    creation_date = db.Column(db.DateTime)
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)