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
from PyQt5.QtGui import *
import rsa
import sys
import os


class EncryptMessage(QThread):
    print('1')
    output = pyqtSignal(bool, bytes)
    print('2')

    def __init__(self, parent=None):
        # super().__init__(self, parent)
        QThread.__init__(self, parent)
        self.exiting = False
        print('3')

    def __del__(self):
        self.exiting = True
        print('4')
        try:
            self.wait()
        except RuntimeError:
            print('5')
            # Can't exit - class already finished.
            pass

    def start_encrypting(self, *args):
        (
            self.server_key,
            self.message
        ) = args
        print('6')
        self.start()

    def run(self): 
        with open('over_head.txt', 'r') as read_over_head:
                over_head = bytes(int(read_over_head.read()))
        print(sys.getsizeof(over_head))
        print(sys.getsizeof(self.message+over_head))
        if int(sys.getsizeof(self.message+over_head)) > 501:
            self.output.emit(False, b'0')
        else:
            # Make sure that the server can send our message with additional information such as the current number of users
            # in the chatroom, the color code and the sender's username.
            # color code = 56 bytes, users = 28 bytes, username = 59 bytes. Alltogether = 143 bytes.
            #random_bytes = os.urandom(110)  # For some reason 110 gives us exactly 143 bytes of head-room.
            encrypted_message = rsa.encrypt(self.message, self.server_key)
            print('it actually does get past this.')
            self.output.emit(True, encrypted_message)
