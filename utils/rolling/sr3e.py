# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.rolling import base


"""
The rolling rules can be found on page 38 of the SR3E core rulebook.
"""


class GeneralRoll():
    """
    An easy way to represent a roll.
    """
    def __init__(self, dice, threshold):
        self.threshold = threshold
        self.dice = dice
        self.title = None
        self.rolls = None
        self.hits = None
        self.glitch = False
        self.critical_glitch = False
        self.footer = "SR3e Roll"
        self.message = ""

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


async def general_roll(dice, threshold):
    """
    Handles a general roll for SR3E and returns a dict with strings that can
    be used to build messages with.

    Parameters:
        dice: int
        threshold: int

    Returns:
        dict: {rolls, hits, glitch, critical_glitch, message}
    """

    diceroll = GeneralRoll(dice, threshold)
    await diceroll.roll()
    return diceroll


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
    return sum(rolls) + modifier


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
