import logging
import os
import re
from datetime import datetime, timezone

import dotenv
import requests
from bs4 import BeautifulSoup
from deepdiff import DeepDiff
from playwright.sync_api import sync_playwright
from sqlalchemy.exc import SQLAlchemyError

from errors import (
    CSSTagSelectorError,
    CustomError,
    DatabaseError,
    IncompleteScrapeError,
)
from helpers.expand_rewards_list import expand_rewards_list
from helpers.find_items import PLATINUM_POINTS_TEST_ID, find_items
from helpers.remove_trademark_false_positives import remove_trademark_false_positives
from models import Changes, Listings, db

dotenv.load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

MYNINTENDO_URL = "https://www.nintendo.com/store/exclusives/rewards/"
PRODUCT_READY_SELECTOR = f'[data-testid="{PLATINUM_POINTS_TEST_ID}"]'
MAX_SCRAPE_ATTEMPTS = 3


def derive_preview_item_count(expansion_meta):
    """Return the collapsed preview count when expansion succeeded."""
    if not expansion_meta:
        return None

    if not expansion_meta.get("button_found", False):
        return None

    count_before = expansion_meta.get("count_before")
    count_after = expansion_meta.get("count_after")
    if (
        count_before is not None
        and count_after is not None
        and count_after > count_before
    ):
        return count_before

    return None


def resolve_preview_item_count(expansion_meta, last_record):
    """Keep the stored preview count unless this scrape observed a new expansion."""
    new_preview = derive_preview_item_count(expansion_meta)
    if new_preview is not None:
        return new_preview
    if last_record is not None:
        return last_record.preview_item_count
    return None


def is_incomplete_scrape(last_items, scraped_items, expansion_meta, preview_item_count):
    """Return True when a scrape likely missed hidden items behind expansion."""
    if not last_items:
        return False

    scraped_keys = set(scraped_items)
    last_keys = set(last_items)

    if len(scraped_items) >= len(last_items):
        return False
    if not scraped_keys < last_keys:
        return False

    count_before = expansion_meta.get("count_before", len(scraped_items))
    count_after = expansion_meta.get("count_after", len(scraped_items))
    button_found = expansion_meta.get("button_found", False)
    expansion_failed = not expansion_meta.get("expanded", False)

    if expansion_failed:
        return True
    if button_found and count_after <= count_before:
        return True
    if preview_item_count is not None and count_after == preview_item_count:
        return True

    return False


def load_items():
    """Load the rewards page and return product elements plus expansion metadata."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--window-size=1920,1080',
            '--disable-features=VizDisplayCompositor',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',  # Skip loading images for speed
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
        ])
        page = browser.new_page()
        try:
            page.set_default_timeout(30000)  # 30 seconds
            page.goto(MYNINTENDO_URL, wait_until='networkidle')
            page.wait_for_selector(PRODUCT_READY_SELECTOR, timeout=20000)
            expansion_meta = expand_rewards_list(page, PRODUCT_READY_SELECTOR)
            soup = BeautifulSoup(page.content(), "lxml")
            item_elements = find_items(soup)
            return item_elements, expansion_meta
        finally:
            browser.close()


def fetch_scraped_data():
    """Scrape items with retries when expansion appears incomplete."""
    last_record = Listings.query.order_by(Listings.id.desc()).first()
    last_items = last_record.items if last_record is not None else {}
    preview_item_count = (
        last_record.preview_item_count if last_record is not None else None
    )

    raw_elements = None
    items = None
    images = None
    expansion_meta = None

    for attempt in range(MAX_SCRAPE_ATTEMPTS):
        raw_elements, expansion_meta = load_items()
        items = get_items(raw_elements)
        if not is_incomplete_scrape(
            last_items, items, expansion_meta, preview_item_count
        ):
            images = get_item_images(raw_elements)
            break
        logging.warning(
            "Incomplete scrape attempt %s/%s (count_after=%s, last_count=%s)",
            attempt + 1,
            MAX_SCRAPE_ATTEMPTS,
            expansion_meta.get("count_after"),
            len(last_items),
        )
    else:
        raise IncompleteScrapeError(
            f"Could not load full rewards list after {MAX_SCRAPE_ATTEMPTS} attempts."
        )

    return items, images, expansion_meta


def get_items(items):
    """Function to scrape items listed on MyNintendo Rewards"""

    item_data = {}

    for item in items:
        name = item.get("aria-label", "Unknown Name").strip()

        # targets the element that displays "Exclusive" or "Sold out" label to help determine stock status
        # Use of __DescriptionTag-sc is to reduce the amount of hard coding for the CSS class selection due to website changing what they use
        stock = item.find("div", class_=re.compile("Hc9FH"))

        if not stock:
            raise CSSTagSelectorError("The CSS tag for stock has changed.")

        if stock and stock.text == "Exclusive":
            price_element = item.find("div", class_=re.compile("Zc8hG"))
            price = price_element.get_text() if price_element else "Price Not Found"
        elif stock and stock.text != "Exclusive":
            price = stock.text
        else:
            price = "Price Not Found"
        item_data[name] = price

    return item_data


def get_item_images(items):
    """Function to scrape items listed on MyNintendo Rewards"""
    item_images = {}

    for item in items:

        name = item.get("aria-label", "Unknown Name").strip()

        # targets the element that displays "Exclusive" or "Sold out" label to help determine stock status
        # Use of __DescriptionTag-sc is to reduce the amount of hard coding for the CSS class selection due to website changing what they use
        image = item.find("img", class_=re.compile("EgihB"))

        if not image:
            raise CSSTagSelectorError("The CSS tag for images has changed.")

        image_url = image.get("src", "https://placehold.co/600x400")

        item_images[name] = image_url

    return item_images


def check_for_changes(last_stored_items, scraped_items):
    """Function to compare two dictionaries,
    returning the resulting differences"""

    diff = DeepDiff(last_stored_items, scraped_items)

    if len(diff) == 0:
        return None

    cleaned_diff = remove_trademark_false_positives(diff)

    if len(cleaned_diff) == 0:
        return None

    changes = {}
    for difference in cleaned_diff:

        # if difference is added
        if difference == "dictionary_item_added":
            new_items = []
            for item in diff[difference]:
                new_items.append({item[6:-2]: scraped_items[item[6:-2]]})
            changes["New Items"] = new_items

        # if difference is removed
        if difference == "dictionary_item_removed":
            removed_items = []
            for item in diff[difference]:
                removed_items.append({item[6:-2]: last_stored_items[item[6:-2]]})
            changes["Removed Items"] = removed_items
        # if difference is changed
        if difference == "values_changed":
            changed_items = []
            for item in diff[difference]:
                changed_items.append(
                    {
                        item[
                            6:-2
                        ]: f'{diff[difference][item]["new_value"]} (Old value: {diff[difference][item]["old_value"]})'
                    }
                )
            changes["Changed Items"] = changed_items

    return changes


def get_changes():
    """Function that returns the changes from database"""

    last_change_row_object = Changes.query.order_by(Changes.id.desc()).first()
    if last_change_row_object is None:
        return {"items": {}, "timestamp": None, "expiration": None}

    last_change = {}
    for column in last_change_row_object.__table__.columns:
        if column.name != "id":
            last_change[column.name] = getattr(last_change_row_object, column.name)

    return last_change


def get_latest_listings_summary():
    """Return the most recent cached listings from the database without scraping."""

    last_record = Listings.query.order_by(Listings.id.desc()).first()
    if last_record is None:
        return None

    return {
        "current_listings": last_record.items,
        "images": last_record.images or {},
        "recent_change": {
            "items": "No changes.",
            "timestamp": last_record.timestamp,
        },
        "last_change": get_changes(),
    }


def run_scrape():
    """Scrape with retries, update the database, and return scrape results."""
    items, images, expansion_meta = fetch_scraped_data()
    scrape_results = scrape_mynintendo(items, images, expansion_meta=expansion_meta)
    return items, images, scrape_results


def scrape_mynintendo(current_items, images=None, expansion_meta=None):
    """Function that calls scraping function and updates database if changes were found"""
    last_record = Listings.query.order_by(Listings.id.desc()).first()
    last_items = last_record.items if last_record is not None else {}
    preview_item_count = resolve_preview_item_count(expansion_meta, last_record)

    changes = check_for_changes(last_items, current_items)

    if changes:
        Changes.add_record(changes)
    new_item = Listings.add_record(
        current_items,
        images=images or {},
        preview_item_count=preview_item_count,
    )

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Database error while updating changes: %s", e)
        raise DatabaseError(
            "Database error occurred while updating database for changes."
        ) from e
    except Exception as e:
        logging.error("Unexpected error while updating changes: %s", e)
        raise CustomError(
            "Error occurred while updating database for changes.", e
        ) from e

    if not changes:
        changes = "No changes."

    return {"items": changes, "timestamp": new_item.timestamp}


def message_discord(changes):
    """Function that calls Discord webhook to message user of changes on MyNintendo Rewards"""
    discord_url = f"https://discord.com/api/webhooks/{os.environ['WEBHOOK_ID']}/{os.environ['WEBHOOK_TOKEN']}"
    data = {}

    output_message = f"""<@{os.environ['DISCORD_USER_ID']}>\nCheck the listings: {MYNINTENDO_URL}\n"""
    output_embed = []
    for change in changes:
        embed_obj = {}
        embed_obj["title"] = change
        description = ""
        for item in changes[change]:
            cleaned_item = (f"{item}")[1:-1]
            description = f"{description}{cleaned_item}\n"
        # message = f"{message}{message}\n"
        embed_obj["description"] = description
        output_embed.append(embed_obj)

    data["content"] = output_message
    data["embeds"] = output_embed

    result = requests.post(
        discord_url, json=data, headers={"Content-Type": "application/json"}
    )

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error("Discord webhook delivery failed: %s", err)
    else:
        logging.info(
            "Discord payload delivered successfully, code %s.", result.status_code
        )


def delete_old_records():
    """Function that deletes expired database records"""
    expired_listings = Listings.query.filter(Listings.expiration <= datetime.now(timezone.utc))
    expired_changes = Changes.query.filter(Changes.expiration <= datetime.now(timezone.utc))
    deleted_listings = expired_listings.delete(synchronize_session=False)
    deleted_changes = expired_changes.delete(synchronize_session=False)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error("Database error while deleting records: %s", e)
        raise DatabaseError("Database error occurred while trying to delete records.") from e

    deleted = deleted_listings + deleted_changes
    return deleted
