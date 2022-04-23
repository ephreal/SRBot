# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import argparse


class InvalidArgumentsError(Exception):
    """Raise an InvalidArgumentsError instead of exiting the program"""
    pass


class BaseRollParser(argparse.ArgumentParser):
    """
    Base roll handler to be extended
    """
    def __init__(self):
        # Initialize the argument parser. Do NOT allow help to be auto
        # generated since it always, always, ALWAYS causes a fucking
        # sys.exit to happen. Always. Fuck that.
        super().__init__(exit_on_error=False, add_help=False)
        self.prog = "BaseRoller"
        self.add_argument("-h", "--help", action="store_true",
                          help=argparse.SUPPRESS)
        self.add_argument('dice', default=0, nargs="?", type=int,
                          help="The amount of dice to roll.")
        self.add_argument('-n', '--note', nargs="*",
                          help="Note about this roll")

    def error(self, message):
        raise InvalidArgumentsError


class Sr3RollParser(BaseRollParser):
    """
    A roll parser for SR3E
    """

    def __init__(self):
        super().__init__()
        self.prog = "Sr3Roller"
        self.add_argument("threshold", default=4, nargs="?", type=int,
                          help="The threshold the roll must meet or exceed")
        self.add_argument('-m', metavar="mod", type=int, default=0,
                          help="modifier to add to final result")
        self.add_argument("-i", default=0, nargs="?",
                          type=int, help="Initiative score to add to roll",
                          metavar="score")
        self.add_argument("-o", "--open", action="store_true",
                          help="Gets open ended test threshold")
