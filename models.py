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
        item = Listings(
            items=items,
            change=has_changed
        )
        db.session.add(item)
        return item

    @classmethod
    def update_database(items):
        """Store the scrapped items into database"""
        items_entry = Listings(items=items)

        db.session.add(items_entry)
        return items_entry


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
