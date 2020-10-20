from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands, tasks
import asyncio
import requests
import json
from prettyprinter import pprint, cpprint


with open('assets/discord_config.json') as discord_config:
    discord_config = json.load(discord_config)
    client = commands.Bot(command_prefix=".")

    bb = discord_config["bots"]["best_buy"]
    skus = bb["skus"]
    TOKEN = discord_config["tokens"][0]
    print(client)

    @client.event
    async def on_ready():
        print("Bot ready (thumbs up)")

    async def product_status():
        await client.wait_until_ready()
        print("Running Status...")
        counter = 0
        while not client.is_closed():
            c = bb["channels"]["best_buy"]
            channel = client.get_channel(c)
            if channel is None:
                pprint("Channel Not Found")
            else:
                if counter > 4:
                    await asyncio.sleep(30000)
                for sku in skus:
                    product = await get_products(sku, bb["key"])
                    if product['onlineAvailability']:
                        await channel.send(product["addToCartUrl"])
                        counter = counter + 1
                    elif counter < 1:
                        await channel.send(product["addToCartUrl"])
                        counter = counter + 1
                    pprint(product)

            await asyncio.sleep(5)

    async def get_products(sku, apikey):
        base_url = bb['urls']['products']
        url = f"{base_url}/{sku}.json?show=name,sku,onlineAvailability,addToCartUrl&apiKey={apikey}"

        jsonstring = requests.get(url).text
        return json.loads(jsonstring)


    client.loop.create_task(product_status())
    client.run(TOKEN)
