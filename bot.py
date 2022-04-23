# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import os
import sys
import traceback
import re
import logging

from datetime import datetime
from discord import Game
from discord.ext import commands


def build_bot(prefix, config):

    BOT = commands.Bot(command_prefix=prefix)
    BOT.sr_rules = config['optional_rolling_rules']

    # Configure the bot to log error messages properly
    BOT.logger = logging.getLogger()
    if not BOT.logger.handlers:
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler = logging.StreamHandler(sys.stdout)
        BOT.logger.addHandler(stream_handler)

    BOT.logger.info("Logging initialized.")

    @BOT.event
    async def on_member_join(member):
        # Setup user information here.
        pass

    @BOT.event
    async def on_ready():
        """
        Post setup hook.
        Initializes any necessary variables and sets the played game to
        a message on how to get help.
        """
        # Initialize needed variables
        # initialize music players dict
        BOT.players = {}

        # Uptime statistic
        BOT.boot_time = datetime.now()

        # Load all cogs
        BOT.logger.info("Startup complete, loading cogs.")
        await load_cogs()
        BOT.logger.info("Cog loading complete.")
        BOT.logger.info("Connected to server and awaiting commands.")
        BOT.logger.warn("Bot is ready to receive commands.")

        # Set help message
        help_message = Game(name=f"message '{prefix}help' for help")
        if not hasattr(BOT, 'appinfo'):
            BOT.appinfo = await BOT.application_info()
        await BOT.change_presence(activity=help_message)

    @BOT.event
    async def on_message(message):
        """
        Generic operations on user message. For example, adding to analytics to
        see if users are active on the guild.
        """

        if message.author.bot:
            return

        if message.content.startswith(f"{BOT.command_prefix*2}"):
            return

        if message.content.startswith(prefix):
            await BOT.process_commands(message)
            command = message.content.split()
            command = command[0].replace(BOT.command_prefix, "")

        commands = re.findall("{%(.*?)%}", message.content)
        if commands:
            for command in commands:
                command = command.strip()
                if not command.startswith(BOT.command_prefix):
                    command = BOT.command_prefix + command
                message.content = command
                await BOT.process_commands(message)

    @BOT.event
    async def on_command_error(ctx, error):
        await ctx.send(error)

    async def load_cogs(unload_first=False):
        """
        Handles loading all cogs in for the bot.
        """

        cogs = [cog for cog in os.listdir('cogs')
                if os.path.isfile(f"cogs/{cog}")]

        cogs = [cog.replace(".py", "") for cog in cogs]

        for extension in cogs:
            try:
                BOT.logger.debug(f"Loading {extension}...")
                BOT.load_extension(f"cogs.{extension}")
                BOT.logger.debug(f"Loaded {extension}")

            except AttributeError:
                BOT.logger.critical(f"Cog {extension} is malformed.",
                                    "Do you have a setup function?")

            except ModuleNotFoundError:
                BOT.logger.warn(f"Could not find {extension}.",
                                "Please make sure it exists.")

            except OSError as lib_error:
                BOT.logger.warn("Opus is probably not installed")
                BOT.logger.warn(f"{lib_error}")

            except commands.errors.ExtensionAlreadyLoaded:
                BOT.logger.warn(f"The cog {extension} is already loaded.\n"
                                "Skipping the load process for this cog.")

            except SyntaxError:
                BOT.logger.critical(f"The cog {extension} has a syntax error.")
                BOT.logger.critical(traceback.format_exc())

            except commands.errors.NoEntryPointError:
                BOT.logger.critical(f"Cog {extension} has no setup function.")

    return BOT


if __name__ == "__main__":
    print("The bot must be ran with 'python main.py'")
    sys.exit()
