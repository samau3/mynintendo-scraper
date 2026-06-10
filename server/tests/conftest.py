import os

import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("WEBHOOK_ID", "test-webhook-id")
os.environ.setdefault("WEBHOOK_TOKEN", "test-webhook-token")
os.environ.setdefault("DISCORD_USER_ID", "123456789")


@pytest.fixture
def app():
    from app import app as flask_app
    from models import db

    flask_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
