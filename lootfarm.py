import re
import json
from os.path import exists
from os import remove
import cloudscraper
from bs4 import BeautifulSoup
from itemprice import ItemPrice


def clear_lootfarm_prices():
    if exists("lootfarm.json"):
        remove("lootfarm.json")


def get_lootfarm_prices() -> list[ItemPrice]:
    fetch_lootfarm_prices()  # writes prices to scraptf.html if not exists

    with open("lootfarm.json") as f:
        all_prices = json.loads(f.read())

    prices = []
    for item in all_prices["result"].values():
        prices.append(ItemPrice(name=item["n"], buy=float(item["p"])/100, sell=None))
    return prices


def fetch_lootfarm_prices():
    if not exists("lootfarm.json"):
        url = "https://loot.farm/botsInventory_440.json"
        scraper = cloudscraper.create_scraper()

        res = scraper.get(url)
        with open("lootfarm.json", "w") as p:
            p.write(res.text)