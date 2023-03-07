import os

from bs4 import BeautifulSoup
import requests
from deepdiff import DeepDiff
from models import db, Listings, Changes
from datetime import datetime

import dotenv
dotenv.load_dotenv()

url = "https://www.nintendo.com/store/exclusives/rewards/"

# get the text from the provided url
html_text = requests.get(url).text


def check_items():
    """ Function to scrape items listed on MyNintendo Rewards"""

    soup = BeautifulSoup(html_text, 'lxml')
    item_costs = {}
    items = soup.find_all(
        'div', class_='BasicTilestyles__Info-sc-sh8sf3-5 hemcMo')
    for item in items:
        name = item.div.h3.text
        stock = item.find(
            'div', 'ProductTilestyles__DescriptionTag-sc-n2s21r-5 hDroje')  # checks if the item has "Out of Stock" label

        if not stock:
            price = item.find(
                'div', 'ProductTilestyles__PriceWrapper-sc-n2s21r-4 jrjiqe').div.div.span.div.span.text

        cost = f'{stock.text}' if stock else price

        item_costs[name] = cost

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
                changed_items.append({item[6:-2]: diff[difference][item]})
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
    db.session.commit()  # wrap in a try/catch?

    if not changes:
        changes = "No changes."

    return {"changes": changes, "timestamp": new_item.timestamp}


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
    db.session.commit()

    deleted = deleted_listings + deleted_changes
    return deleted
