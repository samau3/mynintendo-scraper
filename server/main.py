import os
import logging
import time

from bs4 import BeautifulSoup

import requests
from deepdiff import DeepDiff
from models import db, Listings, Changes
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from errors import DatabaseError, CSSTagSelectorError, CustomError
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from helpers.remove_trademark_false_positives import remove_trademark_false_positives
from helpers.find_items import find_items

import dotenv
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


MYNINTENDO_URL = "https://www.nintendo.com/store/exclusives/rewards/"
ITEMS_CSS_TAG = "VoZI3"

PARENT_CONTAINER_OF_PRODUCTS_CSS_TAG = "sc-1dskkk7-1"
EXPECTED_CHILD_DIV_COUNT = 2

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def load_items():
    """ Function to load a webpage and wait for a specific tag to load"""
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get(MYNINTENDO_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, ITEMS_CSS_TAG)),
        message="Scraping timedout, CSS tags need to be updated."
    )

    # Add a check for a see more button to load more items

    parent_div = driver.find_element(
        By.CSS_SELECTOR, f'div.sc-1dskkk7-1')

    child_divs = parent_div.find_elements(By.CSS_SELECTOR, ':scope > div')
    logging.info(f"Found {len(child_divs)} child divs.")

    # Check if the number of child divs is greater than usual (e.g., expecting more than a certain number)
    if len(child_divs) > EXPECTED_CHILD_DIV_COUNT:
        # Break the loop if the number of child divs is not greater than expected

        try:
            logging.info("Found more items to load.")
            load_more_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'div.sc-1egu3fv-1.cCkfGx button.MFcmt._3LMnG.xN-5A')),
                message="Scraping timedout, CSS tag for 'See All' button needs to be updated."
            )
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", load_more_button)

            if load_more_button.is_displayed():
                logging.info("'See All' button is visible.")
            else:
                logging.error("'See All' button is not visible.")

            logging.info(load_more_button.get_attribute("outerHTML"))
            driver.execute_script("arguments[0].click();", load_more_button)
            logging.info("'See All' button clicked.")
            # Add a delay to give enough time for the items to load
            time.sleep(3)
            # Wait for additional items to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, ITEMS_CSS_TAG)),
                message="Scraping timedout, CSS tags need to be updated."
            )

            new_child_divs = parent_div.find_elements(
                By.CSS_SELECTOR, ':scope > div')
            logging.info(
                f"Number of child divs after clicking 'See All': {len(new_child_divs)}")

        except TimeoutException as e:
            logging.error(e.msg)

    soup = BeautifulSoup(parent_div.get_attribute("outerHTML"), 'lxml')

    item_elements = find_items(soup, ITEMS_CSS_TAG)
    return item_elements


def get_items(items):
    """ Function to scrape items listed on MyNintendo Rewards"""

    item_data = {}

    for item in items:
        name = item.get('aria-label', 'Unknown Name').strip()

        # targets the element that displays "Exclusive" or "Sold out" label to help determine stock status
        # Use of __DescriptionTag-sc is to reduce the amount of hard coding for the CSS class selection due to website changing what they use
        stock = item.find(
            'div', class_=re.compile('Hc9FH'))

        if not stock:
            raise CSSTagSelectorError("The CSS tag for stock has changed.")

        if stock and stock.text == "Exclusive":
            price_element = item.find('div', class_=re.compile(
                'Zc8hG'))
            price = price_element.get_text() if price_element else "Price Not Found"
        elif stock and stock.text != "Exclusive":
            price = stock.text
        else:
            price = "Price Not Found"
        item_data[name] = price

    return item_data


def get_item_images(items):
    """ Function to scrape items listed on MyNintendo Rewards"""
    item_images = {}

    for item in items:

        name = item.get('aria-label', 'Unknown Name').strip()

        # targets the element that displays "Exclusive" or "Sold out" label to help determine stock status
        # Use of __DescriptionTag-sc is to reduce the amount of hard coding for the CSS class selection due to website changing what they use
        image = item.find(
            'img', class_=re.compile('EgihB'))

        if not image:
            raise CSSTagSelectorError("The CSS tag for images has changed.")

        image_url = image.get('src', 'https://placehold.co/600x400')

        item_images[name] = image_url

    return item_images


def check_for_changes(last_stored_items, scraped_items):
    """ Function to compare two dictionaries, 
        returning the resulting differences"""

    diff = DeepDiff(last_stored_items, scraped_items)

    if (len(diff) == 0):
        return None

    cleaned_diff = remove_trademark_false_positives(diff)

    if (len(cleaned_diff) == 0):
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


def scrape_mynintendo(current_items):
    """ Function that calls scraping function and updates database if changes were found"""
    last_record = Listings.query.order_by(Listings.id.desc()).first()
    last_items = last_record.items if last_record is not None else {}

    changes = check_for_changes(last_items, current_items)

    if changes:
        Changes.add_record(changes)
    new_item = Listings.add_record(current_items)

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        raise DatabaseError(
            "Database error occurred while updating database for changes.")
    except Exception as e:
        print(str(e))
        raise CustomError(
            e, "Error occurred while updating database for changes.")

    if not changes:
        changes = "No changes."

    return {"items": changes, "timestamp": new_item.timestamp}


def message_discord(changes):
    """ Function that calls Discord webhook to message user of changes on MyNintendo Rewards"""
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
