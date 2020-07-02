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
from Crypto.Random import get_random_bytes
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import multiprocessing
import rsa


class GenerateKeys(QThread):
    print('1')
    output = pyqtSignal(bytes, rsa.key.PublicKey, rsa.key.PrivateKey)
    print('2')

    def __init__(self, parent=None):
        # super().__init__(self, parent)
        QThread.__init__(self, parent)
        self.exiting = False
        self.bit_size = 4096
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

    def start_generating_keys(self, *args):
        print('6')
        self.start()

    def run(self):
        aes_key = get_random_bytes(32)  # for AES256 encryption.
        (public_key, private_key) = rsa.newkeys(self.bit_size, poolsize=multiprocessing.cpu_count())
        self.output.emit(aes_key, public_key, private_key)
        
