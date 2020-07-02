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
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import subprocess
import tempfile
import psutil
import select
import time
import errno
import sys
import os


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


class ReceiveMessage(QThread):
    print('1')
    output = pyqtSignal(QTextBrowser, str, str, str)   # Don't forget to type in the output types
    print('2')

    def __init__(self, parent=None):
        # super().__init__(self, parent)
        QThread.__init__(self, parent)
        self.exiting = False
        self.is_image = False
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

    def start_receiving_messages(self, *args):
        # Receive the arguments.
        (
            self.HEADER_LENGTH,
            self.server_socket,
            self.textBrowser,
            self.pushButton,
            self.label4,
            self.decrypt_json_object
        ) = args
        print('6')
        self.start()

    def send_message_to_textBrowser(self):
        username = f"{datetime.now().strftime('%H:%M')} {self.received_username}"
        text = self.received_message
        color_code = self.received_privilege
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
                        after_https = link.split("https://")[1]
                        website = after_https.split(".")[0]
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
        self.output.emit(self.textBrowser, color_code, username, text)
    
    def receive_a_message(self):
        message_header = self.server_socket.recv(self.HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = self.server_socket.recv(message_length)
        return message

    def run(self):
        # Now we want to loop over received messages (there might be more than one) and print them
        run = True
        while True:
            if run:
                try:
                    # This basically waits until there's actual traffic to receive - before this it costed 1 thread or - 25% of CPU
                    # if you had 4 threads all the time to run this - now it costs 0% until there's actual messages/requests to be sent
                    # or received :)
                    read_sockets, _, _ = select.select([self.server_socket], [], [])
                    server_socket = read_sockets[0]
                    message_header = server_socket.recv(self.HEADER_LENGTH)
                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(message_header):
                        print('Connection closed by the server')
                        self.textBrowser.append("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Server has closed the connection.</p></body></html>\n")
                        self.pushButton.hide()
                        run = False 
                    if run:
                        message_length = int(message_header.decode('utf-8').strip())
                        received_data = server_socket.recv(message_length)
                        message = self.decrypt_json_object(encrytped_json_object=received_data)
                        if message == "FAILED":
                            return
                        self.received_privilege = message['color_code']
                        self.current_users = message['users']
                        self.received_username = message['username']
                        self.label4.setText(f"Users:\n{self.current_users}")
                        message = message['message']                        
                        
                        if message.startswith('/get_image'):
                            # Get image url from the message
                            image_url = message.split()[1]
                            # Get the image data from the provided link
                            with tempfile.TemporaryFile() as tempf:
                                proc = subprocess.Popen(['torsocks', 'python3.8',
                                                         '{}/get_image_from_website.py'.format(os.getcwd()),
                                                         '{}'.format(0), '{}'.format(image_url)], stdout=tempf)
                                proc.wait()
                                tempf.seek(0)
                                self.received_message = tempf.read().decode('utf-8')
                                print(len(self.received_message))
                            self.is_image = True
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
