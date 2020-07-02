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


class SendMessage(QThread):
    print('1')
    output = pyqtSignal(bool, QLineEdit)
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

    def start_sending_the_message(self, *args):
        (
            self.HEADER_LENGTH, 
            self.server_socket, 
            self.textEdit, 
            self.encrypt_a_message
        ) = args
        print('6')
        self.start()

    def run(self):
        print('7')
        message = self.textEdit.text()
        if message == '/clear':
            # self.textBrowser.clear()
            # self.textEdit.setText("")
            # We will do this afterwards.. for some reason I get this error I do not understand:
            #   QObject: Cannot create children for a parent that is in a different thread.
            #   (Parent is QTextDocument(0x242f5b0), parent's thread is QThread(0x1fa6a30), current thread is SendMessage(0x23009e0)
            #   Segmentation fault (core dumped)
            self.output.emit(True,
                             self.textEdit)
        else:
            print('8')
            message = message.encode('utf-8')
            encrypted_message = self.encrypt_a_message(message=message)
            print('9')
            # If message is not empty - send it
            if message and encrypted_message and not self.exiting:
                print('10')
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                message_header = f"{len(str(encrypted_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.server_socket.send(message_header + encrypted_message)
                print('11')
                self.textEdit.setText("")
                # Update the 2 variables.
                self.output.emit(False,
                                 self.textEdit)
