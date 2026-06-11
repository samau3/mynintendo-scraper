import logging

from flask import Blueprint, jsonify

from errors import CustomError
from main import get_changes, get_items, load_items

check_api = Blueprint("check", __name__)


@check_api.route("/check-fly")
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
        logging.error("Fly health check failed: %s", err)
        raise CustomError("Fly is down.") from err


@check_api.route("/check-scraping")
def check_scraping():
    """
    Check if the scraping functionality of the API is running.

    Returns:
        A JSON response indicating that the scraping functionality is running.
        Raises a CustomError if the scraping function fails.
    """
    try:
        raw_item_elements, _expansion_meta = load_items()
        get_items(raw_item_elements)
        return jsonify("API Scraping is running.")
    except Exception as err:
        logging.error("Scraping health check failed: %s", err)
        raise CustomError("Scraping function failed.") from err


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
        logging.error("Database health check failed: %s", err)
        raise CustomError("DB function failed.") from err
