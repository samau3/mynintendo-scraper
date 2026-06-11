from flask import Blueprint, jsonify

from main import (
    delete_old_records,
    fetch_scraped_data,
    get_latest_listings_summary,
    message_discord,
    run_scrape,
)

main_api = Blueprint("main", __name__)


@main_api.get("/scrape")
def call_scrape_fn():
    """
    Scrapes items and checks for changes. If changes are found, notifies via Discord.

    Returns:
        A JSON response containing the timestamp of the scrape.
    """

    _items, _images, results = run_scrape()

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

    items, _images, _expansion_meta = fetch_scraped_data()

    return jsonify(items)
