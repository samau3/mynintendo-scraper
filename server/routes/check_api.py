from flask import Blueprint, jsonify
from main import get_items, get_changes, load_items
from errors import CustomError

check_api = Blueprint("check", __name__)


@check_api.route('/check-fly')
def check_fly():
    """
    Check if the 'fly' component of the API is running.

    Returns:
        A JSON response indicating that the 'fly' component is running.
        Raises a CustomError if there is an issue with the 'fly' component.
    """
    try:
        return jsonify("API is running.")
    except Exception as err:
        print(err)
        raise CustomError("Fly is down.")


@check_api.route("/check-scraping")
def check_scraping():
    """
    Check if the scraping functionality of the API is running.

    Returns:
        A JSON response indicating that the scraping functionality is running.
        Raises a CustomError if the scraping function fails.
    """
    try:
        raw_item_elements = load_items()
        get_items(raw_item_elements)
        return jsonify("API Scraping is running.")
    except Exception as err:
        print(err)
        raise CustomError("Scraping function failed.")


@check_api.route("/check-db")
def check_fly_db():
    """
    Check if the database functionality of the API is running.

    Returns:
        A JSON response indicating that the database functionality is running.
        Raises a CustomError if the database function fails.
    """
    try:
        get_changes()
        return jsonify("API DB is running.")
    except Exception as err:
        print(err)
        raise CustomError("DB function failed.")
