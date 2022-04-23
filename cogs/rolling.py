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
        self.db_handler = self.bot.db_handler.rolling

    @commands.command(aliases=['r'])
    async def roll(self, ctx, *args):
        """
        Rolls dice. If no version is specified, this will default to SR3
        rolling rules.
        """

        roll = sr3e.Roll(*args)
        print(roll.roll_type)

        if roll.roll_type == "help":
            await roll.format_help()
        if roll.roll_type == "initiative":
            await roll.initaitive_roll()
        if roll.roll_type == "open":
            await roll.open_test()
            print(roll.rolls)
        elif roll.roll_type == "general":
            await roll.roll()
            userid = ctx.author.id
            await self.db_handler.save_roll(userid, roll.rolls, roll.threshold)

        embed = await build_embed(ctx, roll.title, roll.message,
                                  footer=roll.footer)

        await ctx.send(embed=embed)

    @commands.command(aliases=['rr'])
    async def reroll(self, ctx):
        """
        Rerolls your last roll.
        """

        userid = ctx.author.id
        rolls, threshold = await self.db_handler.get_last_roll(userid)
        if not rolls:
            return await ctx.send("You have not yet made a roll.")

        rolls = rolls.strip("[]").split(", ")
        rolls = [int(roll) for roll in rolls]
        dice = len([roll for roll in rolls if roll < threshold])
        to_save = [roll for roll in rolls if roll >= threshold]

        roll = sr3e.Roll(str(dice), str(threshold))
        await roll.reroll(to_save)

        await self.db_handler.save_roll(userid, roll.rolls, threshold)
        embed = await build_embed(ctx, roll.title, roll.message,
                                  footer=roll.footer)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rolling(bot))
