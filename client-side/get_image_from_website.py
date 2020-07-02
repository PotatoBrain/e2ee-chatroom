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
import requests
import base64
import sys


def prepare_html(image_dir=False, link=False, img_tag=''):
    if image_dir != '0':
        image = open(image_dir, 'rb').read()
    elif link != '0':
        img_tag = '<a href="{0}">'.format(link)
        image = requests.get(link).content

    data_uri = base64.b64encode(image).decode('utf-8')
    img_tag += '<img src="data:image/png;base64,{0}" width="400" height="250">'.format(data_uri)
    print(img_tag)


prepare_html(sys.argv[1], sys.argv[2])
