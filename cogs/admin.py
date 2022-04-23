# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/srbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from discord.client import Client


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        Shuts down the bot gracefully.
        """
        await ctx.send("Bot is shutting down.")

        with open("poweroff", "w") as f:
            f.write("powering off")

        self.bot.logger.warn("Bot is shutting down")
        await Client.close(self.bot)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        """
        Retarts the bot gracefully.
        """

        self.bot.logger.warn("Bot is restarting")
        await Client.close(self.bot)


def setup(bot):
    bot.add_cog(Admin(bot))
