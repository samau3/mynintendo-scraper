import os

from flask import Flask, jsonify
from flask_cors import CORS
from selenium.common.exceptions import TimeoutException

from models import db, connect_db
from main import (
    scrape_mynintendo,
    message_discord,
    get_items,
    get_changes,
    load_items,
    get_item_images,
)
from errors import CustomError, CSSTagSelectorError
from routes.check_api import check_api
from routes.main_api import main_api

import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

app.json.sort_keys = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"].replace(
    "postgres://", "postgresql://"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
# need below line to keep db connection active
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

app.register_blueprint(main_api, url_prefix="/api")
app.register_blueprint(check_api, url_prefix="/api")


@app.get("/")
def display_scrape_summary():
    """
    Displays a summary of the scrape, including current listings, images, recent changes, and the last change.
    If changes are found during scraping, notifies via Discord.

    Returns:
        A JSON response containing:
        - current_listings: A list of current items.
        - images: A list of item images.
        - recent_change: The results of the most recent scrape.
        - last_change: Information about the last change detected.
    """

    raw_item_elements = load_items()
    items = get_items(raw_item_elements)
    images = get_item_images(raw_item_elements)
    scrape_results = scrape_mynintendo(items)
    last_change = get_changes()

    if scrape_results["items"] != "No changes.":
        message_discord(scrape_results["items"])

    display = {
        "current_listings": items,
        "images": images,
        "recent_change": scrape_results,
        "last_change": last_change,
    }
    return jsonify(display)


@app.errorhandler(404)
def handle_not_found_error(error):
    response = {"message": "Resource not found."}
    return jsonify(response), 404


@app.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, CustomError):
        response = {"message": str(error)}
    elif isinstance(error, CSSTagSelectorError):
        response = {"message": str(error)}
        return jsonify(response), 503
    elif isinstance(error, TimeoutException):
        response = {"message": str(error)[9:-1]}
    else:
        response = {
            "message": f"{error}",
        }

    return jsonify(response), 500


@app.after_request
def add_header(response):
    """Add non-caching headers on every request."""

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    return response


with app.app_context():
    db.create_all()
