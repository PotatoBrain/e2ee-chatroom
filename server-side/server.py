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
import subprocess
import tempfile
import os
import json


class CheckForUpdates:
    
    def __init__(self):
        pass
    
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
        self.make_if_not_exists()
        # This checks if there are any new files to download, as opposed to updating them.
        site_info = self.get_text_trough_Tor(
            "https://raw.githubusercontent.com/PotatoBrain/e2ee-chatroom/master/server-side/server_files_list.json")
        site_downloads_list = json.loads(site_info)
        try:
            # Tries to open the file, handles an error if doesn't exist - creates a new file with the newest file requirements.
            with open('server_files_list.json', 'r') as downloads_list_json:
                downloads_list = json.loads(downloads_list_json.read())
            if not site_downloads_list == downloads_list:
                # There are some new files to be downloaded, thus - update our local list.
                with open('server_files_list.json', 'w') as new_server_files_list:
                    new_server_files_list.write(json.dumps(site_downloads_list))
                    print('Updated list of file links')
        except FileNotFoundError:
            with open('server_files_list.json', 'w') as new_server_files_list:
                new_server_files_list.write(json.dumps(site_downloads_list))
                print('Downloaded list of file links')

        version_file_exists = os.path.isfile('./server_version.md')
        if version_file_exists:
            with open('server_version.md', 'r') as version_file:
                current_version = version_file.read()
        else:
            current_version = 1.1
        try:
            newest_version = self.get_text_trough_Tor(
                "https://raw.githubusercontent.com/PotatoBrain/e2ee-chatroom/master/server-side/server_version.md")
            
            if float(newest_version) > float(current_version):
                update = input("Update avaliable, download it? (Y?)").lower()
                if update == "y"\
                        or update == '':
                    for file_name in site_downloads_list.keys():
                        newest_file_code = self.get_text_trough_Tor(site_downloads_list[file_name])
                        with open('{}'.format(file_name), 'w') as new_file:
                            new_file.write(newest_file_code)
                        print('Updated -', file_name)
                        
                    if not os.path.isfile('server_config.json'):
                        server_config = self.get_text_trough_Tor(
                            "https://raw.githubusercontent.com/PotatoBrain/e2ee-chatroom/master/server-side/server_config.json")
                        with open('server_config.json', 'w') as new_server_config:
                            new_server_config.write(server_config)
                        print("New server config downloaded, it's recommneded to edit paramaters such as room name and rules.")
                            
                    print('Updates downloaded, please restart the program..')
                    exit()
                else:
                    pass
        except requests.ConnectionError:
            pass
        
        
CheckForUpdates().check_for_updates()
restart = False
try:
    from Crypto.Util.RFC1751 import key_to_english, english_to_key
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    from Crypto.Cipher import AES
    from threading import Thread
    from base64 import b64encode
    from base64 import b64decode
    import multiprocessing
    import create_database
    import add_to_database
    import hash_password
    import get_settings
    import requests
    import sqlite3
    import socket
    import select
    import random
    import time
    import rsa
    import re
except ModuleNotFoundError:
    print('SOME PACKAGES ARE NOT INSTALLED!')
    os.system('pip3.8 install -r requirements.txt')
    print('===================== Please restart the program. =========================')
    restart = True

# Changes the window title to Server
os.system('PS1=$\nPROMPT_COMMAND=\necho -en "\033]0;Server\a"; clear')

if not restart:
    # A few static methods.
    def rsa_encrypt_a_message(message, public_key):
        return rsa.encrypt(message, public_key)


    def rsa_encrypt_json_object(dictionary, public_key):
        json_object = json.dumps(dictionary).encode('utf-8')
        return rsa_encrypt_a_message(message=json_object,
                                    public_key=public_key)


    # Define our main thread and start them on every
    class SocketServer():
        def __init__(self):
            self.HEADER_LENGTH = 128
            # Get stuff from the json config file, you can edit your settings for your room there.
            try:
                _, self.TOR_HIDDEN_ADDRESS, self.database_name, self.table_name, self.IP, self.PORT, self.BIT_SIZE, \
                    self.ROOM_NAME, self.ROOM_RULES, self.required_client_version, self.ban_permission, self.kick_permission, self.mute_permission, \
                    self.image_permission = get_settings.return_config("server_config").values()
                if self.database_name == 'no-database':
                    create_database.create_database()
                    print('------------------------- Database created -------------------------')
                self.reload_permissions()
            except:
                print("Your server_config.json file is deprecated! Download the newest one and change your settings manually(maybe to be automated)")
                return
            # Create a socket
            # socket.AF_INET - address family, IPv4, some other possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
            # socket.SOCK_STREAM - TCP, connection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams,
            # socket.SOCK_RAW - raw IP packets
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # SO_ - socket option
            # SOL_ - socket option level
            # Sets REUSEADDR (as a socket option) to 1 on socket
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind, so server informs operating system that it's going to use given IP and port
            # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to
            # 127.0.0.1 and remotely to LAN interface IP
            self.server_socket.bind((self.IP, self.PORT))
            # This makes server listen to new connections
            self.server_socket.listen()
            # List of sockets for select.select()
            self.sockets_list = [self.server_socket]
            # List of connected self.clients - socket as a key, user header and name as data
            self.clients = {}
            self.sock_threads = []
            self.thread_counter = 0
            self.notified_socket = {}
            self.next_json_object = {}
            self.banned_users_but_connected = []
            self.start_time = time.time()
            # Generate a new encryption key pair, key size/encryption strength depends on the room config.
            (self.pubkey, self.privkey) = rsa.newkeys(self.BIT_SIZE,
                                                    poolsize=multiprocessing.cpu_count())
            self.aes_key = get_random_bytes(32)  # for AES256 encryption.
            self.room_info = json.dumps({'BIT_SIZE': self.BIT_SIZE,
                                        'ROOM_NAME': self.ROOM_NAME,
                                        'ROOM_RULES': self.ROOM_RULES,
                                        'CLIENT_REQUIRED': self.required_client_version}).encode('utf-8')
            print('YOU CAN POST/SHARE THE CURRENT PUBLIC SERVER KEY SOMEWHERE ELSE SO PEOPLE CAN COMPARE AND VERIFY THEM,\
                IN ORDER TO PREVENT MITM ATTACKS!!!\nRoom public key:', self.pubkey)
            print(f'Listening for connections on {self.IP}:{self.PORT}, {self.TOR_HIDDEN_ADDRESS}')
            self.start_threads()

        def start_threads(self):
            """ Accept an incoming connection.
            Start a new SocketServerThread that will handle the communication. """
            try:
                while True:
                    read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
                    # Iterate over notified sockets and start a thread for each of them
                    for notified_socket in read_sockets:
                        if notified_socket not in self.banned_users_but_connected:
                            client_thr = Thread(target=self.initialize_thread,
                                                args=(notified_socket, self.thread_counter))
                            self.thread_counter += 1
                            self.sock_threads.append(client_thr)
                            client_thr.start()
                    client_thr.join()

                    # It's not really necessary to have this, but will handle some socket exceptions just in case
                    for notified_socket in exception_sockets:
                        username = self.clients[notified_socket][0]
                        # Remove from list for socket.socket()
                        self.sockets_list.remove(notified_socket)
                        # Remove from our list of users
                        del self.clients[notified_socket]
                        color_code = '#FFFFFF'
                        users = len(self.clients.keys())
                        for next_client_socket in self.clients:
                            # Send the color code of the matching privilege, number of total users, username and the actual
                            # message.
                            complete_message = {'color_code': color_code,
                                                'users': users,
                                                'username': username,
                                                'message': 'has disconnected.'}
                            try:
                                final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                                    public_key=self.clients[next_client_socket][2])
                                final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                                next_client_socket.send(final_message_header + final_message)
                            except OverflowError:
                                break
            except KeyboardInterrupt:
                self.close()

        def close(self):
            """ Close the client socket threads and server socket if they exists. """
            print('Closing server thread ({})'.format(self.TOR_HIDDEN_ADDRESS))
            for thr in self.sock_threads:
                thr.stop()
                thr.join()
            if self.server_socket:
                self.server_socket.close()
            print("Server has shutdown.")

        def initialize_thread(self, notified_socket, thread_number):
            self.notified_socket[thread_number] = notified_socket
            self.next_json_object[thread_number] = None
            self.run(thread_number)

        def detailed_help(self, thread_number, complete_message, message):
            complete_message['color_code'] = '#a873fc'
            command = message.split()[1].lower()
            if command == 'clear':
                complete_message['message'] = "This clears the whole chat on your screen."
            elif command == 'members':
                complete_message['message'] = "This will display all the members and their rank."
            elif command == 'uptime':
                complete_message['message'] = "Displays the amount of time that the room has been online for."
            elif command == 'image':
                complete_message['message'] = "/image LINK  - sends the image to the room, has to be a link of the image's location. Accepts Tor links."
            elif command == 'banlist':
                complete_message['message'] = "Displays the list of all banned users."
            elif command == 'reload':
                complete_message['message'] = "Reloads the room's permissions."
            elif command == 'update':
                complete_message['message'] = "/update USERNAME RANK  - updates the rank of the user, be it upgrade or downgrade."
            elif command == 'ban':
                complete_message['message'] = "/ban USER1 USER2  - bans the users from the room."
            elif command == 'unban':
                complete_message['message'] = "/unban USER1 USER  - unbans the users from the room."
            elif command == 'ranks':
                complete_message['message'] = "Shows the hierarchy of the room."
            elif command == 'bug':
                complete_message['message'] = "You can help us by reporting a bug that you have encountered. Support us by sharing this program with your friends, or even consider improving our code."
            else:
                self.command_not_found(thread_number=thread_number, complete_message=complete_message, message='.{}'.format(command))
                return
            complete_message['username'] = 'Command {}'.format(command)
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            
        def arguments_needed(self, thread_number, complete_message, command):
            complete_message['color_code'] = '#ff6060'
            complete_message['username'] = 'Argument(s) missing'
            complete_message['message'] = "Command {0} needs one or more arguments. Try doing /help {0}.".format(command)
            self.send_message(thread_number=thread_number, complete_message=complete_message)

        def permission_needed(self, thread_number, complete_message, username, rank_needed):
            complete_message['color_code'] = '#ff6060'
            complete_message['username'] = username
            complete_message['message'] = "You need the {} rank to execute this command.".format(
                rank_needed)
            self.send_message(thread_number=thread_number, complete_message=complete_message)

        def command_help(self, thread_number, complete_message):
            complete_message['color_code'] = '#edff84'
            complete_message['username'] = 'Commands'
            complete_message['message'] = "/clear, /members, /uptime, /ranks, /image, /banlist, /bug"
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            complete_message['username'] = 'Administration tools'
            complete_message['message'] = "/reload, /update, /ban, /unban"
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            complete_message['username'] = 'Help'
            complete_message['message'] = 'Try doing "/help COMMAND" for more information.'
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            
        def command_members(self, thread_number, complete_message):
            usernames = ''
            for user in self.clients:
                username = self.clients[user][0]
                next_privilage = self.get_privilege(username)[0]
                if next_privilage:
                    usernames += f"{username}({next_privilage}), "
                else:
                    usernames += f"{username}, "
            complete_message['color_code'] = '#FFFFFF'
            complete_message['username'] = 'Members online'
            complete_message['message'] = usernames
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            
        def command_uptime(self, thread_number, complete_message):
            uptime = int(time.time() - self.start_time)
            seconds = int(uptime % 60)
            hours = int(uptime / 3600)
            minutes = int(uptime / 60 - (hours * 60))

            complete_message['color_code'] = '#FFFFFF'
            complete_message['username'] = 'Uptime'
            complete_message['message'] = f"{hours}h {minutes}m {seconds}s"
            self.send_message(thread_number=thread_number, complete_message=complete_message)

        def command_banlist(self, thread_number, complete_message):
            banned_users = ''
            for banned_user in self.banned_users():
                banned_users += '{}, '.format(banned_user[0])
            complete_message['color_code'] = '#FFFFFF'
            complete_message['username'] = 'Banned users'
            complete_message['message'] = banned_users
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            
        def command_bug(self, thread_number, complete_message):
            complete_message['color_code'] = '#FFFFFF'
            complete_message['username'] = 'Report bugs'
            complete_message['message'] = 'Report bugs on our GitHub project page at [https://github.com/PotatoBrain/e2ee-chatroom/issues]'
            self.send_message(thread_number=thread_number, complete_message=complete_message)

        def command_ban(self, thread_number, complete_message, users, message):
            if message.strip() == '/ban':
                self.arguments_needed(thread_number=thread_number, complete_message=complete_message,
                    command='ban')
                return
            # Get all the mentioned users
            users_to_ban = message.split()[1:]
            print(users_to_ban)
            banned_users = []
            already_banned_users = []
            users_dont_exist = []

            for user_to_ban in users_to_ban:
                banned_status = self.get_banned_status(user_to_ban)
                if banned_status is False:
                    # That username is not registered in the database
                    users_dont_exist.append(user_to_ban)
                elif banned_status == 1:
                    # The user is already banned
                    already_banned_users.append(user_to_ban)
                else:
                    # Ban the user
                    self.ban_user(user_to_ban)
                    banned_users.append(user_to_ban)
                    banned_user_socket = self.get_client_by_value(user_to_ban)
                    if banned_user_socket is not False:
                        complete_message['color_code'] = '#FF0000'
                        complete_message['username'] = 'Ban hammer'
                        complete_message['message'] = "You have been banned."
                        final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                            public_key=self.clients[banned_user_socket][2])
                        final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                        try:
                            banned_user_socket.send(final_message_header + final_message)
                            self.banned_users_but_connected.append(banned_user_socket)
                            print('Closed connection from:{}'.format(main_dict[0]))
                            # Remove from list for socket.socket()
                            self.sockets_list.remove(banned_user_socket)
                            # Remove from our list of users
                            del self.clients[banned_user_socket]
                        except ConnectionResetError:
                            # The user is not online.
                            pass
                        users = len(self.clients.keys())
                        # Send the color code of the matching privilege, number of total users, username and the actual
                        # message.
                        complete_message['users'] = users
                        complete_message['username'] = 'Ban hammer'
                        complete_message['message'] = '{} has been banned.'.format(user_to_ban)
                        for next_client_socket in self.clients:
                            try:
                                final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                                    public_key=self.clients[next_client_socket][2])
                                final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                                next_client_socket.send(final_message_header + final_message)
                            except OverflowError:
                                break
            complete_message['color_code'] = '#FFFFFF'
            if banned_users:
                banned_users_info = ''
                for user in banned_users:
                    banned_users_info += '{}, '.format(user)
                complete_message['users'] = users
                complete_message['username'] = 'Banned users'
                complete_message['message'] = banned_users_info
                self.send_message(thread_number=thread_number, complete_message=complete_message)
            if already_banned_users:
                already_banned_users_info = ''
                for user in already_banned_users:
                    already_banned_users_info += '{}, '.format(user)
                complete_message['users'] = users
                complete_message['username'] = 'Already banned users'
                complete_message['message'] = already_banned_users_info
                self.send_message(thread_number=thread_number, complete_message=complete_message)
            if users_dont_exist:
                no_users_info = ''
                for user in users_dont_exist:
                    no_users_info += '{}, '.format(user)
                complete_message['users'] = users
                complete_message['username'] = 'Usernames do not exist'
                complete_message['message'] = no_users_info
                self.send_message(thread_number=thread_number, complete_message=complete_message)

        def command_unban(self, thread_number, complete_message, message):
            if message.strip() == '/unban':
                self.arguments_needed(thread_number=thread_number, complete_message=complete_message,
                    command='unban')
                return

            # Get all the mentioned users
            users_to_unban = message.split()[1:]
            complete_message['color_code'] = '#FFFFFF'
            unbanned_users = []
            not_banned_users = []
            users_dont_exist = []

            for user_to_unban in users_to_unban:
                banned_status = self.get_banned_status(user_to_unban)
                if banned_status is False:
                    # That username is not registered in the database
                    users_dont_exist.append(user_to_unban)
                elif banned_status == 0 or banned_status == None:
                    # The user is not banned
                    not_banned_users.append(user_to_unban)
                else:
                    # Unban the user
                    self.unban_user(user_to_unban)
                    unbanned_users.append(user_to_unban)
            if unbanned_users:
                unbanned_users_info = ''
                for user in unbanned_users:
                    unbanned_users_info += '{}, '.format(user)
                complete_message['username'] = 'Unbanned users'
                complete_message['message'] = unbanned_users_info
                self.send_message(thread_number=thread_number, complete_message=complete_message)
            if not_banned_users:
                not_banned_users_info = ''
                for user in not_banned_users:
                    not_banned_users_info += '{}, '.format(user)
                complete_message['username'] = 'Not banned users'
                complete_message['message'] = not_banned_users_info
                self.send_message(thread_number=thread_number, complete_message=complete_message)
            if users_dont_exist:
                no_users_info = ''
                for user in users_dont_exist:
                    no_users_info += '{}, '.format(user)                
                complete_message['username'] = 'Users do not exist'
                complete_message['message'] = no_users_info    
                self.send_message(thread_number=thread_number, complete_message=complete_message)
        
        def command_image(self, thread_number, complete_message, message):
            if message.strip() == '/image':
                self.arguments_needed(thread_number=thread_number, complete_message=complete_message,
                    command='image')
                return
            image_url = message.split()[1]
            # Check if the url is actually the location link the of the image - it SHOULD in theory give us some error.
            with tempfile.TemporaryFile() as tempf:
                proc = subprocess.Popen(['torsocks', 'python3.8',
                                        '{}/get_image_from_website.py'.format(os.getcwd()),
                                        '{}'.format(0), '{}'.format(image_url)], stdout=tempf)
                proc.wait()
                tempf.seek(0)
                image_exists = tempf.read().decode('utf-8')
            if image_exists.strip() == 'False':
                complete_message['color_code'] = '#ff6060'
                complete_message['username'] = 'Image'
                complete_message['message'] = "Please use a valid image location link."
                self.send_message(thread_number=thread_number, complete_message=complete_message)
                return
            complete_message['message'] = '/get_image {}'.format(image_url)
            # Tell clients to get that image from Tor.
            for client_socket in self.clients:
                final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                        public_key=self.clients[client_socket]
                                                        [2])
                final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(final_message_header + final_message)
        
        def command_update(self, thread_number, complete_message, username, message):
            if message.strip() == '/update':
                self.arguments_needed(thread_number=thread_number, complete_message=complete_message,
                    command='update')
                return
            user_to_update = message.split()[1]
            try:
                privilege = message.split()[2]
            except IndexError:
                self.arguments_needed(thread_number=thread_number, complete_message=complete_message,
                    command='update')
                return
            user_info = self.get_privilege(user_to_update)
            complete_message['color_code'] = '#ff6060'
            if not user_info is False:
                current_privilege = user_info[0]
                current_power_level = user_info[1]
                power_level = self.get_power_level(given_privilege=privilege)
                if not power_level is False:
                    self.update_user(username=user_to_update, power_level=power_level)
                    complete_message['color_code'] = '#FF0000'
                    
                    if int(power_level) > int(current_power_level): 
                        update_status = 'Upgrade'
                        updated = 'upgraded'
                        
                    elif int(power_level) < int(current_power_level):
                        update_status = 'Downgrade'
                        updated = 'downgraded'
                    
                    else:
                        complete_message['username'] = 'Update'
                        complete_message['message'] = 'Cannot update the user to the same rank they already have.'
                        self.send_message(thread_number=thread_number, complete_message=complete_message)
                        return
                        
                    complete_message['username'] = update_status
                    complete_message['message'] = "{0} {1} {2} from {3} to {4} rank.".format(username, updated, user_to_update, current_privilege, privilege)
                        
                    for client_socket in self.clients:
                        try:
                            final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                                public_key=self.clients[client_socket]
                                                                [2])
                            final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(final_message_header + final_message)
                        except OverflowError:
                            break
                else:
                    complete_message['username'] = 'Update'
                    complete_message['message'] = "Cannot update the user to a rank that doesn't exist."
                    self.send_message(thread_number=thread_number, complete_message=complete_message)
            else:
                complete_message['username'] = 'Update'
                complete_message['message'] = "Cannot update a user that doesn't exist."
                self.send_message(thread_number=thread_number, complete_message=complete_message)

        def command_ranks(self, thread_number, complete_message):
            complete_message['color_code'] = '#FFFFFF'
            complete_message['username'] = 'Ranks'
            complete_message['message'] = 'Displaying all the ranks and their colors.'
            self.send_message(thread_number=thread_number, complete_message=complete_message)
            total_ranks = 0
            for power_level in self.ranks:
                if not power_level == 'You can change the name and power levels of your ranks':
                    rank_color_code = self.rank_colors[power_level]
                    complete_message['color_code'] = rank_color_code
                    complete_message['username'] = self.ranks[power_level]
                    complete_message['message'] = ''
                    self.send_message(thread_number=thread_number, complete_message=complete_message)
                    total_ranks += 1
            complete_message['color_code'] = '#FFFFFF'
            complete_message['username'] = 'Total Ranks'
            complete_message['message'] = '{}'.format(total_ranks)
            self.send_message(thread_number=thread_number, complete_message=complete_message)

        def command_not_found(self, thread_number, complete_message, message):
            complete_message['color_code'] = '#ff6060'
            complete_message['username'] ='Help'
            complete_message['message'] = "Command {} not found. Try doing /help.".format(message[1:])
            self.send_message(thread_number=thread_number, complete_message=complete_message)
        
        def regular_message(self, complete_message):
            for client_socket in self.clients:
                # Send the color code of the matching privilege, number of total users, username and the
                # actual message.
                try:
                    final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                        public_key=self.clients[client_socket]
                                                        [2])
                    final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(final_message_header + final_message)
                except OverflowError:
                    break
                
        def command_reload(self, thread_number, complete_message):
            self.reload_permissions()
            complete_message['color_code'] = '#4374ff'
            complete_message['username'] = 'Reload'
            complete_message['message'] = 'Server permissions reloaded successfully.'
            self.send_message(thread_number=thread_number, complete_message=complete_message)
        

        def run(self, thread_number):
            print("[Thr {}] started.".format(thread_number))
            # If notified socket is a server socket - new connection, accept it
            if self.notified_socket[thread_number] == self.server_socket:
                print('is new')

                # Accept new connection
                # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                # The other returned object is ip/port set
                client_socket, client_address = self.server_socket.accept()

                message = self.receive_message(client_socket)
                if message is not None:
                    try:
                        print('message for the logging in - ', message)
                        info_message = message.decode('utf-8')
                        if info_message == "INFO-PLS":
                            print('room info:', self.room_info)
                            room_info_header = f"{len(str(self.room_info)):<{self.HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(room_info_header + self.room_info)
                            print('info sent')
                        return
                    except AttributeError:
                        # Get the public key from the client
                        public_key = message
                        print('passed the public_key')

                    ready_key = self.pubkey.save_pkcs1(format='DER')
                    key_message_header = f"{len(str(ready_key)):<{self.HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(key_message_header + ready_key)

                    # Client should send their username and password right away, receive it
                    user = self.receive_message(client_socket)
                    print('passed the user')

                    # If False - client disconnected before he sent his name
                    if user is False:
                        return
                    else:
                        # Send back login status.
                        users = len(self.clients.keys()) + 1
                        user = self.rsa_decrypt_json_object(thread_number=thread_number,
                                                        encrypted_json_object=user)
                        login_register = str(user['login_register'])
                        username = str(user['username'])
                        password = str(user['password'])
                        aes_key = english_to_key(user['aes_key'])
                        color_code = '#FFFFFF'
                        print('client public key is: ', public_key)

                        login_status = str(self.login_account(login_register, username, password))
                        
                        id_identifier = 0
                        if login_status == '3' or login_status == '4':
                            # Add accepted socket to select.select() list
                            self.sockets_list.append(client_socket)
                            complete_message = {'color_code': color_code, 'users': users, 'username': username,
                                                'message': 'has joined.'}
                            for next_client_socket in self.clients:
                                # Send the message someone joined.
                                try:
                                    final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                                        public_key=self.clients[next_client_socket]
                                                                        [2])
                                    final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                                    next_client_socket.send(final_message_header + final_message)
                                except OverflowError:
                                    break
                            # Also save username and other stuff.
                            id_identifier = random.randint(1000000000000000, 9999999999999999)  # Will be used in the future if I somehow
                            # Figure out how to upload photos from computers directyl - I made it in the first day, that wasn't the problem..
                            # what was is that he ciphertext got changed as it came to the server, and I even tried it over localhost..
                            # so it's not the Tor, I suspect it has to be something either with the sockets or PyQt5 library, something
                            # that I may be missing, but I have literally spent a week trying to figure it out..
                            self.clients[client_socket] = [username, client_address, public_key, 
                            {'aes_key':             aes_key,
                            'id_identifier':       id_identifier,
                            'iv':                  False
                            }]
                            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, username))
                        display_message = {'login_status': login_status, 
                                        'users': users,
                                        'id_identifier': id_identifier}
                        display_message = rsa_encrypt_json_object(dictionary=display_message,
                                                            public_key=public_key)
                        display_message_header = f"{len(display_message):<{self.HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(display_message_header + display_message)
                        print('message sent')
            # Else existing socket is sending a message
            else:
                main_dict = self.clients[self.notified_socket[thread_number]]
                print('not new')
                try:
                    # Receive message
                    message = self.receive_message(self.notified_socket[thread_number])
                    print('1')
                    # If False, client disconnected, clean
                    if message is False:
                        print('why are we here.. just to suffer?')
                        print('Closed connection from:{}'.format(main_dict[0]))
                        username = main_dict[0]
                        # Remove from list for socket.socket()
                        self.sockets_list.remove(self.notified_socket[thread_number])
                        # Remove from our list of users
                        del self.clients[self.notified_socket[thread_number]]
                        color_code = '#FFFFFF'
                        users = len(self.clients.keys())
                        complete_message = {'color_code': color_code, 'users': users, 'username': username,
                                            'message': 'has disconnected.'}
                        for next_client_socket in self.clients:
                            # Send the color code of the matching privilege, number of total users, username and the actual
                            # message.
                            try:
                                final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                                    public_key=self.clients[next_client_socket]
                                                                    [2])
                                final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                                next_client_socket.send(final_message_header + final_message)
                            except OverflowError:
                                break
                    else:
                        print('2')
                        print('message: ', message)
                        message = self.rsa_decrypt_a_message(encrypted_message=message)
                        print('3')
                        users = len(self.clients.keys())
                        username = main_dict[0]
                        user_info = self.get_privilege(username)
                        user_privilege = user_info[0]
                        user_power_level = user_info[1]
                        color_code = self.rank_colors[str(user_power_level)]
                        print(username, '>', message)

                        complete_message = {'color_code': color_code,
                                            'users': users,
                                            'username': username,
                                            'message': message}

                        # Check if the user has executed any known commands or not.
                        if message.startswith('/'):
                            if message.lower().startswith('/help'):
                                if message.lower().strip() == '/help':
                                    self.command_help(thread_number=thread_number, complete_message=complete_message)
                                
                                else:
                                    self.detailed_help(thread_number=thread_number, complete_message=complete_message,
                                                    message=message)
                                
                            elif message.lower().startswith('/members'):
                                self.command_members(thread_number=thread_number, complete_message=complete_message)                            
                                
                            elif message.lower().startswith('/uptime'):
                                self.command_uptime(thread_number=thread_number, complete_message=complete_message)
                                
                            elif message.lower() == '/banlist':
                                self.command_banlist(thread_number=thread_number, complete_message=complete_message)
                                
                            elif message.lower() == '/bug':
                                self.command_bug(thread_number=thread_number, complete_message=complete_message)
                                
                            elif message.lower().startswith('/ban'):
                                if user_power_level >= self.ban_permission:
                                    self.command_ban(thread_number=thread_number, complete_message=complete_message,
                                                    users=users, message=message)
                                    
                                else:
                                    self.permission_needed(thread_number=thread_number, complete_message=complete_message,
                                                        username='Ban', rank_needed=self.ban_permission_rank)
                                    
                            elif message.lower().startswith('/unban'):
                                if user_power_level >= self.ban_permission:
                                    self.command_unban(thread_number=thread_number, complete_message=complete_message,
                                                    message=message)
                                    
                                else:
                                    self.pernission_needed(thread_number=thread_number, complete_message=complete_message,
                                                        username='Unban', rank_needed=self.ban_permission_rank)
                            
                            elif message.lower().startswith('/image'):
                                if user_power_level >= self.image_permission:
                                    self.command_image(thread_number=thread_number, complete_message=complete_message, 
                                        message=message)
                                    
                                else:
                                    self.permission_needed(thread_number=thread_number, complete_message=complete_message,
                                                        username='Image', rank_needed=self.image_permission_rank)
                                
                            elif message.lower().startswith('/update'):
                                if user_power_level == 100:
                                    self.command_update(thread_number=thread_number, complete_message=complete_message, 
                                                        username=username, message=message)
                                    
                                else:
                                    self.permission_needed(thread_number=thread_number, complete_message=complete_message,
                                                        username='Update', rank_needed=self.owner_rank)
                            
                            elif message.lower() == '/reload':
                                if user_power_level == 100:
                                    self.command_reload(thread_number=thread_number, complete_message=complete_message)
                                
                                else:
                                    self.permission_needed(thread_number=thread_number, complete_message=complete_message,
                                                        username='Reload', rank_needed=self.owner_rank)
                                    
                            elif message.lower() == '/ranks':
                                self.command_ranks(thread_number=thread_number, complete_message=complete_message)

                            elif message.lower().startswith('/get_image'):
                                # Only the server can send this.
                                return

                            else:
                                self.command_not_found(thread_number=thread_number, complete_message=complete_message, 
                                                    message=message)
                                
                        else:       
                            self.regular_message(complete_message=complete_message)
                            
                except ConnectionResetError as e:
                    print(e)
                    print('Closed connection from:{}'.format(main_dict[0]))
                    username = main_dict[0]
                    # Remove from list for socket.socket()
                    self.sockets_list.remove(self.notified_socket[thread_number])
                    # Remove from our list of users
                    del self.clients[self.notified_socket[thread_number]]
                    color_code = '#FFFFFF'
                    users = len(self.clients.keys())
                    # Send the color code of the matching privilege, number of total users, username and the actual
                    # message.
                    complete_message = {'color_code': color_code,
                                        'users': users,
                                        'username': username,
                                        'message': 'has disconnected.'}
                    for next_client_socket in self.clients:
                        try:
                            final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                                public_key=self.clients[next_client_socket][2])
                            final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
                            next_client_socket.send(final_message_header + final_message)
                        except OverflowError:
                            break

        # Handles message receiving
        def receive_message(self, client_socket):

            try:
                # Receive our "header" containing message length, it's size is defined and constant
                message_header = client_socket.recv(self.HEADER_LENGTH)
            except socket.error:
                # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
                # or just lost his connection socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what
                # sends information about closing the socket (shutdown read/write) and that's also a cause when we
                # receive an empty message
                return False

            # If we received no data, client gracefully closed a connection, for example using socket.close() or
            # socket.shutdown(socket.SHUT_RDWR)
            if not len(message_header):
                return False

            try:
                # Convert header to int value
                message_length = int(message_header.decode('utf-8').strip())
            except ValueError:
                # The user is probably connecting to our Tor hidden service via a Web Browser. Not supported.
                return False

            # Return an object of message header and message data
            message = client_socket.recv(message_length)
            try:
                final_message = rsa.key.PublicKey.load_pkcs1(message, format='DER')
            except:
                final_message = message
            return final_message

        def send_message(self, thread_number, complete_message):
            final_message = rsa_encrypt_json_object(dictionary=complete_message,
                                                    public_key=self.clients[self.notified_socket[
                                                    thread_number]][2])
            final_message_header = f"{str(len(final_message)):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.notified_socket[thread_number].send(final_message_header + final_message)

        @staticmethod
        def sanitize_data(data):
            return re.sub(r"[^a-zA-Z0-9 ]", "", data)

        def login_account(self, login_register, username, password):
            with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                cursor = conn.cursor()
                if not username or not password:
                    # Username or password are empty..
                    display_message = 1
                elif len(username) > 10:
                    display_message = 7
                elif len(password) > 30:
                    display_message = 8
                elif ("select" in username.lower() or
                    "delete" in username.lower() or
                    "insert" in username.lower() or
                    "drop" in username.lower() or
                    "update" in username.lower() or
                    "select" in password.lower() or
                    "delete" in password.lower() or
                    "insert" in password.lower() or
                    "drop" in password.lower() or
                    "update" in password.lower()):
                    # To prevent SQL injections, I guess.
                    display_message = 2
                else:
                    # Check for any symbols - not allowed in order to prevent SQL injections - I am not a hacker, but this is as far as I know of how to prevent most of them.
                    sanitized_username = self.sanitize_data(username)
                    sanitized_password = self.sanitize_data(password)
                    if sanitized_username != username or sanitized_password != password:
                        # There are symbols in the username or passwords..
                        display_message = 6
                    else:
                        if login_register == 'register':
                            exists = self.get_privilege(username=username)
                            if not exists:
                                add_to_database.insert_user(self.database_name, self.table_name, username, password)
                                # Created new account, grant access.
                                display_message = 3
                            else:
                                # User already register, deny access.
                                display_message = 10
                        elif login_register == 'login':
                            banned_status = self.get_banned_status(username)
                            if banned_status == 1:
                                # They have been banned, deny access.
                                display_message = 9
                            else:
                                try:
                                    # Take their password, hash it and compare from the one that's in the database.
                                    cursor.execute("SELECT salt FROM {} WHERE username=?".format(self.table_name), (username,))
                                    salt = cursor.fetchone()[0]
                                    cursor.execute("SELECT hashed_password FROM {} WHERE username=?".format(self.table_name), (username,))
                                    database_hashed_password = cursor.fetchone()[0]
                                    hashed_password = hash_password.hash_the_password(password, salt)['password']
                                    print('hashed_password: ', hashed_password)
                                    if hashed_password == database_hashed_password:
                                        display_message = 4
                                        # Grant access
                                    else:
                                        # Incorrect password.
                                        display_message = 5
                                except TypeError:
                                    # The user is not registered, deny access.
                                    display_message = 11
            return display_message

        def get_client_by_value(self, username):
            for client in self.clients.keys():
                if self.clients[client][0] == username:
                    return client
            return False

        def get_privilege(self, username):
            try:
                with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT power_level FROM {} WHERE username=?".format(self.table_name), (username,))
                    power_level = cursor.fetchone()[0]
                    privilege = self.ranks.get(power_level)
                return [privilege, int(power_level)]
            except Exception as e:
                print(e)
                return False

        def get_banned_status(self, username):
            try:
                with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT banned FROM {} WHERE username=?".format(self.table_name), (username,))
                    banned_status = cursor.fetchone()[0]
                return banned_status
            except TypeError:
                return False

        def ban_user(self, username):
            with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE {} SET banned=? WHERE username=?".format(self.table_name), (1, username,))

        def unban_user(self, username):
            with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE {} SET banned=? WHERE username=?".format(self.table_name), (0, username,))

        def banned_users(self):
            with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username FROM {} WHERE banned=?".format(self.table_name), (1,))
                return cursor.fetchall()

        def update_user(self, username, power_level):
            try:
                with sqlite3.connect("./databases/{}.db".format(self.database_name)) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE {} SET power_level=? WHERE username=?".format(self.table_name), (power_level, username,))
            except TypeError:
                return False

        def get_power_level(self, given_privilege):
            for power_level in self.ranks:
                if self.ranks[power_level] == given_privilege:
                    return power_level
            return False
        
        def reload_permissions(self):
            _, self.TOR_HIDDEN_ADDRESS, self.database_name, self.table_name, self.IP, self.PORT, self.BIT_SIZE, \
                self.ROOM_NAME, self.ROOM_RULES, self.required_client_version, self.ban_permission, self.kick_permission, self.mute_permission, \
                self.image_permission = get_settings.return_config("server_config").values()
            self.ranks = get_settings.return_config("permissions")
            self.rank_colors = get_settings.return_config('rank_colors')
            self.ban_permission = int(self.ban_permission)
            self.kick_permission = int(self.kick_permission)
            self.mute_permission = int(self.mute_permission)
            self.image_permission = int(self.image_permission)
            self.owner_rank = self.ranks.get(str(100))
            self.ban_permission_rank = self.ranks.get(str(self.ban_permission))
            self.kick_permission_rank = self.ranks.get(str(self.kick_permission))
            self.mute_permission_rank = self.ranks.get(str(self.mute_permission))
            self.image_permission_rank = self.ranks.get(str(self.image_permission))

        def aes_encrypt_a_message(self, public_key, *, dictionary):
            data = json.dumps(dictionary).encode()
            cipher = AES.new(self.aes_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data, AES.block_size))
            iv = b64encode(cipher.iv)
            ct = b64encode(ct_bytes)
            return rsa_encrypt_a_message(message=iv, public_key=public_key), ct

        def rsa_decrypt_a_message(self, encrypted_message):
            try:
                message = rsa.decrypt(encrypted_message, self.privkey)
                if type(message) is str:
                    return message
                print('not str :(')
                print('message     ', message)
                return message.decode('utf-8')
            except rsa.pkcs1.DecryptionError as e:
                print(e)
                return 'FAILED'
            except TypeError as e2:
                print(e2)
                return 'FAILED'

        def rsa_decrypt_json_object(self, thread_number, encrypted_json_object):
            json_object = self.rsa_decrypt_a_message(encrypted_message=encrypted_json_object)
            self.retry_json(thread_number=thread_number,
                            received_info=json_object)
            return self.next_json_object[thread_number]

        def aes_decrypt_a_message(self, iv, key, *, aes_encrypted_ciphertext):
            # try:
            # print('ciphertext is ', aes_encrypted_ciphertext)
            print('ciphertext type ', type(aes_encrypted_ciphertext))
            print('ciphertext length ', len(aes_encrypted_ciphertext))
            print('iv type ', type(iv))
            print('iv is ', iv)
            print('iv length ', len(iv))
            iv = b64decode(iv)
            ct = b64decode(aes_encrypted_ciphertext)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            data = unpad(cipher.decrypt(ct), AES.block_size)
            # Should return the decrypted ciphertext which is the image in bytes
            return data
            # except (ValueError, KeyError):
            #     # Decryption failed.
            #     return False


        def retry_json(self, thread_number, received_info):
            try:
                self.next_json_object[thread_number] = json.loads(received_info)
            except ValueError:
                time.sleep(1)
                print(received_info)
                new_json_object = received_info[:-3]
                if new_json_object == '':
                    raise TypeError 
                self.retry_json(thread_number=thread_number,
                                received_info=new_json_object)


    if __name__ == "__main__":
        __author__ = "PotatoBrain"
        a = SocketServer()
        a.close()
