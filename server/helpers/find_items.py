import re
from errors import CSSTagSelectorError


def find_items(soup, tag):
    """Function to scrape items listed on MyNintendo Rewards"""
    items = soup.find_all("a", class_=re.compile(tag))

    if not items:
        raise CSSTagSelectorError("The CSS tag for items have changed.")

    return items
