import re
import json
from os.path import exists
from os import remove
import cloudscraper
from bs4 import BeautifulSoup
from itemprice import ItemPrice


def clear_mannco_prices():
    if exists("mannco.json"):
        remove("mannco.json")


def get_mannco_prices() -> list[ItemPrice]:
    fetch_mannco_prices()  # writes prices to scraptf.html if not exists

    with open("mannco.json") as f:
        all_prices: dict = json.loads(f.read())

    prices = []
    for botdata in all_prices.values():
        for item in botdata["response"].values():
            if float(item["price"]) > 0:
                prices.append(
                    ItemPrice(name=item["name"], buy=float(item["price"]), sell=None)
                )
    return prices


def fetch_mannco_prices():
    if not exists("mannco.json"):
        url = "https://mannco.trade/api/getBotsInventory"
        scraper = cloudscraper.create_scraper()

        res = scraper.get(url)
        with open("mannco.json", "w") as p:
            p.write(res.text)
