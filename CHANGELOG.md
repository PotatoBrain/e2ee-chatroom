__Update 1.60__
* __Cryptography__ - Messages encryption changed from RSA to AES with RSA. Of course, the AES keys are encrypted with the RSA cryptosystem and the ciphertext's initialization vectors(maybe not neccesary :/)(see the difference between asymmetric and symetric key cryptosystems).
* __Server side__ - Servers can now set their own characters limit, because now they aren't restricted with the RSA's maximum encryption limit(for RSA-4096 it was 501 bytes or - around 501 characters, with AES, people can now send loooong messages, if allowed.)
* __Cryptography__ - not only are the messages sent - encrypted/decrypted faster, but also the server doesn't HAVE TO use RSA-4096 (whose key generation is around 10 times slower than RSA-2048), but can use a key-size of 2048, which is DRAMASTICALLY faster. One reason of this is that the server doesn't have to encrypt huge amounts of messages for EVERY user with their RSA public key, but with server's AES key instead, and also rooms can choose between faster and more secure.
* __Client side__ - Client-side will automatically generate a keypair of the size that the server has it(not over 4096).
* __Client side__ - Changed so if a connection to the server is lost (a Tor circuit changes, the room goes offline or restarts, etc.) - it will retry to connect to the server. Useful if one wants to be connected to the server as soon as possible after if closes, for example. Useful for 24/7 administrative activities, or even if the connection is lost unexpectedly.
* __Client side__ - Added an option to receive links of images instead, though it's inside the code, it will probably be added with the user-friendly gui update.
* __Server and client side__ - Sending and receiving messages while receiving an image from someone was a big problem that I believe I have FIXED, with threading and removing a part of server-side code for images that for some reason gave errors - the user had to restart their client in order to send messages IF they had sent anything while they were receiving the image(even knowing it didn't help, because it was a server-side problem). Please report any bugs.

__Update 1.51__
* __Client side__ - Changed the scaling of images: if the image is over 620 pixels in width, it will be scaled down to 1. fit the chatroom window(whose size will probably be changed in the future/made resizable) , but also 2. there are about 10-20 whitespace lines before and after the image is sent, if it's over the 620 pixels in width.
We are using a library called __cv2__ to get the size of the temporarily downloaded image.
If the image is under 620 pixels in width ( height is not checked because there's no problem with that ) - the image is actually not resized, in order to keep the original (the best) quality of the image.
* __Client side__ - Tweaked the feature that changes links in the square brackets (example [invidio.us]) to a clickable link __ONLY__ IF the link ...is actually a link, in other words, if it's not just words, it has to contain ends such as '.com', '.org' and such.

__Update 1.50__
* __Project transfered back to GitHub, from GitLab, due to last update(line below), which would be impossible otherwise, because of GitLab captchas :*(*(__
* __Server and client update__ - Route requests of <del>GitLab</del> GitHub texts (updates) through Tor, as well.
  * Only 1 file required - server.py/client.py which then makes it's own python file __tor_requests.py__ that will be used to download the other(newest) files trough Tor with the help of torsocks.

__Update 1.40__
* __Client update__ - A new command /bug , links to our issues section of our project(on GitLab).
* __Client update__ - A new login design, seperate buttons for register and login now(they were 1 button)
* __Server update__ - Sends a required version of the client-side, the one it's compatible with(and client-side displays if the version is incompatible.
* __Server and client update__ - Everything can be downloaded just with the single server.py/client.py file.

__Update 1.30__
* __Client update__ - Made receiving, sending messages and generating keys work in another PyQt5 thread (there's no more the case of the application not responding due to the keys generating and blocking the main GUI loop.)
* __Server update__ - Made more colorful and everything got re-checked, as well as made easier to read - more functions.
* __Server update__ - Python dependencies get automatically installed; permissions handled now with the power level instead of names, code bade better, added commands /ranks, /image, /reload, /update (upgrade or downgrade someone);

__Early updates__
* added so one can see a more detailed help of the command with /help COMMAND
* Added some administrative tools ban and unban. Unfortunately this is only effective at the username level - because one can't ban IP addresses because there are none. No room can know the client's IP address.
* Hash passwords, with salts.
* Make the programs work on Windows systems.
* Check for updates.
* Implement Tor communication to our project.
* Figure out how onion hidden services work, how to create them, and how to communicate with them through the Tor network through scripts, sockets library.
* Encrypt the commmunication, with the RSA cryptosystem.
* Make server-side and client-sides able to communicate over local network.
