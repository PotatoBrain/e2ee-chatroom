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
import sqlite3
import hash_password
import get_settings


def insert_user(db_name, table_name, username, password):
    hash_password_dict = hash_password.hash_the_password(password)
    created_password = hash_password_dict['password']
    salt = hash_password_dict['salt']
    with sqlite3.connect("./databases/{}.db".format(db_name)) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO {}(username, hashed_password, salt, power_level, banned) "
                       "VALUES(?, ?, ?, ?, ?)".format(table_name), (username, created_password, salt, '0', 0))

