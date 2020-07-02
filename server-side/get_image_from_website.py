import requests
import base64
import sys


def prepare_html(image_dir=False, link=False, img_tag=''):
    try:
        if image_dir != '0':
            pass
        elif link != '0':
            image = requests.get(link).content
    except requests.exceptions.MissingSchema:
        print('False')

prepare_html(sys.argv[1], sys.argv[2])
