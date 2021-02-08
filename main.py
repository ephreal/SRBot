# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import asyncio
import bot
import importlib
import json
import os
import sys


def load_config():
    """
    Loads bot configuration for use.
    """
    with open("secrets/secrets.json", 'r') as secrets:
        return json.load(secrets)


def first_time_setup(CONFIG):
    """
    Walks the user through for first time setup.

    CONFIG: JSON dict
        -> TOKEN: str
    """
    token = input("Please input your discord bot token here: ")

    CONFIG["token"] = token

    with open("secrets/secrets.json", 'w') as config_file:
        config_file.write(json.dumps(CONFIG, sort_keys=True,
                                     indent=4, separators=(',', ': ')))

    return token


def run_client(client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start(*args, **kwargs))
    except Exception as e:
        print("Error", e)
    print("Restarting...")


CONFIG = load_config()
TOKEN = CONFIG["token"]

if TOKEN == "BOT_TOKEN_HERE":
    TOKEN = first_time_setup(CONFIG)

while not os.path.exists("poweroff"):
    BOT = bot.build_bot("?")
    run_client(BOT, TOKEN)
    importlib.reload(bot)

# Remove the file "poweroff" so it'll turn on next time
os.remove("poweroff")
sys.exit()
