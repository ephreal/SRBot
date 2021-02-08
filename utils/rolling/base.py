# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/SRBot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import random


async def roll(dice_pool=1, sides=6):
    # Weirdly, randrange seems to be way faster than randint
    return [random.randrange(sides) + 1 for _ in range(0, dice_pool)]
