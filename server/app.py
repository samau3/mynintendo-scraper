import os

from flask import Flask, jsonify
from flask_cors import CORS

from models import db, connect_db
from main import scrape_mynintendo, message_discord, delete_old_records, get_items, get_changes, load_items, get_item_images
from errors import CustomError, CSSTagSelectorError
from routes.check_api import check_api

import dotenv
dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

app.json.sort_keys = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# need below line to keep db connection active
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.register_blueprint(check_api, url_prefix="/api")

@app.get('/')
def show_home_page():
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
        "last_change": last_change
    }
    return jsonify(display)


@app.get('/api/scrape')
def call_scrape_fn():
    raw_item_elements = load_items()
    items = get_items(raw_item_elements)
    results = scrape_mynintendo(items)

    if results["items"] != "No changes.":
        message_discord(results["items"])

    return jsonify(results["timestamp"])


@app.get('/api/delete')
def delete_records():

    results = delete_old_records()
    return f"Deleted {results} entries."


@app.get("/api/get-items")
def call_get_items():
    raw_item_elements = load_items()
    items = get_items(raw_item_elements)

    return jsonify(items)


# @app.get("/api/check-fly")
# def check_fly():
#     try:
#         return jsonify("API is running.")
#     except Exception as err:
#         print(err)
#         raise CustomError("Fly is down.")


# @app.get("/api/check-scraping")
# def check_scraping():
#     try:
#         raw_item_elements = load_items()
#         get_items(raw_item_elements)
#         return jsonify("API Scraping is running.")
#     except Exception as err:
#         print(err)
#         raise CustomError("Scraping function failed.")


# @app.get("/api/check-db")
# def check_fly_db():
#     try:
#         get_changes()
#         return jsonify("API DB is running.")
#     except Exception as err:
#         print(err)
#         raise CustomError("DB function failed.")


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
