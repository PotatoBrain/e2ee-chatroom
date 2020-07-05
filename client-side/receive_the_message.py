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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import subprocess
import tempfile
import os


class ReceiveMessage(QThread):
    output = pyqtSignal(str, int, str, str, bool)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        
    def __del__(self):
        self.exiting = True
        try:
            self.wait()
        except RuntimeError:
            # Can't exiit - class already finished.
            pass
    
    def start_receiving_the_message(self, *args):
        # Receive the arguments.
        (self.is_image,
         self.show_images,
         self.received_privilege, 
         self.current_users, 
         self.received_username,
         self.image_link) = args
        self.start()
        
    @staticmethod
    def get_image_type(tempf, image_dir, image_link, only_link):
        proc = subprocess.Popen(['torsocks', 'python3.8',
                                        '{}/get_image_from_website.py'.format(os.getcwd()),
                                        '{}'.format(image_dir), '{}'.format(image_link),
                                        '{}'.format(only_link)], stdout=tempf)
        return proc

    def get_image(self, image_link):
        print('in get_image.')
        # Get the image data from the provided link
        with tempfile.TemporaryFile() as tempf:
            if self.show_images:
                proc = self.get_image_type(tempf=tempf,
                                           image_dir=0, 
                                           image_link=image_link, 
                                           only_link=0)
            else:
                proc = self.get_image_type(tempf=tempf,
                                           image_dir=0, 
                                           image_link=image_link, 
                                           only_link=1)
            proc.wait()
            tempf.seek(0)
            image_html = tempf.read().decode('utf-8')
        return image_html
        
    def run(self):
        image_html = self.get_image(image_link=self.image_link)
        
        self.output.emit(self.received_privilege, self.current_users, self.received_username, image_html, self.is_image)
        
