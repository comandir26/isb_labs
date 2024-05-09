import argparse
import sys

import files

from symmetric import Symmetric
from assymetric import Assymetric


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Gybrid cryptosystem. Specify '
                                                  'settings=settings.json to run the program with the set parameters. '
                                                  'If you want to save the keys along your path, specify the -sym, '
                                                  '-pub, -priv and -key options if you want. If you want to encrypt '
                                                  'your text, specify the parameters -sym, -priv, -text, -enc_text. '
                                                  'If you want to decrypt your text, specify the parameters - sym, '
                                                  '-priv, -dec_text, -enc_text'))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation',
                       help='Key generation', action='store_true')
    group.add_argument('-enc', '--encryption',
                       help='Encryption', action='store_true')
    group.add_argument('-dec', '--decryption',
                       help='Decryption', action='store_true')
    parser.add_argument('-settings', '--settings', type=str,
                        default=None, help='File with settings')
    parser.add_argument('-key', '--key_length', type=int, default=8, 
                        help='Key length for symmetric encryption CAST5, \
                        40 to 128 bits in length in increments of 8 bits. \
                        Possible values: 5, 6, 7, 8, ... 15, 16. Default = 8.')
    parser.add_argument('-sym', '--user_symmetric_key_path',
                        type=str, default=None, help='User path to symmetric key')
    parser.add_argument('-pub', '--user_public_key_path',
                        type=str, default=None, help='User path to public key')
    parser.add_argument('-priv', '--user_private_key_path',
                        type=str, default=None, help='User path to private key')
    parser.add_argument('-text', '--user_text_path', type=str,
                        default=None, help='User path to text')
    parser.add_argument('-enc_text', '--user_enc_text_path', type=str,
                        default=None, help='User path to encrypted text')
    parser.add_argument('-dec_text', '--user_dec_text_path', type=str,
                        default=None, help='User path to decrypted text')
    args = parser.parse_args()
    match args:
        case args if args.generation:
            key_length = args.key_length
            if key_length < 5 or key_length > 16:
                print("Unsuitable symmetric encryption key size")
                sys.exit()
            symmetric = Symmetric.generate_key(key_length)
            private, public = Assymetric.generate_keys()
            enc_symmetric = Assymetric.encrypt_key(symmetric, public)
            if args.user_symmetric_key_path and args.user_public_key_path \
                    and args.user_private_key_path:
                path_to_symmetric = args.user_symmetric_key_path
                path_to_public = args.user_public_key_path
                path_to_private = args.user_private_key_path
            elif args.settings:
                settings = files.read_json(args.settings)
                path_to_symmetric = settings.get('symmetric_key')
                path_to_public = settings.get('public_key')
                path_to_private = settings.get('private_key')
            if not path_to_symmetric or not path_to_public or not path_to_private:
                print('No paths to save were found, check the parameter names')
                sys.exit()
            files.save_bytes(path_to_symmetric, enc_symmetric)
            files.save_public_key(path_to_public, public)
            files.save_private_key(path_to_private, private)
            print("Key generation and saving completed successfully")
        case args if args.encryption:
            if args.user_text_path and args.user_symmetric_key_path \
                    and args.user_private_key_path and args.user_enc_text_path:
                path_to_text = args.user_text_path
                path_to_private = args.user_private_key_path
                path_to_symmetric = args.user_symmetric_key_path
                path_to_encrypted = args.user_enc_text_path
            elif args.settings:
                settings = files.read_json(args.settings)
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
            enc_symmetric = files.read_bytes(path_to_symmetric)
            dec_symmetric = Assymetric.decrypt_key(enc_symmetric, private)
            encrypted_text = Symmetric.encrypt_text(text, dec_symmetric)
            files.save_bytes(path_to_encrypted, encrypted_text)
            print('The encryption and saving of the text were completed successfully')
        case args if args.decryption:
            if args.user_dec_text_path and args.user_symmetric_key_path \
                    and args.user_private_key_path and args.user_enc_text_path:
                path_to_encrypted = args.user_enc_text_path
                path_to_private = args.user_private_key_path
                path_to_symmetric = args.user_symmetric_key_path
                path_to_decrypted = args.user_dec_text_path
            elif args.settings:
                settings = files.read_json(args.settings)
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
            enc_symmetric = files.read_bytes(path_to_symmetric)
            dec_symmetric = Assymetric.decrypt_key(enc_symmetric, private)
            decrypted_text = Symmetric.decrypt_text(
                encrypted_text, dec_symmetric)
            files.save_text(path_to_decrypted, decrypted_text)
            print('Decryption and saving were completed successfully')
             