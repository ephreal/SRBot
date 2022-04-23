# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import bot
import importlib
import json
import os
import sys


def load_secrets():
    """
    Loads bot configuration for use.
    """
    with open("secrets/secrets.json", 'r') as secrets:
        return json.load(secrets)


def load_config():
    """
    Loads the config
    """

    with open('config/config.json', 'r') as config:
        return json.load(config)


def first_time_setup(SECRETS):
    """
    Walks the user through for first time setup.

    SECRETS: JSON dict
        -> TOKEN: str
    """
    token = input("Please input your discord bot token here: ")

    SECRETS["token"] = token

    with open("secrets/secrets.json", 'w') as config_file:
        config_file.write(json.dumps(SECRETS, sort_keys=True,
                                     indent=4, separators=(',', ': ')))

    return token


CONFIG = load_config()
SECRETS = load_secrets()
TOKEN = SECRETS["token"]

if TOKEN == "BOT_TOKEN_HERE":
    TOKEN = first_time_setup(SECRETS)

while not os.path.exists("poweroff"):
    print("Bot is starting up...")
    BOT = bot.build_bot("?", CONFIG)
    BOT.run(TOKEN)
    importlib.reload(bot)

# Remove the file "poweroff" so it'll turn on next time
os.remove("poweroff")
sys.exit()
