# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""


import os
import traceback
import re

from datetime import datetime
from discord import Game
from discord.ext import commands


def build_bot(prefix):

    BOT = commands.Bot(command_prefix=prefix)

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
        print("Startup complete, loading Cogs....")
        await load_cogs()
        print("Cog loading complete.")
        print("Connected to server and awaiting commands.")

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
            await BOT.db_handler.metrics.update_commands(command, 1)

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
                print(f"Loading {extension}...")
                BOT.load_extension(f"cogs.{extension}")
                print(f"Loaded {extension}")

            except AttributeError as e:
                print(f"Cog {extension} is malformed. Do you have a setup"
                      "function?")
                traceback.print_tb(e.__traceback__)

            except ModuleNotFoundError:
                print(f"Could not find {extension}. Please make sure it "
                      "exists.")

            except OSError as lib_error:
                print("Opus is probably not installed")
                print(f"{lib_error}")

            except commands.errors.ExtensionAlreadyLoaded:
                print(f"The cog {extension} is already loaded.\n"
                      "Skipping the load process for this cog.")

            except SyntaxError as e:
                print(f"The cog {extension} has a syntax error.")
                traceback.print_tb(e.__traceback__)

            except commands.errors.NoEntryPoint as e:
                print(f"Cog {extension} has no setup function.")
                traceback.print_tb(e.__traceback__)

    return BOT


if __name__ == "__main__":
    import sys
    print("The bot must be ran through main.py")
    print("Please run 'python main.py' instead")
    sys.exit()
