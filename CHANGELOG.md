Update 1.40
* Client update - a new command /bug , links to our issues section of our project(on GitLab).
* Client update - a new login design, seperate buttons for register and login now(they were 1 button)
* Server update - sends a required version of the client-side, the one it's compatible with(and client-side displays if the version is incompatible.
* Server and client update - everything can be downloaded just with the single server.py/client.py file.

Update 1.30
* Client update - Made receiving, sending messages and generating keys work in another PyQt5 thread (there's no more the case of the application not responding due to the keys generating and blocking the main GUI loop.)
* Server update - Made more colorful and everything got re-checked, as well as made easier to read - more functions.
* Server update - Python dependencies get automatically installed; permissions handled now with the power level instead of names, code bade better, added commands /ranks, /image, /reload, /update (upgrade or downgrade someone);

Early updates
* added so one can see a more detailed help of the command with /help COMMAND
* Added some administrative tools ban and unban. Unfortunately this is only effective at the username level - because one can't ban IP addresses because there are none. No room can know the client's IP address.
* Hash passwords, with salts.
* Make the programs work on Windows systems.
* Check for updates.
* Implement Tor communication to our project.
* Figure out how onion hidden services work, how to create them, and how to communicate with them through the Tor network through scripts, sockets library.
* Encrypt the commmunication, with the RSA cryptosystem.
* Make server-side and client-sides able to communicate over local network.