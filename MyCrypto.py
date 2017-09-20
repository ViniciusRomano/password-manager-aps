#!/usr/bin/python

import hashlib
import pickle

from Crypto.Cipher import AES
from Crypto import Random


class MyCrypto():

    # hash password in SHA256
    def hash_password(self, password):
        hash_pass = hashlib.sha256(password).hexdigest()
        return hash_pass

    # padding message
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key):
        key = self.pad_password(key)[:16]
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext, key):
        key = self.pad_password(key)[:16]
        iv = self.pad(ciphertext)[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        # removes zeros from plaintext and returns
        return plaintext.rstrip(b"\0")
