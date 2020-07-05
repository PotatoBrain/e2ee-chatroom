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
from Crypto.Util.RFC1751 import key_to_english, english_to_key
import receive_the_message as receive_the_message_file
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import psutil
import select
import errno
import socks
import json
import time
import rsa
import sys
import os


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


class ReceiveMessage(QThread):
    output = pyqtSignal(QTextBrowser, str, str, str, bool, socks.socksocket, rsa.key.PublicKey, object)   # Don't forget to type in the output types

    def __init__(self, parent=None):
        # super().__init__(self, parent)
        QThread.__init__(self, parent)
        self.receive_the_message_thread = receive_the_message_file.ReceiveMessage()
        self.receive_the_message_thread.output.connect(
            self.get_message_contents)
        self.exiting = False
        self.is_image = False

    def __del__(self):
        self.exiting = True
        try:
            self.wait()
        except RuntimeError:
            # Can't exit - class already finished.
            pass

    def start_receiving_messages(self, *args):
        # Receive the arguments.
        (
            self.HEADER_LENGTH,
            self.server_socket,
            self.IP,
            self.PORT,
            self.login_username,
            self.login_password,
            self.show_images,
            self.aes_key,
            self.public_key,
            self.server_key,
            self.server_aes_key,
            self.textBrowser,
            self.pushButton,
            self.label4,
            self.decrypt_aes_data,
            self.decrypt_a_message,
            self.decrypt_json_object
        ) = args
        print('6')
        self.start()

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

    def encrypt_json_object(self, *, dictionary):
        json_object = json.dumps(dictionary).encode('utf-8')
        return self.encrypt_a_message(message=json_object)

    def send_message_to_textBrowser(self):
        username = f"{datetime.now().strftime('%H:%M')} {self.received_username}"
        self.label4.setText(f"Users:\n{self.current_users}")
        color_code = self.received_privilege
        text = self.received_message
        is_link = True
        # This next piece of code basically turns something like [youtube.com] into a [youtube.com] clickable link,
        # Unfortunately also all of the { and } into [ and ].. hopefully I'll find a way around this in the future,
        # for not focused on more important features.
        if not self.is_image:
            try:
                while True:
                    is_www = False
                    # going_for += 1             
                    letters = list(text)
                    start_link = letters.index("[")
                    end_link = letters.index("]")
                    letters[start_link] = "{"
                    letters[end_link] = "}"
                    before_link = text.split(text[start_link], 1)[0] + "{"
                    after_link = "}" + text.split(text[end_link], 1)[1]
                    text = "".join(letters)
                    link = text[start_link:end_link].strip("{")
                    if link.startswith("https://www"):
                        is_www = True
                    elif link.startswith("http://www"):
                        is_www = True
                    elif link.startswith("https://"):
                        pass
                    elif link.startswith("http://"):
                        after_http = link.split("http://")[1]
                        link = f"https://{after_http}"
                    elif link.startswith("www"):
                        link = f"https://{link}"
                        is_www = True
                    else:
                        link = f"https://{link}"
                    if is_www:
                        after_www = link.split("www.")[1]
                        website = after_www.split(".")[0]
                    else:
                        after_https = link.split("https://")[1].strip()
                        website = after_https.split(".")[0]
                        if after_https == website:
                            # For some reason even if there's not a '.', the website is equal to after_https which means that the given link
                            # does not end with anything (examples '.com', '.ord', etc.)
                            # This means that people can send regular tags such as "[SPOILER]" and then a link such as "[https://some-spoiler.com]"(made up)
                            is_link = False
                        else:
                            is_link = True
                    if is_link:
                        text = before_link +  f"<a href=\"{link}\"><span style=\" text-decoration: underline; color:#0000ff;\">{website}</span></a>" + after_link
            except:
                # This turns all the [ and ] we changed into { and } back into [ and ].
                # Unfortunately 
                listed_text = list(text)
                for letter in listed_text:
                    if letter == "{": 
                        listed_text[listed_text.index(letter)] = "["
                    elif letter == "}": 
                        listed_text[listed_text.index(letter)] = "]"
                text = "".join(listed_text)
        self.output.emit(self.textBrowser, color_code, username, text, False, self.server_socket, self.server_key, ''.encode())
    
    def loop(self, key=False):
        while True:
            try:
                display_message_header = self.server_socket.recv(self.HEADER_LENGTH)
                if not display_message_header:
                    print('Connection to the server lost.')
                    self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The connection to the server has been lost..</p></body></html>\n")
                    self.pushButton.hide()
                    self.start_time = time.time()
                    self.run_loop = False
                    return False
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
    
    def receive_a_message(self):
        message_header = self.server_socket.recv(self.HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = self.server_socket.recv(message_length)
        return message
    
    def connect_to_server(self):
        # Create a socket
        self.server_socket = socks.socksocket()
        self.server_socket.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)

        # Connect to a given ip and port
        try:
            self.server_socket.connect((self.IP, self.PORT))
        except socks.GeneralProxyError:
            raise Exception

    def try_reconnecting(self):
        self.connect_to_server()
        # Send my public key.
        public_key_header = f"{len(str(self.public_key)):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.server_socket.send(public_key_header + self.public_key.save_pkcs1(format='DER'))
        # Receive the server's public key.
        self.server_key = self.loop(key=True)
        aes_key_to_go = key_to_english(self.aes_key)
        username_password = self.encrypt_json_object(dictionary=
            {"login_register": "login", "username": self.login_username, "password": self.login_password, "aes_key": aes_key_to_go})
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username_password_header = f"{len(username_password):<{self.HEADER_LENGTH}}".encode('utf-8')
        time.sleep(0.5)
        self.server_socket.send(username_password_header + username_password)
        
        # We don't need any information back.
        answer = self.decrypt_json_object(encrytped_json_object=self.loop())
        self.server_aes_key = english_to_key(answer['aes_key'])
        color_code = "#00ff35"
        self.output.emit(self.textBrowser, '', '', '', True, self.server_socket, self.server_key, self.server_aes_key)
        downtime = self.downtime()
        print('Connection to the server has been restored, after {0}'.format(downtime))
        self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                    "p, li { white-space: pre-wrap; }\n"
                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                    f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:{color_code}; \">CLIENT: <font style=\" color:{color_code}; \">Connection to the server has been restored, after </font><font style=\" color:#FFFFFF; \">{downtime}</font></p>\n")

    def run(self):
        # Now we want to loop over received messages (there might be more than one) and print them
        self.run_loop = True
        while True:
            if self.run_loop:
                try:
                    # This basically waits until there's actual traffic to receive - before this it costed 1 thread or - 25% of CPU
                    # if you had 4 threads all the time to run this - now it costs 0% until there's actual messages/requests to be sent
                    # or received :)
                    read_sockets, _, _ = select.select([self.server_socket], [], [])
                    if self.run_loop:
                        received_data = self.loop()
                        if received_data:
                            decrypted_initialization_vector = self.decrypt_a_message(
                                encrypted_message=received_data)
                            
                            ciphertext = self.loop()
                            
                            message = self.decrypt_aes_data(
                                server_aes_key=self.server_aes_key,
                                iv=decrypted_initialization_vector,
                                ciphertext=ciphertext)
                            if message == "FAILED":
                                return
                            self.received_privilege = message['color_code']
                            self.current_users = message['users']
                            self.received_username = message['username']
                            message = message['message']                        
                            
                            if message.startswith('/get_image'):
                                self.receive_the_message_thread.start_receiving_the_message(
                                True,
                                self.show_images,
                                self.received_privilege, 
                                self.current_users, 
                                self.received_username,
                                message.split()[1])
                                
                            else:
                                self.received_message = message.replace('<', '&lt;')  # Make it so that all '<' are visible to other clients, else it's just a HTML starter.
                                self.is_image = False
                                # Modify and display the message
                                self.send_message_to_textBrowser()
                except IOError as e:
                    # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                    # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                    # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                    # If we got different error code - something happened
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        print('Reading error: {}'.format(str(e)))
                        me = os.getpid()
                        sys.exit(kill_proc_tree(me))

                    # We just did not receive anything
                    continue

                except Exception as e:
                    # Any other exception - something happened, exit
                    print('Reading error: {}'.format(str(e)))
                    me = os.getpid()
                    sys.exit(kill_proc_tree(me))
            else:
                time.sleep(1)
                try:
                    self.try_reconnecting()
                    self.pushButton.show()
                    self.run_loop = True
                except Exception as e:
                    pass
                
    def get_message_contents(self, *args):
        (self.received_privilege, 
         self.current_users, 
         self.received_username, 
         self.received_message, 
         self.is_image) = args
        #Modify and display the message
        self.send_message_to_textBrowser()

    def downtime(self):
        uptime = int(time.time() - self.start_time)
        seconds = int(uptime % 60)
        hours = int(uptime / 3600)
        minutes = int(uptime / 60 - (hours * 60))
        return "{0}h:{1}m:{2}s".format(hours, minutes, seconds)
