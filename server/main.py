import os

from bs4 import BeautifulSoup
import requests
from deepdiff import DeepDiff
from models import db, Listings, Changes
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from errors import DatabaseError, CSSTagSelectorError
import re

import dotenv
dotenv.load_dotenv()

url = "https://www.nintendo.com/store/exclusives/rewards/"


def check_items():
    """ Function to scrape items listed on MyNintendo Rewards"""

    headers = {'Cache-Control': 'no-cache, must-revalidate'}

    # get the text from the provided url
    html_text = requests.get(url, headers=headers).text

    soup = BeautifulSoup(html_text, 'lxml')
    item_costs = {}

    # Find items, based on the CSS tag BasicTilestyles__Info-sc
    items = soup.find_all(
        'div', class_=re.compile('BasicTilestyles__Info-sc'))

    if not items:
        raise CSSTagSelectorError("The CSS tag for items have changed.")

    for item in items:
        # the website changes what header is used (e.g. h2, h3) so need a non hard coded way to target it via find_next()
        header = item.div.find_next()
        name = header.text.strip() if header else "Unknown Name"
        stock = item.find(
            'div', class_=re.compile('ProductTilestyles__DescriptionTag-sc'))  # checks if the item has "Out of Stock" label

        if stock and stock.text == "Exclusive":
            price_element = item.find('div', class_=re.compile(
                'ProductTilestyles__PriceWrapper-sc'))
            price_span = price_element.find_all(
                'span')[2] if price_element else None
            price = price_span.text if price_span else "Price Not Found"

        elif stock and stock.text != "Exclusive":
            price = stock.text
        else:
            price = "Price Not Found"
        item_costs[name] = price

    return item_costs


def check_for_changes(last_stored_items, scraped_items):
    """ Function to compare two dictionaries, 
        returning the resulting differences"""

    diff = DeepDiff(last_stored_items, scraped_items)

    if (len(diff) == 0):
        return None

    changes = {}
    for difference in diff:
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
                removed_items.append(
                    {item[6:-2]: last_stored_items[item[6:-2]]})
            changes["Removed Items"] = removed_items
        # if difference is changed
        if difference == "values_changed":
            changed_items = []
            for item in diff[difference]:
                changed_items.append(
                    {item[6:-2]: f'{diff[difference][item]["new_value"]} (Old value: {diff[difference][item]["old_value"]})'})
            changes["Changed Items"] = changed_items

    return changes


def get_changes():
    """ Function that returns the changes from database """

    last_change_row_object = Changes.query.order_by(Changes.id.desc()).first()
    last_change = {}
    for column in last_change_row_object.__table__.columns:
        if column.name != "id":
            last_change[column.name] = getattr(
                last_change_row_object, column.name)

    return last_change


def scrape_mynintendo():
    """ Function that calls scraping function and updates database if changes were found"""
    results = check_items()
    last_record = Listings.query.order_by(Listings.id.desc()).first()
    last_items = last_record.items if last_record is not None else {}

    changes = check_for_changes(last_items, results)

    if changes:
        Changes.add_record(changes)
    new_item = Listings.add_record(results)

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        raise DatabaseError(
            "Database error occurred while updating database for changes.")

    if not changes:
        changes = "No changes."

    return {"items": changes, "timestamp": new_item.timestamp}


def message_discord(changes):
    """ Function that calls Discord webhook to message user of changes on MyNintendo Rewards"""
    discord_url = f"https://discord.com/api/webhooks/{os.environ['WEBHOOK_ID']}/{os.environ['WEBHOOK_TOKEN']}"
    data = {}

    output_message = f"""<@{os.environ['DISCORD_USER_ID']}>\nCheck the listings: {url}\n"""
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

    data['content'] = output_message
    data['embeds'] = output_embed

    result = requests.post(discord_url, json=data, headers={
                           "Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def delete_old_records():
    """ Function that deletes expired database records """
    expired_listings = Listings.query.filter(
        Listings.expiration <= datetime.utcnow())
    expired_changes = Changes.query.filter(
        Changes.expiration <= datetime.utcnow())
    deleted_listings = expired_listings.delete(synchronize_session=False)
    deleted_changes = expired_changes.delete(synchronize_session=False)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        raise DatabaseError(
            "Database error occurred while trying to delete records.")

    deleted = deleted_listings + deleted_changes
    return deleted
