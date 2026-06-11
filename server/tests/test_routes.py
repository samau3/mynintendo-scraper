from unittest.mock import patch

from errors import CSSTagSelectorError, IncompleteScrapeError
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
        Listings.add_record(
            {"Item A": "100 Platinum Points"},
            images={"Item A": "https://assets.nintendo.com/item-a.png"},
        )
        db.session.commit()

    response = client.get("/api/items/latest")
    assert response.status_code == 200
    data = response.get_json()
    assert data["current_listings"] == {"Item A": "100 Platinum Points"}
    assert data["images"] == {"Item A": "https://assets.nintendo.com/item-a.png"}
    assert data["recent_change"]["items"] == "No changes."


@patch("routes.main_api.fetch_scraped_data")
def test_get_items_endpoint(mock_fetch_scraped_data, client):
    mock_fetch_scraped_data.return_value = (
        {"Item A": "100 Platinum Points"},
        {"Item A": "https://assets.nintendo.com/item-a.png"},
        {"expanded": True, "count_before": 1, "count_after": 1},
    )

    response = client.get("/api/get-items")
    assert response.status_code == 200
    assert response.get_json() == {"Item A": "100 Platinum Points"}


@patch("main.load_items")
def test_root_returns_503_on_css_selector_error(mock_load_items, client):
    mock_load_items.side_effect = CSSTagSelectorError("The CSS tag for stock has changed.")

    response = client.get("/")
    assert response.status_code == 503
    assert "CSS tag for stock" in response.get_json()["message"]


@patch("main.get_item_images")
@patch("main.get_items")
@patch("main.load_items")
def test_root_returns_503_on_incomplete_scrape(
    mock_load_items, mock_get_items, mock_get_item_images, app, client
):
    full_listings = {f"Item {i}": f"{i}00 Platinum Points" for i in range(59)}
    partial_listings = {f"Item {i}": f"{i}00 Platinum Points" for i in range(20)}
    failed_meta = {
        "expanded": False,
        "button_found": True,
        "count_before": 20,
        "count_after": 20,
    }

    with app.app_context():
        Listings.add_record(full_listings)
        db.session.commit()
        initial_count = Listings.query.count()

    mock_load_items.return_value = ([], failed_meta)
    mock_get_items.return_value = partial_listings
    mock_get_item_images.return_value = {}

    response = client.get("/")

    assert response.status_code == 503
    assert "full rewards list" in response.get_json()["message"]

    with app.app_context():
        assert Listings.query.count() == initial_count


@patch("app.run_scrape")
def test_root_returns_503_on_incomplete_scrape_error(mock_run_scrape, client):
    mock_run_scrape.side_effect = IncompleteScrapeError(
        "Could not load full rewards list after 3 attempts."
    )

    response = client.get("/")

    assert response.status_code == 503
    assert "full rewards list" in response.get_json()["message"]
