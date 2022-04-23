# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/rollbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from utils.db.migrations.abc import abc_migration


class Migration(abc_migration.Migration):
    def __init__(self, db="shadowrun.db"):
        super().__init__(db)
        self.version = 0
        self.description = "Initial configuration of the database"
        self.breaks = "Downgrading from this version breaks everything."

    def migrate(self):
        """
        Creates 3 tables: commands, greeting, and tags
        """

        cursor = self.connection.cursor()

        rolls = '''CREATE TABLE if not exists rolls (
                   userid INTEGER primary key not null unique,
                   roll TEXT,
                   threshold integer default 4,
                   unique(userid)
                   )'''

        reference = '''CREATE TABLE if not exists reference (
                       id integer primary key autoincrement not null,
                       name TEXT,
                       data TEXT default null
                       )'''

        tags = '''CREATE TABLE if not exists tags (
                        id integer primary key autoincrement not null,
                        user_id varchar(30),
                        tag varchar(100),
                        content varchar(2000),
                        unique(tag)
                        )'''

        version = '''create table if not exists db_versions (
                     db varchar (64),
                     version integer,
                     unique(db)
                     )'''

        cursor.execute(rolls)
        cursor.execute(reference)
        cursor.execute(tags)
        cursor.execute(version)
        self.connection.commit()

        self.upgrade_table_version("rolls")
        self.upgrade_table_version("reference")
        self.upgrade_table_version("tags")
        self.upgrade_table_version("schema")
        self.upgrade_table_version("version")

        self.migrated = True

    def revert(self):
        """
        Removes the tables
        """

        if not self.revert_requisites():
            raise ValueError

        commands = "drop table rolls"
        greetings = "drop table reference"
        tags = "drop table tags"
        db = "drop table db_versions"
        cursor = self.connection.cursor()

        cursor.execute(commands)
        cursor.execute(greetings)
        cursor.execute(tags)
        cursor.execute(db)

        self.connection.commit()

        self.migrated = False

    def revert_requisites(self):
        """
        Returns True if the database version for any table is > 0
        """

        if self.get_version("rolls") > 0:
            return False

        if self.get_version("reference") > 0:
            return False

        if self.get_version("tags") > 0:
            return False

        if self.get_version("db_versions") > 0:
            return False

    def requisites(self):
        """
        Always returns True. This migration is always safe to apply.
        """
        return True
