"""
Copyright (C) 2020 PotatoBrain <icannotcomeupwithanemail@protonmail.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import update_settings
import sqlite3
import random
import string
import os


def randomString(stringLength=100):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_database():
    db_name = randomString()
    table_name = randomString()
    database_folder = os.path.isdir('./databases')
    if not database_folder:
        os.mkdir('./databases')
    with sqlite3.connect("./databases/{}.db".format(db_name)) as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE {} (
        "id"				    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "username"			    TEXT NOT NULL UNIQUE,
        "hashed_password"	    BLOB NOT NULL,
        "salt"          	    BLOB NOT NULL,
        "power_level"           TEXT,
        "banned"                INTEGER
        )""".format(table_name))

    update_settings.update_config(database_name=db_name,
                                  table_name=table_name)
