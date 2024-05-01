import argparse
import os
import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.padding import ANSIX923
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Cryptosystem:
    def __init__(self, mode):
        self.mode = mode
    def generate_keys(self, path_to_sym, path_to_public, path_to_private, key_length):
        symmetric_key = os.urandom(key_length)#5-16 байт
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        enc_symmetric = public_key.encrypt(symmetric_key, OAEP(mgf=
                                            MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        with open(path_to_sym, 'wb') as f:
            f.write(enc_symmetric)
        with open(path_to_public, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PublicFormat.SubjectPublicKeyInfo))
        with open(path_to_private, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                encryption_algorithm=serialization.NoEncryption()))
            
    def encrypt_text(self, path_to_text, path_to_private, path_to_symmetric, path_to_encrypted, path_to_decrypted):
        with open(path_to_private, 'rb') as pem_in:
            private_bytes = pem_in.read()
        private_key = load_pem_private_key(private_bytes,password=None)

        with open(path_to_symmetric, 'rb') as f:
            encrypted_sym = f.read()

        symmetric_key = private_key.decrypt(encrypted_sym,OAEP(mgf=MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        len_key = len(symmetric_key)
        with open(path_to_text, 'r', encoding='utf-8') as f:
            text = f.read()
        
        padder = ANSIX923(128).padder()
        b_text = bytes(text, 'UTF-8')
        padded_text = padder.update(b_text)+padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()

        with open(path_to_encrypted, 'wb') as f:
            f.write(encrypted_text)

        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()

        unpadder = ANSIX923(128).unpadder()
        unpadded_decrypted_text = unpadder.update(decrypted_text) + unpadder.finalize()
        final_text = unpadded_decrypted_text.decode('UTF-8')

        with open(path_to_decrypted, 'w', encoding='utf-8') as f:
            f.write(final_text)
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Гибридная криптосистема')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help = 'Генерация ключей', action = 'store_true')
    group.add_argument('-enc', '--encryption', help = 'Шифрование', action = 'store_true')
    group.add_argument('-dec', '--decryption', help = 'Дешифрование', action = 'store_true')
    parser.add_argument('settings', type = str, help = 'File with settings')
    parser.add_argument('key_length', type = int, help = 'Key length for symmetric encryption')
    args = parser.parse_args()
    
    if args.generation is not None:
        with open(args.settings, 'r') as json_file:
            settings = json.load(json_file)
        key_length = args.key_length
        enc = Cryptosystem(mode = 'gen')
        enc.generate_keys(settings['symmetric_key'], settings['public_key'], settings['private_key'], key_length)
        print('Успешно!')
    
    elif args.encryption is not None:
        with open(args.settings, 'r') as json_file:
            settings = json.load(json_file)
        enc=Cryptosystem(mode = 'enc')
        enc.encrypt_text(settings['source_text'], settings['private_key'], settings['symmetric_key'], settings['encrypted_text'], settings['decrypted_text'])
        print('Успешно!')
    else:
        print(f'Дешифрование {args.settings}')