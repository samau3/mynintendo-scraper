from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

from helpers.calculate_expiration_date import calculate_expiration_date

db = SQLAlchemy()


class Listings(db.Model):

    __tablename__ = "item_listings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    expiration = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)
    images = db.Column(db.JSON, nullable=False, default=dict)
    preview_item_count = db.Column(db.Integer, nullable=True)

    def __init__(self, items, images=None, preview_item_count=None, expiration=None):
        self.items = items
        self.images = images if images is not None else {}
        self.preview_item_count = preview_item_count
        self.expiration = expiration if expiration else calculate_expiration_date(7)

    @classmethod
    def add_record(self, items, images=None, preview_item_count=None):
        """Store the scrapped items into database"""
        item = Listings(
            items=items,
            images=images,
            preview_item_count=preview_item_count,
        )
        db.session.add(item)
        return item


class Changes(db.Model):

    __tablename__ = "changes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    expiration = db.Column(db.DateTime, nullable=False)
    items = db.Column(db.JSON, nullable=False)

    def __init__(self, items, expiration=None):
        self.items = items
        self.expiration = expiration if expiration else calculate_expiration_date(365)

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


def ensure_schema():
    """Create tables and apply lightweight schema upgrades for existing databases."""
    db.create_all()

    inspector = inspect(db.engine)
    if not inspector.has_table("item_listings"):
        return

    columns = {column["name"] for column in inspector.get_columns("item_listings")}
    if "images" not in columns:
        with db.engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE item_listings "
                    "ADD COLUMN images JSON NOT NULL DEFAULT '{}'"
                )
            )
    if "preview_item_count" not in columns:
        with db.engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE item_listings "
                    "ADD COLUMN preview_item_count INTEGER"
                )
            )
