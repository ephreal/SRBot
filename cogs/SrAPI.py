# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/srbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord.ext import commands
from utils import srapi


class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, quote_type=None):
        """
        Fetches a shadowrun quote
        """

        if not quote_type:
            quote_type = "random"

        quote = await srapi.get_quote(quote_type)
        quote = await srapi.remove_bbcode(quote)
        quote = await srapi.replace_bbcode(quote)
        quote = await srapi.replace_html_escapes(quote)
        quote = await srapi.format_quote(quote)
        await ctx.send(embed=quote)

    @commands.command()
    async def character(self, ctx, name=None):
        """
        Fetches a shadowrun character. If a name is provided, searches for a
        character with that name.
        """

        character = await srapi.get_character(name)
        character = await srapi.replace_html_escapes(character)
        character = await srapi.format_character(character)
        await ctx.send(embed=character)


def setup(bot):
    bot.add_cog(Quotes(bot))
