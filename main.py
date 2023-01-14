from bs4 import BeautifulSoup
import requests
from deepdiff import DeepDiff
from models import db, Listings

url = "https://www.nintendo.com/store/exclusives/rewards/"

# get the text from the provided url
html_text = requests.get(url).text


def check_items():
    """ Function to scrap items listed on MyNintendo Rewards"""

    soup = BeautifulSoup(html_text, 'lxml')
    item_costs = {}
    items = soup.find_all(
        'div', class_='BasicTilestyles__Info-sc-sh8sf3-5 hemcMo')
    for item in items:
        name = item.div.h3.text
        stock = item.find(
            'div', 'ProductTilestyles__DescriptionTag-sc-n2s21r-5 fqZZBn')

        if not stock:
            price = item.find(
                'div', 'ProductTilestyles__PriceWrapper-sc-n2s21r-4 jrjiqe').div.div.span.div.span.text

        cost = f'{stock.text}' if stock else price

        item_costs[name] = cost

    return item_costs


def check_for_changes(last_stored_items, scraped_items):
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
            changes["new_items"] = new_items

        # if difference is removed
        if difference == "dictionary_item_removed":
            removed_items = []
            for item in diff[difference]:
                removed_items.append(
                    {item[6:-2]: last_stored_items[item[6:-2]]})
            changes["removed_items"] = removed_items
        # if difference is changed
        if difference == "values_changed":
            changed_items = []
            for item in diff[difference]:
                changed_items.append({item[6:-2]: diff[difference][item]})
            changes["changed_items"] = changed_items

    return changes


def scrape_mynintendo():
    results = check_items()
    last_record = Listings.query.order_by(Listings.id.desc()).first()
    last_items = last_record.items if last_record is not None else {}

    changes = check_for_changes(last_items, results)
    has_changed = False if changes is None else True

    Listings.add_record(results, has_changed)
    db.session.commit()  # wrap in a try/catch?

    if has_changed:
        return changes

    return {}
