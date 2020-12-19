from bs4 import BeautifulSoup
import requests, json, csv, os
from pprint import pprint
import threading
import concurrent.futures
from vendor.discord_hooks import Webhook

# helpers for discord

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


# Create a bot class late has internal function for bot

class BaseBot:
    __bot_name = ""

    def __init__(self, info):

        self._info = info
        if "webhook" in info:
            self._hook = info["webhook"]

        #add key token in here

    def _load_proxli(self):
        return []


    def __monitor(self, **kwargs):
        pass


    def __monitor_urls(self, **kwargs):
        return None

    def _get_product_ids(self):
        if "skus" in self._info:
            return self._info["skus"]

    @staticmethod
    def json_monitor_response(url, discord_hook=None):
        r = requests.get(url)
        pprint(r.status_code)
        if discord_hook is not None and r.status_code != 200:
            DiscordHelper.discordup(discord_hook, "Should through exception and not",
                                    "DEVON THE BOT STOPPED WORKING, COME REFRESH ME",
                                    "Other URL")
        jsonstring = r.text
        return json.loads(jsonstring)





class BotLoader:

    def __init__(self):
        with open('assets/bots.json') as bot_info:
            self._bot_init_info = json.load(bot_info)
            self._bot_init = self._bot_init_info


    def save_bot_json(self, new_info):
        tmp_file = open("assets/bots.json", "w")
        json.dump(self._bot_init_info, tmp_file)
        tmp_file.close()


    def load(self):
        payload = input("What bots would you like to run?")
        # accepts comma seperated bots
        # accepts strings "all" and "test"
        spayload = payload.split(",|, ")
        pay_str = spayload.pop(0)
        bots_running = []
        if len(spayload) == 0:
            if pay_str == "all" or pay_str == "test":
                for bot_name, bot_info in self._bot_init_info:
                    Name = bot_name.title().replace('_', '')
                    # call instance of class:
                    # multi-process

    @staticmethod
    def update_proxy_list():
        # updated with split lines method
        with open('bot_config/eproxy.txt', 'r') as proxx:
            proxx = proxx.read().splitlines()
            PROXYLIST = [BotLoader.imp_proxy_format(p) for p in proxx if p.strip() != '']


        print("You have entered {} proxies".format(len(PROXYLIST)))


    @staticmethod
    def imp_proxy_format(px):
        p = px.strip().split(":", 2)
        p2 = ":".join([p[0], p[1]])
        return "@".join([p[2], p2])

    @staticmethod
    def toggle_proxy_format(proxy_str):
        # proxy_str = proxy_str.strip()
        try:
            # if the sting is
            p0 = proxy_str[0]
            if p0.isnumeric():
                # takes import format 91.149.237.216:65112:fqtcyvi9tqm:n5w288bvcx8
                # to web or final format fqtcyvi9tqm:n5w288bvcx8@91.149.237.216:65112
                p = proxy_str.split(":", 2)
                p2 = ":".join([p[0], p[1]])
                return "@".join([p[2], p2])
            elif p0.isalpha():
                print(True)
                # takes import format fqtcyvi9tqm:n5w288bvcx8@91.149.237.216:65112
                # to web or final format 91.149.237.216:65112:fqtcyvi9tqm:n5w288bvcx8
                j = proxy_str.split("@")
                return ':'.join([j[1], j[0]])

        except:
            print("Import string is not correct proxy format")
            # TODO: Exception so script prompts funcitionality "developer should chck what is going on"


if __name__ == '__main__':
    input_command = input("Input Command")

    if input_command == 'iproxy':
        BotLoader.update_proxy_list()

    # test_str = "91.149.237.216:65112:fqtcyvi9tqm:n5w288bvcx8"
    # web_version = BotHelper.toggle_proxy_format(test_str)
    # print(f'Web Version: {web_version}')
    # proxy_storage = BotHelper.toggle_proxy_format(web_version)
    # print(f'Proxy: {proxy_storage}')
    # pprint(proxy_storage == test_str)
    #
    # BotLoader.load()
