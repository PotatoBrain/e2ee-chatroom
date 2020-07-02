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
import os
import sys
import json
import psutil


class PreImport:
    
    def __init__(self):
        pass
    
    @staticmethod
    def kill_proc_tree(pid, including_parent=True):
        
        parent = psutil.Process(pid)
        if including_parent:
            parent.kill()
    
    def make_if_not_exists(self):
        if os.path.isfile('tor_request.py'):
            pass
        else:
            # File does not exist, create it.
            tor_request_contents = \
                """import requests
import sys


def get_request(link):
    try:
        text = requests.get(link).text
        print(text)
    except requests.exceptions.MissingSchema as e:
        print('False', e)


get_request(sys.argv[1])"""
            with open('tor_request.py', 'w') as new_tor_request:
                new_tor_request.write(tor_request_contents)
        
    
    def get_text_trough_Tor(self, link):
        with tempfile.TemporaryFile() as tempf:
            proc = subprocess.Popen(['torsocks', 'python3.8',
                                    '{}/tor_request.py'.format(os.getcwd()),
                                    '{}'.format(link),], stdout=tempf)
            proc.wait()
            tempf.seek(0)
            text = tempf.read().decode('utf-8')
        if text[:4] == 'False':
            print('There has been an error:')
            print(text[4:])
            return False
        else:
            return text
    
    def check_for_updates(self):
        try:
            import requests
        except ModuleNotFoundError:
            os.system('pip3.8 install requests[socks]')
            check_for_updates()
        # This checks if there are any new files to download, as opposed to updating them.
        site_info = self.get_text_trough_Tor("https://raw.githubusercontent.com/PotatoBrain/e2ee-chatroom/-/raw/master/scripts/client-side/client_files_list.json")
        site_downloads_list = json.loads(site_info)
        try:
            with open('client_files_list.json', 'r') as downloads_list_json:
                downloads_list = json.loads(downloads_list_json.read())
            if not site_downloads_list == downloads_list:
                with open('client_files_list.json', 'w') as new_server_files_list:
                    new_server_files_list.write(json.dumps(site_downloads_list))
                    print('Updated list of file links')
        except FileNotFoundError:
            with open('client_files_list.json', 'w') as new_server_files_list:
                new_server_files_list.write(json.dumps(site_downloads_list))
                print('Downloaded list of file links')
                
        version_file_exists = os.path.isfile('./client_version.md')
        if version_file_exists:
            with open('client_version.md', 'r') as version_file:
                current_version = version_file.read()
        else:
            current_version = 1.1
        try:
            newest_version = self.get_text_trough_Tor(
                "https://raw.githubusercontent.com/PotatoBrain/e2ee-chatroom/-/raw/master/scripts/client-side/client_version.md")
            if float(newest_version) > float(current_version):
                update = input("Update avaliable, download it? (Y?)").lower()
                if update == "y"\
                        or update == '':
                    with open('client_files_list.json', 'r') as downloads_list_json:
                        downloads_list = json.loads(downloads_list_json.read())
                    for file_name in downloads_list.keys():
                        newest_file_code = self.get_text_trough_Tor(downloads_list[file_name])
                        with open('{}'.format(file_name), 'w') as new_file:
                            new_file.write(newest_file_code)
                        print('Updated -', file_name)
                    print('Updates downloaded, please restart the program..')
                    me = os.getpid()
                    sys.exit(self.kill_proc_tree(me))
                else:
                    pass
        except requests.ConnectionError:
            pass


PreImport().check_for_updates()
restart = False
try: 
    import socks
    import errno
    import rsa
    import time
    import json
    import select
    import requests
    import threading
    from base64 import b64decode
    from base64 import b64encode
    from Crypto.Cipher import AES
    from datetime import datetime
    # from PyQt5 import QtCore, QtGui, QtWidgets
    import send_message as send_message_file
    from Crypto.Util.Padding import pad, unpad
    import receive_messages as receive_messages_file
    import generate_keys as generate_encryption_keys
    from Crypto.Util.RFC1751 import key_to_english, english_to_key
    # from PyQt5.QtWidgets import QGridLayout, QDesktopWidget, QWidget, QMessageBox, QFileDialog
    # from PyQt5.QtCore import QTimer
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
except ModuleNotFoundError:
    print('SOME PACKAGES ARE NOT INSTALLED!')
    os.system('pip3.8 install -r requirements.txt')
    print('===================== Please restart the program. =========================')
    restart = True


class Ui_MainWindow(QWidget):

    def setupUi(self, MainWindow):
        QWidget.__init__(self, parent=None)
        self.HEADER_LENGTH = 128
        self.received_privilege = "#FFFFFF"
        self.current_users = 0
        self.received_username = "Username"
        self.received_message = ""
        self.display_message = 0
        self.private_key = None
        self.public_key = None
        self.server_key = None
        self.aes_key = None
        self.aes_iv = None
        self.image = None
        self.bit_size = 4096
        self.login_register = None
        self.next_json_object = None
        self.generate_keys_thread = generate_encryption_keys.GenerateKeys()
        self.send_message_to_server_thread = send_message_file.SendMessage()
        self.receive_messages_thread = receive_messages_file.ReceiveMessage()
        self.width = int(QDesktopWidget().availableGeometry().width()/4)
        self.height = int(QDesktopWidget().availableGeometry().height()/4)
        self._translate = QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setGeometry(self.width, self.height, 800, 500)
        MainWindow.setMinimumSize(QSize(800, 500))
        MainWindow.setMaximumSize(QSize(800, 500))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QLineEdit(self.centralwidget)
        self.textEdit.hide()
        self.textEdit.setGeometry(QRect(100, 15, 541, 40))
        self.room_address_textEdit = QLineEdit(self.centralwidget)
        self.room_address_textEdit.setGeometry(QRect(70, 10, 400, 30))
        self.room_port_textEdit = QLineEdit(self.centralwidget)
        self.room_port_textEdit.setGeometry(QRect(550, 10, 120, 30))
        palette = QPalette()
        brush = QBrush(QColor(136, 138, 133))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(136, 138, 133))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.hide()
        self.pushButton.setGeometry(QRect(650, 10, 71, 51))
        self.register_or_login_button = QPushButton(self.centralwidget)
        self.register_or_login_button.setGeometry(QRect(10, 8, 110, 50))
        self.register_or_login_button.hide()
        self.generate_keys_button = QPushButton(self.centralwidget)
        self.generate_keys_button.setGeometry(QRect(10, 8, 110, 50))
        self.generate_keys_button.hide()
        self.continue_button = QPushButton(self.centralwidget)
        self.continue_button.setGeometry(QRect(10, 8, 110, 50))
        self.continue_button.hide()
        self.connect_to_server_button = QPushButton(self.centralwidget)
        self.connect_to_server_button.setGeometry(QRect(650, 10, 110, 30))
        # self.send_Image = QPushButton(self.centralwidget)
        # self.send_Image.hide()
        # self.send_Image.setGeometry(QRect(10, 35, 70, 30))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(237, 212, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(237, 212, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        brush = QBrush(QColor(190, 190, 190))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush = QBrush(QColor(237, 212, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        brush = QBrush(QColor(237, 212, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.connect_to_server_button.setPalette(palette)
        self.register_or_login_button.setPalette(palette)
        self.generate_keys_button.setPalette(palette)
        self.continue_button.setPalette(palette)
        self.pushButton.setPalette(palette)
        self.connect_to_server_button.setObjectName("connect_to_server_button")
        self.register_or_login_button.setObjectName("register_or_login_button")
        self.generate_keys_button.setObjectName("generate_keys_button")
        self.continue_button.setObjectName("continue_button")
        self.pushButton.setObjectName("pushButton")
        # self.send_Image.setPalette(palette)
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QRect(10, 30, 81, 17))
        self.label.hide()
        self.label3 = QLabel(self.centralwidget)
        self.label3.hide()
        self.label3.setGeometry(QRect(140, 13, 400, 35))
        self.label4 = QLabel(self.centralwidget)
        self.label4.hide()
        self.label4.setGeometry(QRect(730, 15, 81, 40))
        self.server_address_label = QLabel(self.centralwidget)
        self.server_address_label.setGeometry(QRect(10, 15, 81, 17))
        self.server_port_label = QLabel(self.centralwidget)
        self.server_port_label.setGeometry(QRect(500, 15, 81, 17))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(190, 190, 190))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        self.label.setPalette(palette)
        self.label.setObjectName("label")
        self.label4.setPalette(palette)
        self.label4.setObjectName("label4")
        self.server_address_label.setPalette(palette)
        self.server_address_label.setObjectName("label")
        self.server_port_label.setPalette(palette)
        self.server_port_label.setObjectName("label")
        palette = QPalette()
        brush = QBrush(QColor(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(190, 190, 190))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        self.label3.setPalette(palette)
        self.label3.setObjectName("label3")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QRect(0, 70, 800, 430))
        palette = QPalette()
        brush = QBrush(QColor(10, 10, 10))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(10, 10, 10))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        self.textBrowser.setPalette(palette)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setOpenExternalLinks(True)
        MainWindow.setCentralWidget(self.centralwidget)

        palette = QPalette()
        brush = QBrush(QColor(255, 0, 4))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 0, 4))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(184, 184, 184))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        font = QFont()
        font.setPointSize(12)
        #
        self.username_label = QLabel(self.centralwidget)
        self.username_label.setPalette(palette)
        self.username_label.setGeometry(QRect(0, 0, 101, 18))
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        #
        self.password_label = QLabel(self.centralwidget)
        self.password_label.setGeometry(QRect(0, 70, 101, 18))
        self.password_label.setPalette(palette)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        #
        palette = QPalette()
        brush = QBrush(QColor(0, 232, 54))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(0, 232, 54))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(184, 184, 184))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        self.status_label = QLabel(self.centralwidget)
        self.status_label.setGeometry(QRect(240, 52, 408, 35))
        self.status_label.setPalette(palette)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        #
        self.username_lineEdit = QLineEdit(self.centralwidget)
        self.username_lineEdit.setGeometry(QRect(30, 20, 180, 32))
        self.username_lineEdit.setObjectName("username_lineEdit")
        self.password_lineEdit = QLineEdit(self.centralwidget)
        self.password_lineEdit.setGeometry(QRect(30, 90, 180, 32))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.password_lineEdit.setEchoMode(2)
        #
        palette = QPalette()
        #brush = QBrush(QColor(234, 234, 234))
        #brush.setStyle(Qt.SolidPattern)
        #palette.setBrush(QPalette.Active, QPalette.Base, brush)
        #brush = QBrush(QColor(255, 255, 255))
        #brush.setStyle(Qt.SolidPattern)
        #palette.setBrush(QPalette.Active, QPalette.Window, brush)
        #brush = QBrush(QColor(231, 231, 231))
        #brush.setStyle(Qt.SolidPattern)
        #palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        #brush = QBrush(QColor(255, 255, 255))
        #brush.setStyle(Qt.SolidPattern)
        #palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        #brush = QBrush(QColor(255, 255, 255))
        #brush.setStyle(Qt.SolidPattern)
        #palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        #brush = QBrush(QColor(255, 255, 255))
        #brush.setStyle(Qt.SolidPattern)
        #palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        #
        # GroupBox being white was planned, but for some reason it works in the Qt 5 Designer,
        # ..but not in Python code ;-;
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(10, 140, 629, 38))  # 471
        self.groupBox.setPalette(palette)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        #
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush = QBrush(QColor(255, 0, 4))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        brush = QBrush(QColor(182, 182, 182))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        self.login_button = QPushButton(self.groupBox)
        self.login_button.setEnabled(True)
        self.login_button.setGeometry(QRect(539, 2, 88, 34))
        self.login_button.setPalette(palette)
        self.login_button.setObjectName("login_button")
        #
        self.register_button = QPushButton(self.groupBox)
        self.register_button.setEnabled(True)
        self.register_button.setGeometry(QRect(2, 2, 88, 34))
        self.register_button.setPalette(palette)
        self.register_button.setObjectName("register_button")
        #
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QRect(128, 7, 131, 22))
        self.checkBox.setObjectName("checkBox")
        self.username_lineEdit.hide()
        self.password_lineEdit.hide()
        self.register_button.hide()
        self.username_label.hide()
        self.password_label.hide()
        self.status_label.hide()
        self.login_button.hide()
        self.checkBox.hide()
        self.groupBox.hide()

        ######################################################################################
        # Generating encryption keys
        self.generate_keys_button.clicked.connect(
            self.start_generating_keys_thread)  # Starts generating keys, now the main window can respond
        #    while doing that xD
        self.generate_keys_thread.output.connect(
            self.receive_generated_keys)  # Receive the generated keys.
        
        # Sending messages
        self.pushButton.clicked.connect(self.start_sending_messages_thread)  # Send a message to the Server
        self.send_message_to_server_thread.output.connect(
            self.send_message_to_server_update_variables)  # Update a few variables
        self.send_message_to_server_thread.finished.connect(
            self.send_message_to_server_update_Ui)  # Enable the button again?

        # Receiving messages
        self.receive_messages_thread.output.connect(
            self.receive_messages_update_variables)  # Update a few variables.
        ######################################################################################
        # This above started a few threads so the code doesn't block the main gui loop.

        self.register_or_login_button.clicked.connect(self.change_to_login)
        self.connect_to_server_button.clicked.connect(self.connect_to_server)
        self.continue_button.clicked.connect(self.hide_login_section)
        
        self.for_some_reason_this_works = MainWindow
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)        
        
    def change_to_login(self):
        self.register_or_login_button.hide()
        self.textBrowser.hide()
        self.label3.hide()
        current_coords = self.for_some_reason_this_works.pos()
        self.for_some_reason_this_works.setGeometry(current_coords.x(), current_coords.y(), 650, 180)
        self.for_some_reason_this_works.setMinimumSize(QSize(650, 180))
        self.for_some_reason_this_works.setMaximumSize(QSize(650, 180))
        self.username_lineEdit.show()
        self.password_lineEdit.show()
        self.register_button.show()
        self.username_label.show()
        self.password_label.show()
        self.status_label.show()
        self.login_button.show()
        self.checkBox.show()
        self.groupBox.show()
        self.checkBox.clicked.connect(self.change_checkbox)  # Show/hide the password
        self.register_button.clicked.connect(self.send_register_info)
        self.login_button.clicked.connect(self.send_login_info)

    def send_register_info(self):
        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)
        self.login_username = self.username_lineEdit.text()
        self.login_password = self.password_lineEdit.text()
        self.login_register = 'register'
        self.handle_client()
        
    def send_login_info(self):
        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)
        self.login_username = self.username_lineEdit.text()
        self.login_password = self.password_lineEdit.text()
        self.login_register = 'login'
        self.handle_client()
        
    def change_checkbox(self):
        if self.checkBox.isChecked():
            self.password_lineEdit.setEchoMode(0)
        else:
            self.password_lineEdit.setEchoMode(2)

    def start_generating_keys_thread(self):
        self.generate_keys_button.setEnabled(False)
        self.label3.show()
        palette = QPalette()
        brush = QBrush(QColor(2, 201, 16))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(2, 201, 16))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(190, 190, 190))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        self.label3.setPalette(palette)
        self.label3.show()

        print('Starting generating encryption keys, this may take up to a minute, depending on your hardware.')
        self.generate_keys_thread.start_generating_keys()
        
    def receive_generated_keys(self, *args):
        (self.aes_key, self.public_key, self.private_key) = args
        print('Keys generated.')
        self.label3.setText(self._translate("MainWindow", "Keys generated, please\n login/register now."))
        self.generate_keys_button.hide()
        self.register_or_login_button.show()

    def start_receiving_messages_thread(self):
        self.receive_messages_thread.start_receiving_messages(
            self.HEADER_LENGTH,
            self.server_socket,
            self.textBrowser,
            self.pushButton,
            self.label4,
            self.decrypt_json_object)

    def receive_messages_update_variables(self, *args):
        (self.textBrowser, color_code, username, text) = args
        self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD    HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
            f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:{color_code}; \">{username}<font style=\" color:#FFFFFF;\"> >  {text}</font></p></body></html>\n")
        self.textBrowser.moveCursor(QTextCursor.End)

    def start_sending_messages_thread(self):
        self.pushButton.setEnabled(False)
        self.send_message_to_server_thread.start_sending_the_message(
            self.HEADER_LENGTH,
            self.server_socket,
            self.textEdit,
            self.encrypt_a_message)

    def send_message_to_server_update_variables(self, *args):
        (clear_browser, self.textEdit) = args
        if clear_browser:
            self.textBrowser.clear()
            self.textEdit.setText("")

    def send_message_to_server_update_Ui(self):
        self.pushButton.setEnabled(True)        

    def show_login_section(self):
        self.server_address_label.hide()
        self.server_port_label.hide()
        self.room_address_textEdit.hide()
        self.room_port_textEdit.hide()
        self.connect_to_server_button.hide()
        self.generate_keys_button.show()

    def connect_to_server(self, just_connect=False):
        if not just_connect:
            self.IP = self.room_address_textEdit.text()
            self.PORT = self.room_port_textEdit.text()
            if not self.PORT:
                self.PORT = 80

        # Create a socket
        self.server_socket = socks.socksocket()
        self.server_socket.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

        # Connect to a given ip and port
        try:
            self.server_socket.connect((self.IP, self.PORT))

            # Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
            # self.server_socket.setblocking(False)

            if not just_connect:
                room_info_please = f"INFO-PLS".encode('utf-8')
                room_info_please_header = f"{len(room_info_please):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.server_socket.send(room_info_please_header + room_info_please)
                received_info = self.loop().decode('utf-8')
                print(received_info)

                self.retry_json(received_info)
                self.room_info = self.next_json_object
                room_encryption_size = self.room_info['BIT_SIZE']
                room_name = self.room_info['ROOM_NAME']
                room_rules = self.room_info['ROOM_RULES']
                required_client_version = self.room_info['CLIENT_REQUIRED']
                with open('client_version.md', 'r') as version_file:
                    current_client_version = version_file.read()
                version_ok = float(required_client_version) == float(current_client_version)
                if version_ok:
                    version_status = 'GOOD, v{}.'.format(current_client_version)
                    color_code = "#00ff35"
                else:
                    version_status = "Your client version is {0}, and the required client version for this room is {1}. Consider updating your client!".format(current_client_version, required_client_version)
                    color_code = "#FF0000"
                

                self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#FF0000; \">ROOM NAME: <font style=\" color:#FFFFFF; \">{room_name}</font></p>\n")
                self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#FF0000; \">ROOM ADDRESS: <font style=\" color:#FFFFFF; \">{self.IP}</font></p>\n")
                self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#FF0000; \">ROOM PORT: <font style=\" color:#FFFFFF; \">{self.PORT}</font></p>\n")
                self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#FF0000; \">ROOM ENCRYPTION: <font style=\" color:#FFFFFF; \">RSA-{room_encryption_size}</font></p>\n")
                self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#FF0000; \">ROOM RULES: <font style=\" color:#FFFFFF; \">{room_rules}</font></p>\n")
                self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#FF0000; \">CLIENT VERSION: <font style=\" color:{color_code}; \">{version_status}</font></p>\n")
                self.show_login_section()
        except socks.GeneralProxyError:
            self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Room is either offline or doesn't exist..</p></body></html>\n")
        except socks.ProxyConnectionError:
            self.show_popup()

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText("Error: You do not have Tor(network) running.")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry)
        # TODO Start Tor automatically. How on Windows?
        msg.setDetailedText(
            "On Linux you can say in terminal:\n"
            "tor & nohup\n"
            "You can close that window and retry.")
        x = msg.exec_()

    def receive_a_message(self):
        message_header = self.server_socket.recv(self.HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = self.server_socket.recv(message_length)
        return message

    def receive_messages(self):
        # Moved to the receive_messages.py
        pass

    def loop(self, key=False):
        while True:
            try:
                display_message_header = self.server_socket.recv(self.HEADER_LENGTH)
                display_message_length = int(display_message_header.decode('utf-8').strip())
                if key:
                    received_message = self.server_socket.recv(display_message_length)
                    display_message = rsa.key.PublicKey.load_pkcs1(received_message, format='DER')
                else:
                    received_message = self.server_socket.recv(display_message_length)
                    display_message = received_message
                return display_message
            except:
                pass

    def hide_login_section(self):
        # Hide the login part because it is not needed anymore.  
        self.label.show()        
        self.label3.hide()
        self.continue_button.hide()
        # self.send_Image.show()
        self.textEdit.show()
        self.pushButton.show()
        self.label4.setText(f"Users:\n{self.current_users}")
        self.label4.show()
        
        self.textBrowser.setHtml(self._translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Type /help to get a list of commands. Please report any bugs.</p></body></html>\n"))

        #  This will be receiving new messages for us in another thread, so that we can have a True loop and not block the receiving.

        self.start_receiving_messages_thread()

    def handle_client(self):
        self.display_message = None
        display_message = None
        self.connect_to_server(True)

        # Send my public key.
        public_key_header = f"{len(str(self.public_key)):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.server_socket.send(public_key_header + self.public_key.save_pkcs1(format='DER'))

        # Receive the server's public key.
        self.server_key = self.loop(True)
        print('server public key is: ', self.server_key)
        aes_key_to_go = key_to_english(self.aes_key)
        print('aes_key_to_go --- ', aes_key_to_go)
        username_password = self.encrypt_json_object(dictionary=
            {"login_register": self.login_register, "username": self.login_username, "password": self.login_password, "aes_key": aes_key_to_go})

        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username_password_header = f"{len(username_password):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.server_socket.send(username_password_header + username_password)
        # Receive an answer if we are logged in or nah.
        answer = self.decrypt_json_object(encrytped_json_object=self.loop())
        display_message = answer['login_status']
        self.current_users = answer['users']
        self.id_identifier = answer['id_identifier']

        if display_message == "1":
            self.status_label.setText(self._translate("MainWindow", "Username or Password are empty"))
            self.allowed_or_not(False)
        elif display_message == "2":
            self.status_label.setText(self._translate("MainWindow", "Please no SQL injections :)"))
            self.allowed_or_not(False)
        elif display_message == "3":
            self.status_label.setText(self._translate("MainWindow", "Account Created"))
            self.allowed_or_not(True)
        elif display_message == "4":
            self.status_label.setText(self._translate("MainWindow", "Correct Password"))
            self.allowed_or_not(True)
        elif display_message == "5":
            self.status_label.setText(self._translate("MainWindow", "Wrong Password"))
            self.allowed_or_not(False)
        elif display_message == "6":
            self.status_label.setText(self._translate("MainWindow", "Use normal characters or numbers,please"))
            self.allowed_or_not(False)
        elif display_message == "7":
            self.status_label.setText(self._translate("MainWindow", "Max username characters: 10"))
            self.allowed_or_not(False)
        elif display_message == "8":
            self.status_label.setText(self._translate("MainWindow", "Max password characters: 30"))
            self.allowed_or_not(False)
        elif display_message == "9":
            self.status_label.setText(self._translate("MainWindow", "You have been banned."))
            self.allowed_or_not(False)
        elif display_message == "10":
            self.status_label.setText(self._translate("MainWindow", "User is already registered."))
            self.allowed_or_not(False)
        elif display_message == "11":
            self.status_label.setText(self._translate("MainWindow", "User does not exist."))
            self.allowed_or_not(False)
        
        print(display_message)
        self.display_message = display_message
        if self.display_message == "3" or self.display_message == "4":
            self.label3.setText(self._translate("MainWindow", self.status_label.text()))
            self.label.setText(self.login_username)
            print(self.status_label.text())
            self.label3.show()
            self.username_lineEdit.hide()
            self.password_lineEdit.hide()
            self.register_button.hide()
            self.username_label.hide()
            self.password_label.hide()
            self.status_label.hide()
            self.login_button.hide()
            self.checkBox.hide()
            self.groupBox.hide()
            current_coords = self.for_some_reason_this_works.pos()
            self.for_some_reason_this_works.setGeometry(current_coords.x(), current_coords.y(), 800, 500)
            self.for_some_reason_this_works.setMinimumSize(QSize(800, 500))
            self.for_some_reason_this_works.setMaximumSize(QSize(800, 500))
            self.textBrowser.show()
            
            self.register_or_login_button.hide()
            self.continue_button.show()

    def encrypt_a_message(self, *, message):
        try:
            encrypted_message = rsa.encrypt(message, self.server_key)
            return encrypted_message
        except OverflowError:
            self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Too long message. Try again.</p></body></html>\n")
            return False

    def aes_encrypt_data(self, *, data):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv)
        ct = b64encode(ct_bytes)
        return self.encrypt_a_message(message=iv), ct

    def encrypt_json_object(self, *, dictionary):
        json_object = json.dumps(dictionary).encode('utf-8')
        return self.encrypt_a_message(message=json_object)

    def decrypt_a_message(self, *, encrypted_message):
        data = rsa.decrypt(encrypted_message, self.private_key)
        if type(data) is str:
            return data
        else:
            return data.decode()

    def decrypt_json_object(self, *, encrytped_json_object):
        try:
            json_object = self.decrypt_a_message(encrypted_message=encrytped_json_object)
            self.retry_json(json_object)
            return self.next_json_object
        except rsa.pkcs1.DecryptionError:
            return "FAILED"

    def decrypt_aes_data(self, iv, *, ciphertext):
        iv = b64decode(iv)
        ciphertext = b64decode(ciphertext)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
        print('decrypted image: ', data)
        return data

    def retry_json(self, received_info):
        try:
            self.next_json_object = json.loads(received_info)

            # I've encountered a error code that I can not exaplain, but have found a solution around it.
            # If you know a solution to it, I would be glad to hear it. The error code appears when we try
            # to load a json object - that is somehow {DICTIONARY}399 (or sometimes 433) - it appears
            # to be added to the dictionary object on it's way from the server to the client and the other
            # way around - it may be a Tor thingie, I am not sure. The error code:
            #
            # {"BIT_SIZE": 4096, "ROOM_NAME": "The official project room", "ROOM_RULES": "Be nice :)"}399
            # Traceback (most recent call last):
            #     File "client.py", line 341, in connect_to_server
            #         self.room_info = json.loads(received_info)
            #     File "/usr/lib/python3.8/json/__init__.py", line 357, in loads
            #         return _default_decoder.decode(s)
            #     File "/usr/lib/python3.8/json/decoder.py", line 340, in decode
            #         raise JSONDecodeError("Extra data", s, end)
            # json.decoder.JSONDecodeError: Extra data: line 1 column 89 (char 88)
            # Aborted
            #
            # For now I just remove those 3 last numbers and it works.

        except ValueError:
            print(received_info)
            new_json_object = received_info[:-3]
            self.retry_json(new_json_object)

    @staticmethod
    def get_palette(color):
        if color == 'green':
            palette = QPalette()
            brush = QBrush(QColor(2, 201, 16))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
            brush = QBrush(QColor(2, 201, 16))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
            brush = QBrush(QColor(190, 190, 190))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        elif color == 'red':
            palette = QPalette()
            brush = QBrush(QColor(255, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
            brush = QBrush(QColor(255, 0, 0))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
            brush = QBrush(QColor(190, 190, 190))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        return palette
    
    def allowed_or_not(self, allowed):
        if allowed:
            palette = self.get_palette('green')
            self.status_label.setPalette(palette)
            self.status_label.show()
        else:
            palette = self.get_palette('red')
            self.status_label.setPalette(palette)
            self.status_label.show()
            self.login_button.setEnabled(True)
            self.register_button.setEnabled(True)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(self._translate("MainWindow", "Chat"))
        self.pushButton.setText(self._translate("MainWindow", "Send"))
        self.pushButton.setShortcut(self._translate("MainWindow", "Return"))
        self.register_or_login_button.setText(self._translate("MainWindow", "Register/Login"))
        self.register_or_login_button.setShortcut(self._translate("MainWindow", "Return"))
        self.generate_keys_button.setText(self._translate("MainWindow", "Generate keys"))
        self.generate_keys_button.setShortcut(self._translate("MainWindow", "Return"))
        self.continue_button.setText(self._translate("MainWindow", "Continue"))
        self.continue_button.setShortcut(self._translate("MainWindow", "Return"))
        self.connect_to_server_button.setText(self._translate("MainWindow", "Connect"))
        self.connect_to_server_button.setShortcut(self._translate("MainWindow", "Return"))
        # self.send_Image.setText(self._translate("MainWindow", "Image"))
        self.label3.setText(self._translate("MainWindow", "Generating encryption keys, please wait :)"))
        self.label4.setText(self._translate("MainWindow", "Users: 1"))
        self.server_address_label.setText(self._translate("MainWindow", "Address:"))
        self.server_port_label.setText(self._translate("MainWindow", "Port:"))
        #
        self.username_lineEdit.setPlaceholderText(self._translate("MainWindow", "Max 10 characters"))
        self.password_lineEdit.setPlaceholderText(self._translate("MainWindow", "Max 15 characters"))
        self.username_label.setText(self._translate("MainWindow", "Username:"))
        self.password_label.setText(self._translate("MainWindow", "Password:"))
        self.status_label.setText(self._translate("MainWindow", "Status:"))
        self.login_button.setText(self._translate("MainWindow", "Login"))
        self.register_button.setText(self._translate("MainWindow", "Register"))
        self.checkBox.setText(self._translate("MainWindow", "Show password"))


def main():
    os.system('PS1=$\nPROMPT_COMMAND=\necho -en "\033]0;Client\a"; clear')
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    me = os.getpid()
    sys.exit(PreImport.kill_proc_tree(me))


if __name__ == "__main__":
    __author__ = "PotatoBrain"
    try:
        if not restart:
            main()
    except KeyboardInterrupt:
        print("Program has exited because of keyboard interruption.")
