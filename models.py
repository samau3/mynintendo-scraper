from datetime import datetime
import sqlalchemy

db = sqlalchemy()


class Listings(db.Model):

    __tablename__ = "item_listings"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items = db.Column(db.JSONB, nullable=False)
    change = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def update_database(items):
        """Store the scrapped items into database"""
        items_entry = Listings(items=items)

        db.session.add(items_entry)
        return items_entry

# change to use Flask, and utilize cron-job.org to hit an endpoint
