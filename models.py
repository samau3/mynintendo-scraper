from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Listings(db.Model):

    __tablename__ = "item_listings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.Column(db.JSON, nullable=False)
    change = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def add_record(self, items, has_changed):
        """Store the scrapped items into database"""
        item = Listings(
            items=items,
            change=has_changed
        )
        db.session.add(item)
        return item


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)