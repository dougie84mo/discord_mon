from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands, tasks
from itertools import cycle
import json
from pprint import pprint
import threading
from vendor.discord_hooks import Webhook



# Create a bot class late has internal function for bot

# helpers for discord


class BaseBot:
    _bot_name=""
    __multi_thread=False

    def __init__(self, hook, multi_thread=None):
        self._hook = hook
        with open('assets/bots.json') as bot_info:
            bots = json.load(bot_info)
            self._info = bots[self._bot_name]

        if multi_thread is True:
            self.__multi_thread = True

    def monitor(self):
        pass





class DiscordHelper:

    @staticmethod
    def get_token(token, key="server_token"):
        with open('../assets/discord_config.json') as discord_config:
            dc = json.load(discord_config)
            token = dc[key][token]

        return token

    @staticmethod
    def discordup(hook, addToCartUrl, productName, productUrl, description=None, image=None, tn=None):
        embed = Webhook(hook)
        # embed.set_author(name=f'[{productName}]({productUrl})')
        embed.set_title(title=productName, url=productUrl)
        embed.set_desc(f'[CLICK TO ADD TO CART]({addToCartUrl})')
        if description is not None:
            embed.add_field(name='Description: ', value=description)
        if image is not None:
            embed.set_image(image)
        if tn is not None:
            embed.set_thumbnail(tn)
        embed.set_footer(text='Created by SecureTheHype', icon_url='https://image.ibb.co/gq7xgT/blackyzylogo.png',
                         ts=True)
        embed.post()


class BotHelper:

    @staticmethod
    def user_agents():
        return [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
            ""
        ]


    @staticmethod
    def bot_page_monitor():
        return {
            "tesla": "",
            "best_buy": "",
        }


    @staticmethod
    def bot_api_monitor(mon_arg, key=None):

        if key is None:
            url_monitors = {}
            if 2 in mon_arg:
                url_monitors.update({
                    "best_buy": f"{mon_arg[0]}{mon_arg[1]}.json?show=name,sku,onlineAvailability,addToCartUrl&apiKey={mon_arg[2]}"
                 })
            elif 1 in mon_arg:
                url_monitors.update({
                    "tesla": f"{mon_arg[0]}{mon_arg[1]}"
                })

            return
