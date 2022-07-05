import cloudscraper
import re
from bs4 import BeautifulSoup
from os.path import exists
from os import remove
from itemprice import ItemPrice


def clear_scraptf_prices():
    if exists("scraptf.html"):
        remove("scraptf.html")


def get_scraptf_prices(key_price: int, refined_price: int) -> tuple[list[ItemPrice], str]:
    fetch_scraptf_prices()  # writes prices to scraptf.html if not exists

    with open("scraptf.html") as f:
        page_content = f.read()

    parser = BeautifulSoup(page_content, "html.parser")
    page_table = parser.find("table", id="itembanking-list")

    # tbody -> tr -> td
    tablebody = page_table.find("tbody")
    tablerows = tablebody.find_all("tr")
    prices = []
    for tablerow in tablerows:
        rowcells = tablerow.find_all("td")
        name, buy_raw, sell_raw = rowcells[1:4]
        limits = rowcells[4].findChildren("div" , recursive=False)[0].get("title")
        name, buy_raw, sell_raw = (
            name.text.strip(),
            buy_raw.text.strip(),
            sell_raw.text.strip(),
        )
        buy_total_price = parse_price(buy_raw, key_price, refined_price)
        sell_total_price = parse_price(sell_raw, key_price, refined_price)
        prices.append(ItemPrice(name=name, buy=buy_total_price, sell=sell_total_price, limits=limits))
    return prices


def fetch_scraptf_prices():
    if not exists("scraptf.html"):
        url = "https://scrap.tf/items"
        scraper = cloudscraper.create_scraper()

        res = scraper.get(url)
        with open("scraptf.html", "w") as p:
            p.write(res.text)


def parse_price(price_string: str, key_price: int, refined_price: int) -> int:
    refined_pattern = re.compile(r"(\d*.?\d+) refined")
    key_pattern = re.compile(r"(\d+) key")
    refined_total, key_total = 0, 0
    if refined_pattern.search(price_string) is not None:
        refined_total = float(refined_pattern.search(price_string).group(1)) * refined_price
    if key_pattern.search(price_string) is not None:
        key_total = float(key_pattern.search(price_string).group(1)) * key_price
    return refined_total + key_total
