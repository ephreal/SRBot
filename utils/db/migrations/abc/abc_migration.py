# -*- coding: utf-8 -*-
"""
This software is licensed under the License (MIT) located at
https://github.com/ephreal/srbot/Licence

Please see the license for any restrictions or rights granted to you by the
License.
"""

from abc import ABC
import sqlite3
from sqlite3 import OperationalError


class Migration(ABC):
    def __init__(self, db="shadowrun.db"):
        self.version = None
        self.connection = sqlite3.connect(db)
        self.description = "This is the abstract base class"
        self.breaks = "These changes break no functionality"

        if self.get_schema_version() == self.version:
            self.migrated = True
        else:
            self.migrated = False

    def migrate(self):
        """
        Applies a migration to the database
        """
        pass

    def revert(self):
        """
        Reverts changes done by this migration
        """
        pass

    def requisites(self):
        """
        This must return true for the migration to run.
        """
        pass

    def revert_requisites(self):
        """
        This must return True for the database revert to run
        """
        pass

    def upgrade_table_version(self, table):
        """
        Increments the version of the table specified
        """

        cursor = self.connection.cursor()
        try:
            cursor.execute("select version from db_versions where db=?",
                           (table,))
            version = cursor.fetchall()[0][0]
            version += 1
            cursor.execute("""update db_versions set version = ?
                           where db = ?""", (version, table,))
        except IndexError:
            version = 0
            cursor.execute("""insert into db_versions (db,version) values
                           (?, 0)""", (table,))

        self.connection.commit()

    def downgrade_table_version(self, table):
        """
        Decrements the version of the table specified
        """

        cursor = self.connection.cursor()
        try:
            cursor.execute("select version from db_versions where db=?",
                           (table, ))
            version = cursor.fetchall()[0][0]
            version -= 1

            if version < 0:
                # The table is slated for removal, remove the version from the
                # db_versions table now

                cursor.execute("delete from db_versions where db=?", (table, ))
            else:
                cursor.execute("""update db_versions set version = ?
                               where db=?""", (version, table, ))

        except IndexError:
            pass

    def get_schema_version(self):
        """Returns the current schema version of the database"""

        cursor = self.connection.cursor()
        sql = """select version from db_versions where db='schema'"""

        try:
            cursor.execute(sql)
            version = cursor.fetchall()[0][0]
        except sqlite3.OperationalError:
            version = -1
        except IndexError:
            version = -1

        return version

    def get_version(self, table):
        """
        Returns the current version of the passed in table.
        """

        cursor = self.connection.cursor()
        sql = """select version from db_verisons where db='?'"""

        try:
            cursor.execute(sql, (table,))
            version = cursor.fetchall()[0][0]
        except sqlite3.OperationalError:
            version = -1
        except IndexError:
            version = -1

        return version

    def failed_migration_pending(self, tables):
        if not self.get_schema_version() == self.version:
            return

        cursor = self.connection.cursor()

        for table in tables:
            try:
                sql = f"select * from {table} where id=1"
                cursor.execute(sql)
            except OperationalError:
                return True
        return False
