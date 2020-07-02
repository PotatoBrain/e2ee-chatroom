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
import json


def return_or_write_config(new_config=None):
	if new_config is None:
		read_write = 'r'
	else:
		read_write = 'w'
	with open('server_config.json', read_write) as myfile:
		if new_config is None:
			data = myfile.read()
			return json.loads(data)
		else:
			data = myfile.write(json.dumps(new_config))


def update_config(database_name, table_name):
	current_dict = return_or_write_config()
	current_dict['database_name'] = database_name
	current_dict['table_name'] = table_name
	return_or_write_config(current_dict)
