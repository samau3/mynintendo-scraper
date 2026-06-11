from flask import Blueprint, jsonify

from main import (
    delete_old_records,
    get_item_images,
    get_items,
    get_latest_listings_summary,
    load_items,
    message_discord,
    scrape_mynintendo,
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
    images = get_item_images(raw_item_elements)
    results = scrape_mynintendo(items, images)

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


@main_api.get("/items/latest")
def get_cached_listings():
    """
    Returns the most recent listings from the database without scraping.

    Returns:
        A JSON response with cached listings, or 404 if no records exist.
    """

    summary = get_latest_listings_summary()
    if summary is None:
        return jsonify({"message": "No cached listings found."}), 404

    return jsonify(summary)


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
