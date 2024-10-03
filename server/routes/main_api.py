from flask import Blueprint, jsonify
from main import (
    scrape_mynintendo,
    message_discord,
    delete_old_records,
    get_items,
    load_items,
)

main_api = Blueprint("main", __name__)


@main_api.get("/scrape")
def call_scrape_fn():
    """
    Scrapes items and checks for changes. If changes are found, notifies via Discord.

    Returns:
        A JSON response containing the timestamp of the scrape.
    """

    raw_item_elements = load_items()
    items = get_items(raw_item_elements)
    results = scrape_mynintendo(items)

    if results["items"] != "No changes.":
        message_discord(results["items"])

    return jsonify(results["timestamp"])


@main_api.get("/delete")
def delete_records():
    """
    Deletes old records from the database.

    Returns:
        A string indicating the number of deleted entries.
    """

    results = delete_old_records()
    return f"Deleted {results} entries."


@main_api.get("/get-items")
def call_get_items():
    """
    Retrieves and processes items.

    Returns:
        A JSON response containing the processed items.
    """

    raw_item_elements = load_items()
    items = get_items(raw_item_elements)

    return jsonify(items)
