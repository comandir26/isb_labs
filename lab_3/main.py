import argparse
import os
import sys

from typing import Tuple

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.padding import ANSIX923
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import files


class Cryptosystem:
    def __init__(self):
        pass
    def generate_keys(self, key_length) -> Tuple[bytes, rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        symmetric_key = os.urandom(key_length)
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        enc_symmetric = public_key.encrypt(symmetric_key, OAEP(mgf=
                                            MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return enc_symmetric, private_key, public_key
    

    def encrypt_text(self, text, encrypted_sym, private_key):
        symmetric_key = private_key.decrypt(encrypted_sym,OAEP(mgf=MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        padder = ANSIX923(128).padder()
        b_text = bytes(text, 'UTF-8')
        padded_text = padder.update(b_text)+padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()
        return encrypted_text
        

    def decrypt_text(self, encrypted_text, encrypted_sym, private_key):
        symmetric_key = private_key.decrypt(encrypted_sym,OAEP(mgf=MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()
        unpadder = ANSIX923(128).unpadder()
        unpadded_decrypted_text = unpadder.update(decrypted_text) + unpadder.finalize()
        final_text = unpadded_decrypted_text.decode('utf-8', errors='ignore')
        return final_text
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Гибридная криптосистема')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help = 'Генерация ключей', action = 'store_true')
    group.add_argument('-enc', '--encryption', help = 'Шифрование', action = 'store_true')
    group.add_argument('-dec', '--decryption', help = 'Дешифрование', action = 'store_true')
    parser.add_argument('settings', type = str, help = 'File with settings')
    parser.add_argument('key_length', type = int, help = 'Key length for symmetric \
                        encryption CAST5, 40 to 128 bits (5 to 16 bytes) in length \
                        in increments of 8 bits(5, 6, 7, 8, ... 15, 16)')
    args = parser.parse_args()
    if args.generation:
        settings = files.read_json(args.settings)
        if settings is None:
            print("Файл с параметрами не найден")
            sys.exit()
        key_length = args.key_length
        if key_length < 5 or key_length > 16:
            print("Неподходящий размер ключа симметричного шифрования")
            sys.exit()
        system = Cryptosystem()
        symmetric, private, public = system.generate_keys(key_length)
        path_to_symmetric = settings.get('symmetric_key')
        path_to_public = settings.get('public_key')
        path_to_private = settings.get('private_key')
        if not path_to_symmetric or not path_to_public or not path_to_private:
            print('Пути для сохранения не найдены, проверьте имена параметров')
            sys.exit()
        files.save_bytes(path_to_symmetric, symmetric) 
        files.save_public_key(path_to_public, public)
        files.save_private_key(path_to_private, private)
        print("Генерация и сохранение ключей успешно завершены")
    elif args.encryption:
        settings = files.read_json(args.settings)
        if settings is None:
            print("Файл с параметрами не найден")
            sys.exit()
        system=Cryptosystem()
        path_to_text = settings.get('source_text')
        path_to_private = settings.get('private_key')
        path_to_symmetric = settings.get('symmetric_key')
        path_to_encrypted = settings.get('encrypted_text')
        if not path_to_text or not path_to_private or not path_to_symmetric or not path_to_encrypted:
            print('Пути не найдены, проверьте имена параметров')
            sys.exit()
        text = files.read_text(path_to_text)
        private = files.read_private_key(path_to_private)
        symmetric = files.read_bytes(path_to_symmetric)
        encrypted_text = system.encrypt_text(text, symmetric, private)
        files.save_bytes(path_to_encrypted, encrypted_text)
        print('Шифрование и сохранение текста выполнены успешно')
    else:
        settings = files.read_json(args.settings)
        if settings is None:
            print("Файл с параметрами не найден")
            sys.exit()
        system=Cryptosystem()
        path_to_encrypted = settings.get('encrypted_text')
        path_to_private = settings.get('private_key')
        path_to_symmetric = settings.get('symmetric_key')
        path_to_decrypted = settings.get('decrypted_text')
        if not path_to_encrypted or not path_to_private or not path_to_symmetric or not path_to_decrypted:
            print('Пути не найдены, проверьте имена параметров')
            sys.exit()
        encrypted_text = files.read_bytes(path_to_encrypted)
        private = files.read_private_key(path_to_private)
        symmetric = files.read_bytes(path_to_symmetric)
        decrypted_text = system.decrypt_text(encrypted_text, symmetric, private)
        files.save_text(path_to_decrypted, decrypted_text)
        print('Расшифровка и сохранение выполнены успешно')
         