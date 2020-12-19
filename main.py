from pprint import pprint
import sys, importlib, json
import concurrent.futures
from utils import BotLoader




#create application



def multi_thread_asset():
    with open('assets/bots.json') as bot_info:
        bots = json.load(bot_info)

    with concurrent.futures.ThreadPoolExecutor() as main_executor:
        global executor



if __name__ == '__main__':
    Bot

