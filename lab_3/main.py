import argparse
import sys

import files

from cryptosystem import Cryptosystem


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gybrid cryptosystem')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation',
                       help='Key generation', action='store_true')
    group.add_argument('-enc', '--encryption',
                       help='Encryption', action='store_true')
    group.add_argument('-dec', '--decryption',
                       help='Decryption', action='store_true')
    parser.add_argument('settings', type=str, help='File with settings')
    parser.add_argument('-key', '--key_length', type=int, default=8, help='Key length for symmetric \
                        encryption CAST5, 40 to 128 bits in length in \
                        increments of 8 bits. Possible values: 5, 6, 7, 8, ... 15, 16. Default = 8.')
    args = parser.parse_args()
    if args.generation:
        settings = files.read_json(args.settings)
        if settings is None:
            print("The file with the parameters was not found")
            sys.exit()
        key_length = args.key_length
        if key_length < 5 or key_length > 16:
            print("Unsuitable symmetric encryption key size")
            sys.exit()
        symmetric, private, public = Cryptosystem.generate_keys(key_length)
        path_to_symmetric = settings.get('symmetric_key')
        path_to_public = settings.get('public_key')
        path_to_private = settings.get('private_key')
        if not path_to_symmetric or not path_to_public or not path_to_private:
            print('No paths to save were found, check the parameter names')
            sys.exit()
        files.save_bytes(path_to_symmetric, symmetric)
        files.save_public_key(path_to_public, public)
        files.save_private_key(path_to_private, private)
        print("Key generation and saving completed successfully")
    elif args.encryption:
        settings = files.read_json(args.settings)
        if settings is None:
            print("The file with the parameters was not found")
            sys.exit()
        path_to_text = settings.get('source_text')
        path_to_private = settings.get('private_key')
        path_to_symmetric = settings.get('symmetric_key')
        path_to_encrypted = settings.get('encrypted_text')
        if not path_to_text or not path_to_private or \
                not path_to_symmetric or not path_to_encrypted:
            print('No paths found, check the parameter names')
            sys.exit()
        text = files.read_text(path_to_text)
        private = files.read_private_key(path_to_private)
        symmetric = files.read_bytes(path_to_symmetric)
        encrypted_text = Cryptosystem.encrypt_text(text, symmetric, private)
        files.save_bytes(path_to_encrypted, encrypted_text)
        print('The encryption and saving of the text were completed successfully')
    else:
        settings = files.read_json(args.settings)
        if settings is None:
            print("he file with the parameters was not found")
            sys.exit()
        path_to_encrypted = settings.get('encrypted_text')
        path_to_private = settings.get('private_key')
        path_to_symmetric = settings.get('symmetric_key')
        path_to_decrypted = settings.get('decrypted_text')
        if not path_to_encrypted or not path_to_private or \
                not path_to_symmetric or not path_to_decrypted:
            print('No paths found, check the parameter names')
            sys.exit()
        encrypted_text = files.read_bytes(path_to_encrypted)
        private = files.read_private_key(path_to_private)
        symmetric = files.read_bytes(path_to_symmetric)
        decrypted_text = Cryptosystem.decrypt_text(encrypted_text, symmetric, private)
        files.save_text(path_to_decrypted, decrypted_text)
        print('Decryption and saving were completed successfully')
 