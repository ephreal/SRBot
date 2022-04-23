# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/srbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils.rolling import sr3e
from utils.embeds import build_embed


class Rolling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r'])
    async def roll(self, ctx, dice, threshold=4):
        """
        Rolls dice. If no version is specified, this will default to SR3
        rolling rules.
        """

        try:
            dice = int(dice)
            threshold = int(threshold)
        except ValueError:
            return await ctx.send("Dice and threshold must be an integer")

        message = await sr3e.general_roll(dice, threshold)
        message = await build_embed(ctx, message['title'], message['message'],
                                    footer=message['footer'])

        await ctx.send(embed=message)


def setup(bot):
    bot.add_cog(Rolling(bot))
