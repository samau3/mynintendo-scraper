from bs4 import BeautifulSoup
import requests
# import time

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

    print(item_costs)


check_items()
