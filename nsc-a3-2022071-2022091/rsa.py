# rsa.py
import random
import math
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime

class RSA:
    def __init__(self, key_size):
        self.key_size = key_size
        self.block_size = key_size // 8

    def generate_key(self):
        self.p = getPrime(self.key_size // 2)
        self.q = getPrime(self.key_size // 2)
        # Ensure distinct primes:
        while self.p == self.q:
            self.q = getPrime(self.key_size // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

    def generate_e(self):
        self.e = random.randrange(2, self.phi)
        while math.gcd(self.e, self.phi) != 1:
            self.e = random.randrange(2, self.phi)

    def generate_d(self):
        self.d = pow(self.e, -1, self.phi)

    def generate_keys(self):
        self.generate_key()
        self.generate_e()
        self.generate_d()
        return (self.e, self.n), (self.d, self.n)

    def encrypt(self, plaintext, public_key):
        e, n = public_key
        ciphertext = ""
        for i in range(0, len(plaintext), self.block_size - 11):
            block = plaintext[i:i+self.block_size-11]
            block_bytes = block.encode('utf-8')
            block_bytes = pad(block_bytes, self.block_size)
            block_int = int.from_bytes(block_bytes, byteorder='big')
            enc_int = pow(block_int, e, n)
            enc_bytes = enc_int.to_bytes((enc_int.bit_length() + 7) // 8, byteorder='big')
            ciphertext += b64encode(enc_bytes).decode('utf-8') + " "
        return ciphertext.strip()

    def decrypt(self, ciphertext, private_key):
        d, n = private_key
        plaintext = ""
        for block in ciphertext.strip().split():
            block_bytes = b64decode(block)
            block_int = int.from_bytes(block_bytes, byteorder='big')
            dec_int = pow(block_int, d, n)
            dec_bytes = dec_int.to_bytes((dec_int.bit_length() + 7) // 8, byteorder='big')
            dec_bytes = unpad(dec_bytes, self.block_size)
            plaintext += dec_bytes.decode('utf-8')
        return plaintext
