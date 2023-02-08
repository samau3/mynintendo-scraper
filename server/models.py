from datetime import datetime
from helpers.calculate_expiration_date import calculate_expiration_date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Listings(db.Model):

    __tablename__ = "item_listings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)

    def __init__(self, items, timestamp=None, expiration=None):
        self.timestamp = timestamp
        self.expiration = expiration if expiration else calculate_expiration_date(
            7)
        self.items = items

    @classmethod
    def add_record(self, items):
        """Store the scrapped items into database"""
        item = Listings(
            items=items,
        )
        db.session.add(item)
        return item


class Changes(db.Model):

    __tablename__ = "changes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiration = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)

    def __init__(self, items, timestamp=None, expiration=None):
        self.timestamp = timestamp
        self.expiration = expiration if expiration else calculate_expiration_date(
            7)
        self.items = items

    @classmethod
    def add_record(self, items):
        """Store the scrapped items into database"""
        item = Changes(
            items=items,
        )
        db.session.add(item)
        return item


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
