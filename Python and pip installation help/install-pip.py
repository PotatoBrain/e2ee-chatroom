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
import getpass
import time
import os


def run_command(command, print_command=False, final=''):
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(command, stdout=tempf)
        proc.wait()
        tempf.seek(0)
        for part in command: final+=' '+part
        if print_command: print('=================Running: ', final)
        print(tempf.read().decode())


def main():
    user = getpass.getuser()
    path_1 = '/home/{0}/.local/bin/pip3.8'.format(user)
    path_2 = '/usr/local/bin/pip3.8'
    path_3 = '/usr/bin/pip3.8'
    
    main_path = os.getcwd()
    
    print1 = "===================== Now we'll do the installation steps for you, please watch for any errors. ====================="
    run_command(command=['echo', print1])
    time.sleep(2)
    run_command(print_command=True, command=['sudo', 'apt-get', 'install', 'python3'])  # needed so we can upgrade it's pip to 3.8 verison
    time.sleep(2)
    run_command(print_command=True, command=['sudo', 'apt-get', 'install', 'python3.8'])  # or find another way to install on your OS, if it doesn't install after this.
    time.sleep(2)
    run_command(print_command=True, command=['sudo', 'apt-get', 'install', 'python3-pip'])  # because python3.8 doesn't have a pip in the apt directory
    time.sleep(2)
    run_command(print_command=True, command=['pip3', 'install', '-U', 'pip'])  # download the latest pip3 version, which would be 3.8.
    time.sleep(2)
    run_command(print_command=True, command=['sudo', 'cp', path_1, path_2])  # This copies the pip3.8 file to a directory so we can use it in the terminal.
    time.sleep(2)
    run_command(print_command=True, command=['sudo', 'cp', path_1, path_3])  # This may not even be necessary :/
    print2 = "============================ If everything worked, it will display the pip version. ================================="
    run_command(command=['echo', print2])
    run_command(print_command=True, command=['pip3.8', '-V'])  # Displays the pip3.8 version/tests to see if the installation was successful.
    
    
if __name__ == "__main__":
    main()
