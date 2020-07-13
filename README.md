# E2ee chatroom project that routs it's traffic over the Tor network.
Here I make my Python project better and update my progress.

Made using python3.8 and additionally encrypted communication over Tor.

**MORE FEATURES COMING SOON.**

# Linux only :(
This project does not support Windows 10, it may in the future, as it is a hassle to figure everything out and to get it working there, for now.

# Python3.8
Added hopefully useful instructions in the **Python and pip installation help** directory to assist users in installing python and it's installation package.

Basically you need python version 3.8 and it's installation package pip version 3.8.

# You have to have Tor installed
To be automated.
To install it, you can run: **sudo apt-get install tor** , or the package manager that your distribution comes with.

# Running the program
If you want to connect to someone's room you will have to download the client-side program from https://github.com/PotatoBrain/e2ee-chatroom/tree/master/client-side , and then inside that folder open a terminal and type 
> python3.8 client.py

If you want to host a room - you will have to create your own Tor hidden service manually(to be automated in the future), that will listen on the given port, change the server config(the address, port, room name, room rules; do not change the database and table setting) in the **server_config.json** manually(GUI in the future) on https://github.com/PotatoBrain/e2ee-chatroom/tree/master/server-side and run it with 
> python3.8 server.py

# How the server-side works:
Outgoing
> room/server side(IP=127.0.0.1, PORT=1235) ----> the Tor hidden service listens on that port, routs it's traffic to the port 9050 ---->  the Tor network/internet

Incoming
> The Tor network/internet ----> the Tor hidden service listens on the port 9050, routs it's traffic to the server-side port 1235 ----> room/server side(IP=127.0.0.1, PORT=1235)

# Other
Our room's V3 Tor hidden service address: 735tmznegwcmepvctwt7ipnxps6yqfmsqofp5fujie4kvkgrct6kczad.onion
(may not be always online)

You can see image previews in the added images.
And if you are interested, consider checking out the CHANGELOG.md and TODO_list.md to see the progress we have made so far, and the progress we plan on making.

Please note that I am still a beginner-intermediate Python hobbyist programmer.
I am aware that the code may not be good-looking, efficient or the best. My goal is to make it work, and then improve it with time.
Advices and help appreciated.

Special thanks to kecia and others.
