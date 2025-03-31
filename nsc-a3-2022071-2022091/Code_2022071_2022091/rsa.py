import random
import math
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from Crypto.Util.number import getPrime

class RSA:
    def __init__(self, key_size):
        self.p = 0
        self.q = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0
        self.key_size = key_size
        self.block_size = key_size // 8

    def generate_key(self):
        """Generate distinct prime numbers p and q, then compute n and phi."""
        self.p = getPrime(self.key_size // 2)
        self.q = getPrime(self.key_size // 2)

        # Ensure distinct primes
        while self.p == self.q:
            self.q = getPrime(self.key_size // 2)

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

    def generate_e(self):
        """Generate e such that gcd(e, phi) = 1."""
        self.e = random.randrange(2, self.phi)
        while math.gcd(self.e, self.phi) != 1:
            self.e = random.randrange(2, self.phi)

    def generate_d(self):
        """Compute modular inverse of e mod phi (i.e., d)."""
        self.d = pow(self.e, -1, self.phi)

    def generate_keys(self):
        """Generate (public_key, private_key)."""
        self.generate_key()
        self.generate_e()
        self.generate_d()
        return (self.e, self.n), (self.d, self.n)

    def encrypt(self, plaintext, public_key):
        """Encrypt plaintext (str) with the given public key (block-wise)."""
        e, n = public_key
        ciphertext = ""
        # For RSA with PKCS#1-like padding, we leave 11 bytes for overhead
        for i in range(0, len(plaintext), self.block_size - 11):
            block = plaintext[i : i + self.block_size - 11]
            block_bytes = block.encode('utf-8')
            block_bytes = pad(block_bytes, self.block_size)
            block_int = int.from_bytes(block_bytes, byteorder='big')
            encrypted_block = pow(block_int, e, n)
            # Convert to base64
            enc_b64 = b64encode(
                encrypted_block.to_bytes((encrypted_block.bit_length() + 7) // 8, byteorder='big')
            ).decode('utf-8')
            ciphertext += enc_b64 + " "
        return ciphertext.strip()

    def decrypt(self, ciphertext, private_key):
        """Decrypt ciphertext (str) with the given private key (block-wise)."""
        d, n = private_key  # Use the provided private key
        decrypted_text = ""
        blocks = ciphertext.strip().split()
        for block in blocks:
            block_bytes = b64decode(block)
            block_int = int.from_bytes(block_bytes, byteorder='big')
            decrypted_block_int = pow(block_int, d, n)
            # Convert to fixed block size using self.block_size
            fixed_bytes = decrypted_block_int.to_bytes(self.block_size, byteorder='big')
            unpadded = unpad(fixed_bytes, self.block_size)
            decrypted_text += unpadded.decode('utf-8')
        return decrypted_text
