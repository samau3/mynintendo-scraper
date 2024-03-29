import os

from flask import Flask, jsonify
from flask_cors import CORS

from models import db, connect_db
from main import scrape_mynintendo, message_discord, delete_old_records, check_items, get_changes
from errors import CustomError, CSSTagSelectorError

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# need below line to keep db connection active
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


@app.get('/')
def show_home_page():
    items = check_items()
    scrape_results = scrape_mynintendo()
    last_change = get_changes()

    if scrape_results["items"] != "No changes.":
        message_discord(scrape_results["items"])

    display = {
        "current_listings": items,
        "recent_change": scrape_results,
        "last_change": last_change
    }
    return jsonify(display)


@app.get('/api/scrape')
def call_scrape_fn():
    results = scrape_mynintendo()

    if results["items"] != "No changes.":
        message_discord(results["items"])

    return results


@app.get('/api/delete')
def delete_records():

    results = delete_old_records()
    return f"Deleted {results} entries."


@app.get("/api/get-items")
def call_check_items():
    items = check_items()

    return jsonify(items)

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
    else:
        response = {
            "message": "An error occurred.",
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
