import os

from cryptography.hazmat.primitives.padding import ANSIX923
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Symmetric:
    """
    A class that implements a symmetric encryption algorithm

    Attributes:
        None

    Methods:
        generate_key(key_length):
          Generate key for a symmetric algorithm
        encrypt_text(text, symmetric_key):
          Encrypts the text using a symmetric key
        decrypt_text(encrypted_text, symmetric_key):
          Decrypts the text using a symmetric key
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
    def generate_key(key_length: int) -> bytes:
        """
        Static method for generating key for a symmetric algorithm.

        Parameters:
            key_length: int
              Key length for the symmetric algorithm

        Returns:
            symmetric_key: bytes
              Key for a symmetric algorithm
        """
        symmetric_key = os.urandom(key_length)
        return symmetric_key
    
    @staticmethod
    def encrypt_text(text: str, symmetric_key: bytes) -> bytes:
        """
        Static method for text encryption.

        Parameters:
            text: str
              The source text
            symmetric_key: bytes
              Key for a symmetric algorithm

        Returns:
            encrypted_text: bytes
              Encrypted text
        """
        padder = ANSIX923(128).padder()
        b_text = bytes(text, 'UTF-8')
        padded_text = padder.update(b_text)+padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
        return encrypted_text
    
    @staticmethod
    def decrypt_text(encrypted_text: bytes, symmetric_key: bytes) -> str:
        """
        Static method for text decryption.

        Parameters:
            encrypted_text: bytes
              The encrypted text
            symmetric_key: bytes
              Key for a symmetric algorithm

        Returns:
            final_text: str
              Decrypted text
        """
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
     