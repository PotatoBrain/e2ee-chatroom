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
import time
import sys


class SendMessage(QThread):
    output = pyqtSignal(bool, QLineEdit, bool, int)

    def __init__(self, parent=None):
        # super().__init__(self, parent)
        QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        try:
            self.wait()
        except RuntimeError:
            # Can't exit - class already finished.
            pass

    def start_sending_the_message(self, *args):
        (
            self.HEADER_LENGTH, 
            self.server_socket, 
            self.textEdit,
            self.max_chars,
            self.encrypt_a_message,
            self.aes_encrypt_data
        ) = args
        self.start()

    def run(self):
        message = self.textEdit.text()
        message_size = sys.getsizeof(message)-49
        if message == '/clear':
            self.output.emit(True,
                             self.textEdit,
                             False,
                             0)
        elif message_size > self.max_chars:
            self.output.emit(False,
                             self.textEdit,
                             True,
                             message_size)
        else:
            message = message.encode('utf-8')
            RSA_encrypted_initialization_vector, encrypted_message = self.aes_encrypt_data(data=message)
            # If message is not empty - send it
            if message and RSA_encrypted_initialization_vector and encrypted_message and not self.exiting:
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message_header = f"{len(str(RSA_encrypted_initialization_vector)):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.server_socket.send(message_header + RSA_encrypted_initialization_vector)
                time.sleep(0.5)
                message_header = f"{len(str(encrypted_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.server_socket.send(message_header + encrypted_message)
                self.textEdit.setText("")
                # Update the 2 variables.
                self.output.emit(False,
                                self.textEdit, 
                                False,
                                0)

