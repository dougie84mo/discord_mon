from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands, tasks
from itertools import cycle
import json


class APIHelper:

    @staticmethod
    def apiKey(key):
        return f'&apiKey={key}'
