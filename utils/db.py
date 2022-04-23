# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

import sqlite3


class DBHandler():
    def __init__(self, db="shadowrun.db"):
        self.db = db
        self.connection = sqlite3.connect(self.db)
        self.rolling = RollingDB(self.connection)


class RollingDB():
    def __init__(self, connection):
        self.connection = connection

    def get_last_roll(self, userid):
        """
        Searches the database to get the last roll by this user. If no roll
        exists, returns None.

        Parameters:
            userid: int

        Returns:
            [roll] or None
        """

        cur = self.conn.cursor()

        cur.execute("""
        SELECT roll from rolls where userid = ?
        """, (userid,))

        self.connection.commit()
        cur = cur.fetchall()

        return cur[0][0]

    def save_roll(self, userid, roll, threshold):
        """
        Saves the roll and the threshold information to the datavase.

        Parameters:
            userid: int
            roll: [int, int, ..., int]
            threshold: int

        Return:
            None
        """

        cur = self.conn.cursor()

        roll = str(roll)

        cur.execute("""
        insert or ignore into rolls (roll, threshold) values (?, ?)
        """, (roll, threshold,))

        self.connection.commit()
