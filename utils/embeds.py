# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/srbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from discord import Colour, Embed


async def build_embed(ctx, title, message, footer=None, color=Colour.blue()):
    """
    Builds a nice looking embed from the message passed in.

    Parameters:
        ctx: discord.py ctx object
        title: str
        message: str
        color: discord.color.Colour

    Returns:
        Embed
    """

    author = ctx.message.author

    embed = Embed()
    embed.title = title
    embed.description = message
    embed.set_author(name=author.name, icon_url=author.avatar_url)
    embed.thumbnail.height = 128
    embed.thumbnail.width = 128
    embed.color = color

    if footer:
        embed.set_footer(text=footer)

    return embed
