import requests
import json
import time
import math
from prettyprinter import pprint, cpprint
# from dhooks import Webhook, Embed
from vendor.discord_hooks import Webhook
from utils import DiscordHelper, BaseBot




# with open('../assets/discord_config.json') as discord_config:
#     dc = json.load(discord_config)
#     TOKEN = dc["server_tokens"]["df"]

with open('../assets/bots.json') as bot_info:
    bots = json.load(bot_info)
    bb = bots["best_buy"]
    DISCORDHOOK = bb["webhooks"][0]

class BestBuy(BaseBot):
    __bot_name = "best_buy"


    def product_status(self):
        # await client.wait_until_ready()
        print("Running Status...")

        # Thread Item
        skus = bb["skus"]
        second_delay = math.ceil(86400/50000)*len(skus)

        print(f'Monitor delay is: {second_delay} seconds')
        print("Best Buy API only allows 50000 hits Per DAY")
        counter = 0
        # check = 0
        while True:
            if counter > 0:
                time.sleep(60*10)
                counter = 0

            for sku in bb["skus"]:
                product = api_product_key_url(sku, bb["key"], bb["base_api_url"])
                # pprint(stopwatch)
                if "orderable" in product and product['orderable'] != 'SoldOut':
                    print(sku)
                    DiscordHelper.discordup(DISCORDHOOK, product["addToCartUrl"], product["name"], tn=product["image"], productUrl=product["url"])
                    pprint(product)
                    counter += 1
                    # TODO: find n amount of words
                    print(f'Item in Stock: {product["name"][:25]}')
                elif "name" in product:

                    # check += 1
                    # pprint(check)
                    print(f'Not found: {product["name"][:25]}')
                    # await channel.send(test_sentence)
                else:
                    pprint(product)
                time.sleep(second_delay)
# To test if exception occurs



        # await asyncio.sleep(second_delay)


def api_product_key_url(sku, apikey, base_url):
    url = f"{base_url}/{sku}.json?show=name,sku,onlineAvailability,inStoreAvailability,orderable,addToCartUrl,url,image&apiKey={apikey}"
    r = requests.get(url)
    pprint(r.status_code)
    if r.status_code != 200:
        DiscordHelper.discordup(DISCORDHOOK, "NOT URL", "DEVON THE BOT STOPED WORKING, COME REFRESH ME", "OTher URL")
    jsonstring = r.text
    return json.loads(jsonstring)






if __name__ == '__main__':

    product_status()


# client.run(TOKEN)
