from datetime import datetime, timedelta, timezone

from sqlalchemy import inspect, text

from main import delete_old_records, get_changes
from models import Changes, Listings, db, ensure_schema


def test_ensure_schema_adds_images_column_to_legacy_table(app):
    with app.app_context():
        db.create_all()
        with db.engine.begin() as connection:
            connection.execute(text("DROP TABLE item_listings"))
            connection.execute(
                text(
                    "CREATE TABLE item_listings ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "timestamp DATETIME NOT NULL, "
                    "expiration DATETIME NOT NULL, "
                    "items JSON NOT NULL"
                    ")"
                )
            )

        ensure_schema()

        columns = {
            column["name"] for column in inspect(db.engine).get_columns("item_listings")
        }
        assert "images" in columns

        record = Listings.add_record(
            {"Item A": "100 Platinum Points"},
            images={"Item A": "https://assets.nintendo.com/item-a.png"},
        )
        db.session.commit()
        assert record.images == {"Item A": "https://assets.nintendo.com/item-a.png"}


def test_listings_add_record_sets_expiration(app):
    with app.app_context():
        record = Listings.add_record({"Item A": "100 Platinum Points"})
        db.session.commit()

        assert record.items == {"Item A": "100 Platinum Points"}
        assert record.images == {}
        assert record.expiration is not None
        assert record.expiration > record.timestamp
        assert Listings.query.count() == 1


def test_listings_add_record_stores_preview_item_count(app):
    with app.app_context():
        record = Listings.add_record(
            {"Item A": "100 Platinum Points"},
            preview_item_count=20,
        )
        db.session.commit()

        assert record.preview_item_count == 20


def test_ensure_schema_adds_preview_item_count_column_to_legacy_table(app):
    with app.app_context():
        db.create_all()
        with db.engine.begin() as connection:
            connection.execute(text("DROP TABLE item_listings"))
            connection.execute(
                text(
                    "CREATE TABLE item_listings ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "timestamp DATETIME NOT NULL, "
                    "expiration DATETIME NOT NULL, "
                    "items JSON NOT NULL, "
                    "images JSON NOT NULL DEFAULT '{}'"
                    ")"
                )
            )

        ensure_schema()

        columns = {
            column["name"] for column in inspect(db.engine).get_columns("item_listings")
        }
        assert "preview_item_count" in columns


def test_listings_add_record_stores_images(app):
    with app.app_context():
        images = {"Item A": "https://assets.nintendo.com/item-a.png"}
        record = Listings.add_record(
            {"Item A": "100 Platinum Points"},
            images=images,
        )
        db.session.commit()

        assert record.images == images


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
        db.session.add(Changes({"New Items": [{"Item": "x"}]}, expiration=expired))
        db.session.commit()

        deleted = delete_old_records()
        assert deleted == 2
        assert Listings.query.count() == 1
        assert Changes.query.count() == 0
