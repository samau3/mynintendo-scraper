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
        'div', class_=re.compile('sc-1bsju6x-4'))
    # print(items)
    if not items:
        raise CSSTagSelectorError("The CSS tag for items have changed.")

    for item in items:
        # the website changes what header is used (e.g. h2, h3) so need a non hard coded way to target it via find_next()
        header = item.div.find_next()
        name = header.text.strip() if header else "Unknown Name"

        # targets the element that displays "Exclusive" or "Sold out" label to help determine stock status
        # Use of __DescriptionTag-sc is to reduce the amount of hard coding for the CSS class selection due to website changing what they use
        stock = item.find(
            'div', class_=re.compile('sc-tb903t-0'))

        if not stock:
            raise CSSTagSelectorError("The CSS tag for stock has changed.")

        if stock and stock.text == "Exclusive":
            price_element = item.find('div', class_=re.compile(
                'sc-1f0n8u6-8'))
            price = price_element.get_text() if price_element else "Price Not Found"
        elif stock and stock.text != "Exclusive":
            price = stock.text
        else:
            price = "Price Not Found"
        item_costs[name] = price

    return item_costs


def check_for_changes():
    """ Function to compare two dictionaries, 
        returning the resulting differences"""

    # diff = DeepDiff(last_stored_items, scraped_items)

    # old = {
    #     "Splatoon x The Legend of Zelda Splatfest Keychain Set": "550 Platinum Points"
    # }

    # new = {
    #     "Splatoon™ x The Legend of Zelda™ Splatfest Keychain Set": "550 Platinum Points"
    # }

    scraped_items = {
        "Princess Peach™: Showtime! Pocket Folder Set": "600 Platinum Points",
        "My Nintendo Mario™ Zipper Pouch": "800 Platinum Points",
        "My Nintendo Super Mario™ Removable Tech Sticker sheet": "300 Platinum Points",
        "Splatoon™ 3:  Expansion Pass - Side Order Tech Sticker sheet": "300 Platinum Points",
        "Pokémon™ Scarlet and Pokémon™ Violet Partner Pokémon Mini-Notebook": "500 Platinum Points",
        "Pokémon™ Scarlet and Pokémon™ Violet Highlighter": "500 Platinum Points",
        "Splatoon™ 3: Splatsville Shopping Bag": "800 Platinum Points",
        "Splatoon 3: Graffiti Sticker Set": "400 Platinum Points",
        "WarioWare™: Move It! Magnets": "500 Platinum Points",
        "My Nintendo 2024 Desktop Calendar": "400 Platinum Points",
        "Super Mario™ Holiday Ornament": "500 Platinum Points",
        "Mario Kart™ 8 Deluxe Vinyl Sticker Sheet No. 2": "300 Platinum Points",
        "Detective Pikachu™ Returns Cup Cozy": "500 Platinum Points",
        "Super Mario Bros.™ Wonder Double Keychain": "800 Platinum Points",
        "Super Mario™ Shopping Bag": "800 Platinum Points",
        "Xenoblade Chronicles™ 3: Camping Coasters (set of 4)": "700 Platinum Points",
        "Pikmin™ 4 Kitchen Towel": "600 Platinum Points",
        "Pikmin™ 4 Shoe Charm Set": "500 Platinum Points",
        "Pikmin™ 4 - Sticker Set": "200 Platinum Points",
        "Mario Kart™ 8 Deluxe Vinyl Sticker Sheet": "300 Platinum Points",
        "Splatoon™ x The Legend of Zelda™ Splatfest  Keychain Set": "550 Platinum Points",
        "Metroid Prime™ Remastered - Big Pin Set": "800 Platinum Points",
        "Kirby’s Return to Dream Land™ Deluxe – Kirby & Magolor Canvas Pouch": "500 Platinum Points",
        "My Nintendo Platinum Point and Gold Point Coins Pin Set": "800 Platinum Points",
        "Fire Emblem™ Engage Character Button pins": "700 Platinum Points",
        "Kirby's Dream Buffet Keychain": "600 Platinum Points",
        "MARIO + RABBIDS®  SPARKS OF HOPE keychain": "400 Platinum Points",
        "Super Smash Bros.™ Ultimate Invitation Greeting Card Set": "400 Platinum Points",
        "Mario & Me: A Three-Year Journey Journal Book": "800 Platinum Points",
        "Mario Strikers™: Battle League Drawstring Bag": "600 Platinum Points",
        "Fire Emblem™ Warriors: Three Hopes Memo Pad": "600 Platinum Points",
        "Nintendo Switch™ Sports - Spocco Square Cooling Towel": "550 Platinum Points",
        "Mario Golf™: Super Rush ID Tag": "600 Platinum Points",
        "Bravely Default™ II Reversible Poster": "400 Platinum Points",
        "DC Super Hero Girls™: Teen Power Drawstring Bag": "500 Platinum Points"
    }

    last_stored_items = {
        "Princess Peach™: Showtime! Pocket Folder Set": "600 Platinum Points",
        "My Nintendo Mario™ Zipper Pouch": "800 Platinum Points",
        "My Nintendo Super Mario™ Removable Tech Sticker sheet": "300 Platinum Points",
        "Splatoon™ 3:  Expansion Pass - Side Order Tech Sticker sheet": "300 Platinum Points",
        "Pokémon™ Scarlet and Pokémon™ Violet Partner Pokémon Mini-Notebook": "500 Platinum Points",
        "Pokémon™ Scarlet and Pokémon™ Violet Highlighter": "500 Platinum Points",
        "Splatoon™ 3: Splatsville Shopping Bag": "800 Platinum Points",
        "Splatoon 3: Graffiti Sticker Set": "400 Platinum Points",
        "WarioWare™: Move It! Magnets": "500 Platinum Points",
        "My Nintendo 2024 Desktop Calendar": "400 Platinum Points",
        "Super Mario™ Holiday Ornament": "500 Platinum Points",
        "Mario Kart™ 8 Deluxe Vinyl Sticker Sheet No. 2": "300 Platinum Points",
        "Detective Pikachu™ Returns Cup Cozy": "500 Platinum Points",
        "Super Mario Bros.™ Wonder Double Keychain": "800 Platinum Points",
        "Super Mario™ Shopping Bag": "800 Platinum Points",
        "Xenoblade Chronicles™ 3: Camping Coasters (set of 4)": "700 Platinum Points",
        "Pikmin™ 4 Kitchen Towel": "600 Platinum Points",
        "Pikmin™ 4 Shoe Charm Set": "500 Platinum Points",
        "Pikmin™ 4 - Sticker Set": "200 Platinum Points",
        "Mario Kart™ 8 Deluxe Vinyl Sticker Sheet": "300 Platinum Points",
        "Splatoon x The Legend of Zelda™ Splatfest  Keychain Set": "550 Platinum Points",
        "Metroid Prime™ Remastered - Big Pin Set": "800 Platinum Points",
        "Kirby’s Return to Dream Land™ Deluxe – Kirby & Magolor Canvas Pouch": "500 Platinum Points",
        "My Nintendo Platinum Point and Gold Point Coins Pin Set": "800 Platinum Points",
        "Fire Emblem™ Engage Character Button pins": "700 Platinum Points",
        "Kirby's Dream Buffet Keychain": "600 Platinum Points",
        "MARIO + RABBIDS®  SPARKS OF HOPE keychain": "400 Platinum Points",
        "Super Smash Bros.™ Ultimate Invitation Greeting Card Set": "400 Platinum Points",
        "Mario & Me: A Three-Year Journey Journal Book": "800 Platinum Points",
        "Mario Strikers™: Battle League Drawstring Bag": "600 Platinum Points",
        "Fire Emblem™ Warriors: Three Hopes Memo Pad": "600 Platinum Points",
        "Nintendo Switch™ Sports - Spocco Square Cooling Towel": "550 Platinum Points",
        "Mario Golf™: Super Rush ID Tag": "600 Platinum Points",
        "Bravely Default™ II Reversible Poster": "400 Platinum Points",
        "DC Super Hero Girls™: Teen Power Drawstring Bag": "500 Platinum Points"
    }

    diff = DeepDiff(last_stored_items, scraped_items)

    if (len(diff) == 0):
        return None
    
    cleaned_dict = diff.copy()

    for difference in cleaned_dict:
        cleaned_dict[difference] = remove_trademark_symbols_from_list(cleaned_dict[difference])

    l1, l2 = index_of_common_strings(cleaned_dict["dictionary_item_added"], cleaned_dict["dictionary_item_removed"])

    for i in range(len(l1) - 1, -1, -1):
        diff["dictionary_item_added"].pop(l1[i])
        if len(diff["dictionary_item_added"]) == 0:
            del diff["dictionary_item_added"]
    for i in range(len(l2) - 1, -1, -1):
        diff["dictionary_item_removed"].pop(l2[i])
        if len(diff["dictionary_item_removed"]) == 0:
            del diff["dictionary_item_removed"]
        
    if (len(diff) == 0):
        return None

    changes = {}
    for difference in diff:

        # if difference is added
        if difference == "dictionary_item_added":
            new_items = []
            for item in diff[difference]:
                print(item[6:-2], scraped_items[item[6:-2]])
                new_items.append({item[6:-2]: scraped_items[item[6:-2]]})
            changes["New Items"] = new_items

        # if difference is removed
        if difference == "dictionary_item_removed":
            removed_items = []
            for item in diff[difference]:
                print(item[6:-2], last_stored_items[item[6:-2]])
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

def remove_trademark_symbols_from_list(input_list):
    cleaned_list = []
    for string in input_list:
        # Using re.sub() to remove trademark symbols from each string in the list
        cleaned_string = re.sub(r'™', '', string)
        cleaned_list.append(cleaned_string)
    return cleaned_list

def index_of_common_strings(list1, list2):
    l1_idx = []
    l2_idx = []
    for idx, item in enumerate(list1):  # Iterate over a copy of list1 to avoid modifying it while iterating
        if item in list2:
            l1_idx.append(idx)
            l2_idx.append(list2.index(item))
    return l1_idx, l2_idx


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
