import os

from typing import Tuple

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.padding import ANSIX923
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Cryptosystem:
    """
    A class that implements a hybrid cryptosystem

    Attributes:
        None

    Methods:
        generate_keys(self, key_length):
          Generates keys for an asymmetric algorithm and a key for a symmetric algorithm
        encrypt_text(self, text, encrypted_sym, private_key):
          Encrypts the text using a symmetric algorithm
        decrypt_text(self, encrypted_text, encrypted_sym, private_key):
          Decrypts the text using a symmetric algorithm
    """

    def __init__(self):
        """
        The constructor does nothing

        Parameters:
            None

        Returns:
            None
        """
        pass

    @staticmethod
    def generate_keys(key_length: int) -> Tuple[bytes, rsa.RSAPrivateKey,
                                                rsa.RSAPublicKey]:
        """
        Static method for generating keys for an asymmetric algorithm and 
        a key for a symmetric algorithm. Also encrypts the symmetric encryption 
        key with a public key of the asymmetric algorithm.

        Parameters:
            key_length: int
              Key length for the symmetric algorithm

        Returns:
            (enc_symmetric, private_key, public_key): Tuple[bytes, rsa.RSAPrivateKey,
                 rsa.RSAPublicKey]
              A tuple of keys(encrypted symmetric key, private key, public key)
        """
        symmetric_key = os.urandom(key_length)
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        enc_symmetric = public_key.encrypt(symmetric_key, OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return enc_symmetric, private_key, public_key

    @staticmethod
    def encrypt_text(text: str, enc_symmetric: bytes,
                     private_key: rsa.RSAPrivateKey) -> bytes:
        """
        Static method for text encryption.

        Parameters:
            text: str
              The source text
            enc_symmetric: bytes
              Encrypted symmetric key
            private_key: rsa.RSAPrivateKey
              The private key of the asymmetric algorithm

        Returns:
            encrypted_text: bytes
              Encrypted text
        """
        symmetric_key = private_key.decrypt(enc_symmetric, OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        padder = ANSIX923(128).padder()
        b_text = bytes(text, 'UTF-8')
        padded_text = padder.update(b_text)+padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
        return encrypted_text

    @staticmethod
    def decrypt_text(encrypted_text: bytes, enc_symmetric: bytes,
                     private_key: rsa.RSAPrivateKey) -> str:
        """
        Static method for text decryption.

        Parameters:
            encrypted_text: bytes
              The encrypted text
            enc_symmetric: bytes
              Encrypted symmetric key
            private_key: rsa.RSAPrivateKey
              The private key of the asymmetric algorithm

        Returns:
            final_text: str
              Decrypted text
        """
        symmetric_key = private_key.decrypt(enc_symmetric, OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(
            encrypted_text) + decryptor.finalize()
        unpadder = ANSIX923(128).unpadder()
        unpadded_decrypted_text = unpadder.update(
            decrypted_text) + unpadder.finalize()
        final_text = unpadded_decrypted_text.decode('utf-8', errors='ignore')
        return final_text
 