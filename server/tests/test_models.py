from datetime import datetime, timedelta, timezone

from main import delete_old_records, get_changes
from models import Changes, Listings, db


def test_listings_add_record_sets_expiration(app):
    with app.app_context():
        record = Listings.add_record({"Item A": "100 Platinum Points"})
        db.session.commit()

        assert record.items == {"Item A": "100 Platinum Points"}
        assert record.expiration is not None
        assert record.expiration > record.timestamp
        assert Listings.query.count() == 1


def test_changes_add_record(app):
    with app.app_context():
        record = Changes.add_record({"New Items": [{"Item A": "100 Platinum Points"}]})
        db.session.commit()

        assert record.items == {"New Items": [{"Item A": "100 Platinum Points"}]}
        assert Changes.query.count() == 1


def test_get_changes_returns_empty_default(app):
    with app.app_context():
        result = get_changes()
        assert result == {"items": {}, "timestamp": None, "expiration": None}


def test_delete_old_records_removes_expired_entries(app):
    expired = datetime(2020, 1, 1, tzinfo=timezone.utc)
    current = datetime.now(timezone.utc) + timedelta(days=30)

    with app.app_context():
        db.session.add(Listings({"Old Item": "50 Points"}, expiration=expired))
        db.session.add(Listings({"New Item": "100 Points"}, expiration=current))
        db.session.add(
            Changes({"New Items": [{"Item": "x"}]}, expiration=expired)
        )
        db.session.commit()

        deleted = delete_old_records()
        assert deleted == 2
        assert Listings.query.count() == 1
        assert Changes.query.count() == 0
