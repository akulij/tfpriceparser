import argparse
import sys
import csv

from scraptf import get_scraptf_prices, clear_scraptf_prices
from lootfarm import get_lootfarm_prices, clear_lootfarm_prices
from mannco import get_mannco_prices, clear_mannco_prices
from tradeitgg import get_tradeitgg_prices, clear_tradeitgg_prices


def main(key_price: float, refined_price: float, use_cached):
    if not use_cached:
        clear_scraptf_prices()
        clear_lootfarm_prices()
        clear_mannco_prices()
        clear_tradeitgg_prices()
    scraptf_prices = get_scraptf_prices(key_price, refined_price)
    lootfarm_prices = get_lootfarm_prices()
    mannco_prices = get_mannco_prices()
    tradeitgg_prices = get_tradeitgg_prices()

    prices = {}
    for price in scraptf_prices:
        if not (price.name in prices.keys()):
            prices[price.name] = {
                "scraptf_price": [price.buy],
                "scraptf_price_sell": [price.sell],
                "scraptf_limits": [price.limits],
                "lootfarm_price": [],
                "mannco_price": [],
                "tradeitgg_price": [],
            }
        else:
            prices[price.name]["scraptf_price"].append(price.buy)
    for price in lootfarm_prices:
        if not (price.name in prices.keys()):
            prices[price.name] = {
                "scraptf_price": [],
                "scraptf_price_sell": [],
                "scraptf_limits": "",
                "lootfarm_price": [price.buy],
                "mannco_price": [],
                "tradeitgg_price": [],
            }
        else:
            prices[price.name]["lootfarm_price"].append(price.buy)
    for price in mannco_prices:
        if not (price.name in prices.keys()):
            prices[price.name] = {
                "scraptf_price": [],
                "scraptf_price_sell": [],
                "scraptf_limits": "",
                "lootfarm_price": [],
                "mannco_price": [price.buy],
                "tradeitgg_price": [],
            }
        else:
            prices[price.name]["mannco_price"].append(price.buy)
    for price in tradeitgg_prices:
        if not (price.name in prices.keys()):
            prices[price.name] = {
                "scraptf_price": [],
                "scraptf_price_sell": [],
                "scraptf_limits": "",
                "lootfarm_price": [],
                "mannco_price": [],
                "tradeitgg_price": [price.buy],
            }
        else:
            prices[price.name]["tradeitgg_price"].append(price.buy)

    write_prices(prices)
    if not use_cached:
        clear_scraptf_prices()
        clear_lootfarm_prices()
        clear_mannco_prices()
        clear_tradeitgg_prices()


def write_prices(prices):
    with open("latest.csv", "w") as f:
        writer = csv.writer(f)

        writer.writerow(
            (
                "Название предмета",
                "Цена покупки на scraptf",
                "Цена продажи на scraptf",
                "Лимиты на scraptf",
                "Цена покупки на lootfarm",
                "Цена покупки на mannco",
                "Цена покупки на tradeitgg",
            )
        )

        for name, item_prices in prices.items():
            scraptf_price = item_prices["scraptf_price"]
            scraptf_price_sell = item_prices["scraptf_price_sell"]
            scraptf_limits = item_prices["scraptf_limits"]
            lootfarm_price = item_prices["lootfarm_price"]
            mannco_price = item_prices["mannco_price"]
            tradeitgg_price = item_prices["tradeitgg_price"]
            writer.writerow(
                (
                    name,
                    min(scraptf_price) if len(scraptf_price) else "",
                    min(scraptf_price_sell) if len(scraptf_price_sell) else "",
                    min(scraptf_limits) if len(scraptf_limits) else "",
                    min(lootfarm_price) if len(lootfarm_price) else "",
                    min(mannco_price) if len(mannco_price) else "",
                    min(tradeitgg_price) if len(tradeitgg_price) else "",
                )
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare tf items price (both -k and -r argument needed!)"
    )
    parser.add_argument("-k", help="set price for key")
    parser.add_argument("-r", help="set price for refined")
    parser.add_argument(
        "--cache",
        action="store_true",
        help="use cached (one-time initially downloaded) pages",
    )
    args = parser.parse_args()

    if not (args.k and args.r):
        print("No arguments provided. Pass --help argument for help message")
        exit()

    main(float(args.k), float(args.r), args.cache)
