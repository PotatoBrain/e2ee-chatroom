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
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



def hash_the_password(password, salt=None):
	password =str(password).encode()
	if salt is None:
		salt = os.urandom(64)
	kdf = PBKDF2HMAC(
	    algorithm=hashes.SHA512(),
	    length=64,
	    salt=salt,
	    iterations=100000,
	    backend=default_backend()
	)

	hashed_password = base64.urlsafe_b64encode(kdf.derive(password))
	return {'salt': salt, 'password': hashed_password}

