import re
import json
from os.path import exists
from os import remove
import cloudscraper
from bs4 import BeautifulSoup
from itemprice import ItemPrice


def clear_tradeitgg_prices():
    if exists("tradeitgg.json"):
        remove("tradeitgg.json")


def get_tradeitgg_prices() -> list[ItemPrice]:
    fetch_tradeitgg_prices()  # writes prices to scraptf.html if not exists

    with open("tradeitgg.json") as f:
        all_prices = json.loads(f.read())

    prices = []
    for botinventory in all_prices:
        for rawname, item in botinventory["440"]["items"].items():
            name = rawname.split("_", maxsplit=1)[1]
            prices.append(ItemPrice(name=name, buy=float(item["p"]) / 100, sell=None))
    return prices


def fetch_tradeitgg_prices():
    if not exists("tradeitgg.json"):
        url = "https://inventory.tradeit.gg/sinv/440"
        scraper = cloudscraper.create_scraper()

        headers = {"referer": "https://old.tradeit.gg/?back-to-old=true"}
        res = scraper.get(url, headers=headers)
        with open("tradeitgg.json", "w") as p:
            p.write(res.text)
