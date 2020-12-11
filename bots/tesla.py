from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands, tasks
import asyncio
import requests
import json
from prettyprinter import pprint, cpprint



discord_config = open('assets/discord_config.json')

dc = json.load(discord_config)
client = commands.Bot(command_prefix=".")


TOKEN = dc["server_tokens"]["df"]
print(client)


client.run(TOKEN)
