# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rolling import base
from utils.rolling.parsers import Sr3RollParser


"""
The rolling rules can be found on page 38 of the SR3E core rulebook.
"""


class Roll():
    """
    An easy way to represent a roll.
    """
    def __init__(self, *to_parse):
        self.parser = Sr3RollParser()
        parsed = self.parser.parse_args(to_parse)

        # Used to determine which kind of roll this is later
        self.roll_type = None

        self.threshold = parsed.threshold
        self.dice = parsed.dice

        if parsed.help:
            self.footer = "SR3e Roll Help"
            self.roll_type = "help"
        elif parsed.i:
            self.footer = "SR3e Initiative Roll"
            self.roll_type = "initiative"
        elif parsed.open:
            self.footer = "SR3e Open Test"
            self.roll_type = "open"
        else:
            self.footer = "SR3e Roll"
            self.roll_type = "general"

        self.title = None
        self.rolls = None
        self.hits = None
        self.glitch = False
        self.critical_glitch = False
        self.message = ""
        self.initiative = None
        self.init_mod = parsed.m
        self.note = parsed.note

    async def roll(self):
        """
        Rolls the dice and sets all the appropriate attributes
        """

        self.rolls = await roll(self.dice)
        self.hits = await hits(self.rolls, self.threshold)
        self.critical_glitch = await critical_glitch(self.rolls)
        self.glitch = await glitch(self.rolls)

        # Generate the message so it's ready to go.
        await self.formatted_message()

    async def reroll(self, saved):
        """
        Runs a reroll with the dice passed in.
        """

        self.rolls = await roll(self.dice)
        self.rolls.extend(saved)
        self.rolls.sort()

        self.dice += len(saved)

        self.hits = await hits(self.rolls, self.threshold)
        self.critical_glitch = await critical_glitch(self.rolls)
        self.glitch = await glitch(self.rolls)

        await self.formatted_message()

    async def initiative_roll(self):
        """
        Rolls initiative.
        """

        self.rolls, self.initiative = await roll_initiative(self.dice,
                                                            self.init_mod)
        await self.format_initiative_message()

    async def open_test(self):
        """
        Rolls an open test and formats the message accordingly.
        """

        self.rolls = await roll(self.dice)

        await self.format_open_test()

    async def formatted_message(self):
        """
        Creates and returns a formatted message.
        """

        descriptor = "Hit"
        if self.hits > 1:
            descriptor = "Hits"

        self.message = f"""
            ```md
            <{descriptor}: {self.hits} >
            ===================

            > Results: {self.rolls}
            > Target Number: {self.threshold}

            Dice Rolled: {self.dice}
            ===================

            """

        if self.critical_glitch:
            self.message += "< Critical Glitch >\n"

        self.message += "```"

        self.message = self.message.replace("            ", "")

    async def format_initiative_message(self):
        """
        Formats the initiative in an easy to read fashion.
        """

        self.message = f"""
            ```md
            < Initiative {self.initiative}
            ==============================

            > Rolls: {self.rolls}
            > Modifier: {self.init_mod}
            > Sum: {sum(self.rolls)} + {self.init_mod} = {self.initiative}

            Dice Rolled: {self.dice}
            ==============================
            ```"""

        self.message = self.message.replace("            ", "")

    async def format_help(self):
        """
        Formats a help message that can be returned to the user.
        """

        self.message = f"""
        ```md
        {self.parser.format_help()}
        ```"""

        self.message = self.message.replace("            ", "")
        self.message = self.message.replace("        ", "")

    async def format_open_test(self):
        """
        Formats an open test to return to the user.
        """

        self.message = f"""
            ```md
            < Threshold: {self.rolls[-1]} >
            ===============================

            > Rolls: {self.rolls}

            Dice Rolled: {self.dice}
            ===============================
            ```"""

        self.message = self.message.replace("            ", "")


async def roll(dice):
    """
    Rolls the specified amount of dice. This rerolls sixes and adds the
    results to the original rolls.

    Parameters:
        dice: int

    Returns:
        rolls: [int, int..., int]
    """

    rolls = await base.roll(dice)
    rolls.sort()

    six = [roll for roll in rolls if roll == 6]

    if six:
        pos = len(rolls) - len(six)
        rolls[pos:] = [x + y for x, y in zip(six, await roll(len(six)))]

    return rolls


async def hits(rolls, threshold):
    """
    Checks the rolls to see how many of the rolls meet or exceed the threshold.

    Parameters:
        rolls: [int, int, int..., int]
        threshold: int

    Returns:
        count: int
    """

    count = [roll for roll in rolls if roll >= threshold]
    return len(count)


async def roll_initiative(dice, modifier):
    """
    Rolls initiative and returns the total value of the rolls + modifier

    Parameters:
        dice: int
        modifier: int

    Returns:
        initiative: int
    """

    rolls = [await base.roll() for i in range(0, dice)]
    return [rolls, sum(rolls) + modifier]


async def critical_glitch(rolls):
    """
    Checks to see if a critical glitch has occurred. This occurs when all the
    dice are 1's.

    Parameters:
        dice: [int, int,...,int]

    Returns:
        True or None
    """

    ones = [roll for roll in rolls if roll == 1]
    return len(ones) == len(rolls)


async def glitch(rolls):
    """
    Checks to see if a glitch has occurred. A glitch occurs when the amount of
    ones is >= the amount of rolled * .5.

    If the number of rolls is not even, the number or rolls will be artifically
    inflated by 1 during the check.

    Note: SR3E doesn't have rules in place for a non-critical glitch. This is
    modified from SR5E and is an OPTIONAL rolling rule that will need to be
    enabled in the bot config.

    Parameters:
        rolls: [int, int,...,int]

    Returns:
        True or None
    """
    ones = [roll for roll in rolls if roll == 1]
    rolls = len(rolls)

    if not (rolls % 2) == 0:
        rolls += 1

    if len(ones) >= (rolls / 2):
        return True

    return False
