from flask import Blueprint, jsonify
from main import get_items, get_changes, load_items
from errors import CustomError

check_api = Blueprint("check", __name__)

@check_api.route('/check-fly')
def check_fly():
    try:
        return jsonify("API is running.")
    except Exception as err:
        print(err)
        raise CustomError("Fly is down.")


@check_api.route("/check-scraping")
def check_scraping():
    try:
        raw_item_elements = load_items()
        get_items(raw_item_elements)
        return jsonify("API Scraping is running.")
    except Exception as err:
        print(err)
        raise CustomError("Scraping function failed.")


@check_api.route("/check-db")
def check_fly_db():
    try:
        get_changes()
        return jsonify("API DB is running.")
    except Exception as err:
        print(err)
        raise CustomError("DB function failed.")