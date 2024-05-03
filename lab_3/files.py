import json

from typing import Optional, Dict

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def read_json(path_to_data: str) -> Optional[Dict[str, str]]:
    """
    This function reads data in json format at the specified path.

    Parameters:
        path_to_data: str
          The path to the data

    Returns:
        data: Optional[Dict[str, str]]
          The read data or None
    """
    try:
        with open(path_to_data, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = None
    finally:
        return data


def read_bytes(path_to_data: str) -> Optional[bytes]:
    """
    This function reads data in bytes format at the specified path, 
    it can be the encrypted text or the encrypted symmetric key.

    Parameters:
        path_to_data: str
          The path to the data

    Returns:
        data: Optional[bytes]
          The read data or None
    """
    try:
        with open(path_to_data, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        data = None
    finally:
        return data


def read_text(path_to_text: str) -> Optional[str]:
    """
    This function reads text at the specified path.

    Parameters:
        path_to_text: str
          The path to the text

    Returns:
        text: Optional[str]
          The read text or None
    """
    try:
        with open(path_to_text, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        text = None
    finally:
        return text


def save_text(path_to_save: str, text: str) -> bool:
    """
    This function saves text at the specified path.

    Parameters:
        path_to_save: str
          The path to save the text
        text: str
          The text to save

    Returns:
        saved: bool
          An indicator showing whether the text has been saved
    """
    saved = True
    try:
        with open(path_to_save, 'w', encoding='utf-8') as f:
            f.write(text)
    except FileNotFoundError:
        saved = False
    finally:
        return saved


def save_bytes(path_to_save: str, data: bytes) -> bool:
    """
    This function saves the data in bytes format in the specified path,
    it can be the encrypted text or the encrypted symmetric key.

    Parameters:
        path_to_save: str
          The path to save the data
        data: bytes
          The data to save

    Returns:
        saved: bool
          An indicator showing whether the data has been saved
    """
    saved = True
    try:
        with open(path_to_save, 'wb') as f:
            f.write(data)
    except FileNotFoundError:
        saved = False
    finally:
        return saved


def save_public_key(path_to_save: str, public_key: rsa.RSAPublicKey) -> bool:
    """
    This function saves the public key in the specified path.

    Parameters:
        path_to_save: str
          The path to save the key
        public_key: rsa.RSAPublicKey
          The key to save

    Returns:
        saved: bool
          An indicator showing whether the key has been saved
    """
    saved = True
    try:
        with open(path_to_save, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo))
    except FileNotFoundError:
        saved = False
    finally:
        return saved


def save_private_key(path_to_save: str, private_key: rsa.RSAPrivateKey) -> bool:
    """
    This function saves the private key in the specified path.

    Parameters:
        path_to_save: str
          The path to save the key
        private_key: rsa.RSAPrivateKey
          The key to save

    Returns:
        saved: bool
          An indicator showing whether the key has been saved
    """
    saved = True
    try:
        with open(path_to_save, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption()))
    except FileNotFoundError:
        saved = False
    finally:
        return saved


def read_private_key(path_to_key: str) -> Optional[rsa.RSAPrivateKey]:
    """
    This function reads the private key at the specified path.

    Parameters:
        path_to_key: str
          The path to the key

    Returns:
        key: Optional[rsa.RSAPrivateKey]
          The read key or None
    """
    try:
        with open(path_to_key, 'rb') as pem_in:
            private_bytes = pem_in.read()
        key = load_pem_private_key(private_bytes, password=None)
    except FileNotFoundError:
        key = None
    finally:
        return key
 