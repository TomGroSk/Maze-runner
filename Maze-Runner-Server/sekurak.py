import base64
import config

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class SecurityDispatcher:

    def __init__(self):
        self.key = self.prepareKey()
        self.fernet = Fernet(self.key)

    def prepareKey(self):
        password = config.PASSWORD.encode()
        salt = b'asdf'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, msg):
        return self.fernet.encrypt(msg)

    def decrypt(self, msg):
        return self.fernet.decrypt(msg)