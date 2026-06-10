from unittest.mock import patch

from errors import CSSTagSelectorError
from models import Listings, db


def test_check_fly_returns_ok(client):
    response = client.get("/api/check-fly")
    assert response.status_code == 200
    assert response.get_json() == "API is running."


def test_check_db_returns_ok_with_empty_changes(client):
    response = client.get("/api/check-db")
    assert response.status_code == 200
    assert response.get_json() == "API DB is running."


def test_get_items_latest_returns_404_when_empty(client):
    response = client.get("/api/items/latest")
    assert response.status_code == 404
    assert response.get_json()["message"] == "No cached listings found."


def test_get_items_latest_returns_cached_listings(app, client):
    with app.app_context():
        Listings.add_record({"Item A": "100 Platinum Points"})
        db.session.commit()

    response = client.get("/api/items/latest")
    assert response.status_code == 200
    data = response.get_json()
    assert data["current_listings"] == {"Item A": "100 Platinum Points"}
    assert data["recent_change"]["items"] == "No changes."


@patch("routes.main_api.load_items")
@patch("routes.main_api.get_items")
def test_get_items_endpoint(mock_get_items, mock_load_items, client):
    mock_load_items.return_value = ["mock-element"]
    mock_get_items.return_value = {"Item A": "100 Platinum Points"}

    response = client.get("/api/get-items")
    assert response.status_code == 200
    assert response.get_json() == {"Item A": "100 Platinum Points"}


@patch("app.load_items")
def test_root_returns_503_on_css_selector_error(mock_load_items, client):
    mock_load_items.side_effect = CSSTagSelectorError("The CSS tag for stock has changed.")

    response = client.get("/")
    assert response.status_code == 503
    assert "CSS tag for stock" in response.get_json()["message"]
