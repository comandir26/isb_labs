from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import hashes


class Assymetric:
    """
    A class that implements an assymmetric encryption algorithm

    Attributes:
        None

    Methods:
        generate_keys():
          Generates keys for an asymmetric algorithm
        encrypt_key(symmetric_key, public_key):
          Encrypts the key using an assymmetric algorithm
        decrypt_text(enc_symmetric, private_key):
          Decrypts the key using an assymmetric algorithm
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
    def generate_keys():
        """
        Static method for generating keys for an asymmetric algorithm

        Parameters:
            None

        Returns:
            (private_key, public_key): Tuple[rsa.RSAPrivateKey,rsa.RSAPublicKey]
              A tuple of keys(private key, public key)
        """
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        return private_key, public_key
    
    @staticmethod
    def encrypt_key(symmetric_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
        """
        Static method for key encryption.

        Parameters:
            symmetric_key: bytes
              The source symmetric key
            public_key: rsa.RSAPublicKey
              The public key of the asymmetric algorithm

        Returns:
            enc_symmetric: bytes
              Encrypted symmetric key
        """
        enc_symmetric = public_key.encrypt(symmetric_key, OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return enc_symmetric

    @staticmethod
    def decrypt_key(enc_symmetric: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
        """
        Static method for key decryption.

        Parameters:
            enc_symmetric: bytes
              Encrypted symmetric key
            private_key: rsa.RSAPrivateKey
              The private key of the asymmetric algorithm

        Returns:
            symmetric_key: bytes
              Decrypted symmetric key
        """
        symmetric_key = private_key.decrypt(enc_symmetric, OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return symmetric_key
     