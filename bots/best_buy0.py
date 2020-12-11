from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands, tasks
import asyncio
import requests
import json
import time
import math
from prettyprinter import pprint, cpprint

with open('../assets/discord_config.json') as discord_config:
    dc = json.load(discord_config)
    TOKEN = dc["server_tokens"]["df"]
with open('../assets/bots.json') as bot_info:
    bots = json.load(bot_info)
    bb = bots["best_buy"]

client = commands.Bot(command_prefix=".")



print(client)

discord_config.close()
stopwatch = time.perf_counter()


@client.event
async def on_ready():

    print("Bot ready (thumbs up)")


try:
    async def product_status():
        await client.wait_until_ready()
        print("Running Status...")
        skus = bb["skus"]

        second_delay = math.ceil(86400/50000)*len(skus)
        print(f'Monitor delay is: {second_delay} seconds')
        print("Best Buy API only allows 50000 hits Per DAY")
        counter = 0
        while not client.is_closed():
            c = bb["discord_channel"]
            channel = client.get_channel(c)
            if channel is None:
                pprint("Channel Not Found")
            else:
                    if counter > 4:
                        await asyncio.sleep(60*5)
                        counter = 1
                    for sku in skus:
                        product = await api_product_api_key_url(sku, bb["key"], bb["base_api_url"])
                        if "onlineAvailability" in product and product['onlineAvailability']:
                            await channel.send(product["addToCartUrl"])
                            counter += 1
                        elif counter < 1:
                            # Test that sends item URL on first round
                            test_sentence = f'This is a test for cart url of the {product["name"]}: {product["addToCartUrl"]}'
                            await channel.send(test_sentence)
                            counter += 1
                        pprint(product)
            await asyncio.sleep(second_delay)

except TaskException as e:
    print()

else:
    client.loop.create_task(product_status())

finally:
    print()




async def api_product_api_key_url(sku, apikey, base_url):
    url = f"{base_url}/{sku}.json?show=name,sku,onlineAvailability,addToCartUrl&apiKey={apikey}"

    jsonstring = requests.get(url).text
    return json.loads(jsonstring)


client.run(TOKEN)
