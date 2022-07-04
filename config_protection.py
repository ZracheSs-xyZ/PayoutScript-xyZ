"""
author: EtWnn, https://github.com/EtWnn

Contains encryption functions to protect the private keys written in the configuration file of this project
"""
import base64
import json
import os
from getpass import getpass
from typing import Union, Dict

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_FILE = 'salt.bytes'
CONFIG_FILE = 'config.bytes'
CLEAR_CONFIG_FILE = 'clear_config.json'


def get_salt() -> bytes:
    """
    Return the salt for the hash generation
    If no salt file is found, generate a new one

    :return: salt as bytes
    :rtype: bytes
    """
    try:
        with open(SALT_FILE, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print("Generating salt")
    salt = os.urandom(16)
    with open('salt.bytes', 'wb') as file:
        file.write(salt)
    return salt


def get_derived_key(password: Union[str, bytes]) -> Fernet:
    """
    Generate a proper encryption key from a salt and a password

    :param password: user password
    :type password: Union[str, bytes]
    :return: fernet key
    :rtype: Fernet
    """
    salt = get_salt()

    if isinstance(password, str):
        password = bytes(password, encoding='utf8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)


def write_file(content: Union[str, bytes], file_path: str, key: Fernet):
    """
    Encrypt content and write to a file

    :param content: content to write on the file
    :type content: Union[str, bytes]
    :param file_path: path of the file
    :type file_path: str
    :param key: key for encryption
    :type key: Fernel
    """
    if isinstance(content, str):
        content = bytes(content, encoding='utf8')

    encrypted_content = key.encrypt(content)
    with open(file_path, 'wb') as file:
        file.write(encrypted_content)


def read_file(file_path: str, key: Fernet) -> bytes:
    """
    Decrypt the content of a file

    :param file_path: path of the file
    :type file_path: str
    :param key: key for decryption
    :type key: Fernel
    :return: decrypted content
    :rtype: bytes
    """
    with open(file_path, 'rb') as file:
        encrypted_content = file.read()

    return key.decrypt(encrypted_content)


def get_config() -> Dict:
    """
    Decrypt the config and return it as a json format

    :return: config as a json
    :rtype: Dict
    """
    user_password = getpass("To decrypt the configuration, please enter your password (input will be hidden):")
    key = get_derived_key(user_password)
    try:
        content = read_file(CONFIG_FILE, key)
    except FileNotFoundError:
        msg = """
No configuration has been set yet. You need to set one up with your scholars and accounts information.
Please create one with the command: python config.py --create
        """
        raise RuntimeError(msg)
    return json.loads(content.decode("utf-8"))


def write_config(config: Dict):
    """
    Encrypt the config and write it in file

    :param config: configuration as a json
    :type config: Dict
    """
    user_password = ""
    confirmed_password = "!"
    while user_password != confirmed_password:
        user_password = getpass("\nTo encrypt the configuration, please enter your password (input will be hidden):")
        confirmed_password = getpass("Please confirm your password (input will be hidden):")
        if confirmed_password != user_password:
            print("Passwords do not match, please retry")
    key = get_derived_key(user_password)
    content = json.dumps(config)
    write_file(content, CONFIG_FILE, key)


def write_encrypted_to_clear():
    """
    Decrypt the config file and write it as a clear file

    """
    content = get_config()

    msg = """
WARNING:
    You are about to decrypt the configuration file and write it in a raw format.
    Private keys will be visible!
Are your sure? (y/n):"""
    if input(msg) != "y":
        return

    with open(CLEAR_CONFIG_FILE, 'w') as file:
        json.dump(content, file, indent=4)

    print(f"{CLEAR_CONFIG_FILE} File written")


def write_clear_to_encrypted(file_path: str):
    """
    Read a clear config file and encrypt it
    This can be useful to switch from the old configuration file to the encrypted one

    """
    with open(file_path, 'rb') as file:
        clear_content = json.load(file)
    expected_keys = ['Name', 'PrivateKey', 'AccountAddress', 'ScholarPayoutAddress', 'ScholarPayoutPercentage']
    try:
        clean_content = {
            'AcademyPayoutAddress': clear_content['AcademyPayoutAddress'],
            'Scholars': [
                {k: scholar[k] for k in expected_keys} for scholar in clear_content['Scholars']
            ]
        }
    except KeyError:
        print("The provided file do not have the right configuration format, conversion FAILED")
        return
    write_config(clean_content)

    print(f"Encrypted config file written")
    if input("Would you like to delete the clear file? (y/n):") == "y":
        os.remove(file_path)
        print(f"File {file_path} deleted")
