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
import time
import sys
import cv2
import os


def prepare_html(image_dir=False, link=False, img_tag='', only_link=False):
    image_width = 0
    if image_dir != '0':
        image = open(image_dir, 'rb').read()
    elif link != '0':
        img_tag = '<a href="{0}">'.format(link)
        image = requests.get(link).content

    # Basically make a new file, store the new image in that file and get the image's size, so we can scale it down
    # if it's too big for the chatroom. Deletes it afterwards.
    if int(only_link):
        img_tag += '{}'.format(link)
    else:
        if link:
            def wait_more():
                time.sleep(0.5)
                with open('temp_img.jpg', 'wb') as temp_img:
                    image = requests.get(link).content
                    temp_img.write(image)
                
            wait_more()
            try:
                image_height, image_width, _ = cv2.imread('temp_img.jpg').shape
                os.remove('temp_img.jpg')
            except (FileNotFoundError, AttributeError):
                wait_more()
                
        data_uri = base64.b64encode(image).decode('utf-8')
        if image_width > 800:
            img_tag += '<img src="data:image/png;base64,{0}" width="610" height="400">'.format(data_uri)  
        else:
            img_tag += '<img src="data:image/png;base64,{0}"'.format(data_uri)  
    print(img_tag)

prepare_html(image_dir=sys.argv[1], link=sys.argv[2], only_link=sys.argv[3])


