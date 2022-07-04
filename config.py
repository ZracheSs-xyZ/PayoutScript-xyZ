"""
author: EtWnn, https://github.com/EtWnn

helper to create / edit / delete the configuration file
"""
import argparse
import pprint
from getpass import getpass
from typing import Dict

import config_protection as cfgp


def get_empty_config() -> Dict:
    """
    Create and return an empty configuration

    :return: empty configuration
    :rtype: Dict
    """
    return {
        'AcademyPayoutAddress': '',
        'Scholars': []
    }


def input_scholar_info() -> Dict:
    """
    Handle communication to ask the user to enter scholar information

    :return: scholar information as a scholar
    :rtype: Dict
    """
    print("Enter all needed information for the scholar payout:")
    res = {
        'Name': input("\t-Enter the scholar name:"),
        'AccountAddress': input("\t-Enter the scholarship account address (ex: ronin:<....>):"),
        'PrivateKey': getpass("\t-Enter the scholarship private key (ex: 0x:<....>, input will be hidden):"),
        'ScholarPayoutAddress': input("\t-Enter the scholar payout address (ex: ronin:<....>):")
    }
    while 'ScholarPayoutPercentage' not in res:
        try:
            res['ScholarPayoutPercentage'] = float(input("\t-Enter the scholar payout ratio (between 0 and 1, ex: 0.5):"))
        except ValueError:
            print("Invalid type, please retry")

    return res


def add_new_scholars(config: Dict) -> Dict:
    """
    Add as many new scholars as needed

    :param config: config to add scholars to
    :type config: Dict
    :return: config
    :rtype: Dict
    """
    add_new_scholar = True
    while add_new_scholar:
        scholar_info = input_scholar_info()
        print("\nYour entered the following info:")
        for k, v in scholar_info.items():
            print(f"\t{k}: {v}")
        if input("\nDo you want to add the above information to your scholar payout config? (y/n):") == 'y':
            config['Scholars'].append(scholar_info)
            print("Scholar info added")
        else:
            print("Scholar info ignored")
        add_new_scholar = (input("\nDo you want to add a new scholar? (y/n):") == 'y')
    return config


def delete_scholars(config: Dict) -> Dict:
    """
    Delete as many new scholars as needed

    :param config: config to delete scholars from
    :type config: Dict
    :return: config
    :rtype: Dict
    """
    delete_scholar = True
    while delete_scholar:
        print("Here are the current scholar information:")
        for i, scholar in enumerate(config['Scholars']):
            print(f" #{i}:\n\tName: {scholar['Name']}\n\tScholar Payout address: {scholar['ScholarPayoutAddress']}")
        i_scholar = None
        while i_scholar is None and len(config['Scholars']):
            try:
                i_scholar = int(input("\nEnter the number of the scholar you want to delete:"))
                if i_scholar >= len(config['Scholars']) or i_scholar < 0:
                    raise ValueError
            except ValueError:
                print("Invalid input")
        scholar_info = config['Scholars'][i_scholar]
        for k, v in scholar_info.items():
            print(f"\t{k}: {v}")
        if input("\nDo you want to remove the above information from your scholar payout config? (y/n):") == 'y':
            config['Scholars'].remove(scholar_info)
            print("Scholar deleted")
        else:
            print("Scholar deletion ignored")
        delete_scholar = (input("\nDo you want to delete another scholar? (y/n):") == 'y')
    return config


def edit_academy_payout(config: Dict) -> Dict:
    """
    Edit the address for the academy payout

    :param config: config to edit
    :type config: Dict
    :return: edited config
    :rtype: Dict
    """
    confirmed = False
    if config['AcademyPayoutAddress']:
        print("\nCurrent academy payout address:", config['AcademyPayoutAddress'])
    while not confirmed:
        config['AcademyPayoutAddress'] = input('\nPlease enter the academy payout address (ex: ronin:<....>):')
        print("You entered the address:", config['AcademyPayoutAddress'])
        confirmed = (input("Do you confirm it? (y/n):") == 'y')
    return config


def create_new_config() -> Dict:
    """
    Guide the user through a config file creation

    :return: config
    :rtype: Dict
    """
    print("### Creation of a new configuration ###")
    config = get_empty_config()
    config = edit_academy_payout(config)
    return add_new_scholars(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create / Edit the configuration for the payout')
    parser.add_argument('--display', required=False,
                        help='Display the current config', action="store_true")
    parser.add_argument('--create', required=False,
                        help='Create a new configuration (will overwrite)', action="store_true")
    parser.add_argument('--add', required=False,
                        help='Add new scholars to the config', action="store_true")
    parser.add_argument('--delete', required=False,
                        help='Delete scholars from the config', action="store_true")
    parser.add_argument('--academy', required=False,
                        help='Edit the academy payout address', action="store_true")
    parser.add_argument('--convert_clear', metavar="file_path", required=False,
                        help='Convert a clear json config to an encrypted config (will overwrite)', type=str)
    parser.add_argument('--reveal_encrypt', action="store_true", required=False,
                        help='Convert the encrypted config to a clear json config')
    args = parser.parse_args()
    if args.create:
        new_config = create_new_config()
        cfgp.write_config(new_config)
    if args.add:
        current_config = cfgp.get_config()
        new_config = add_new_scholars(current_config)
        cfgp.write_config(new_config)
    if args.delete:
        current_config = cfgp.get_config()
        new_config = delete_scholars(current_config)
        cfgp.write_config(new_config)
    if args.academy:
        current_config = cfgp.get_config()
        new_config = edit_academy_payout(current_config)
        cfgp.write_config(new_config)
    if args.convert_clear:
        cfgp.write_clear_to_encrypted(args.convert_clear)
    if args.reveal_encrypt:
        cfgp.write_encrypted_to_clear()
    if args.display:
        current_config = cfgp.get_config()
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(current_config)
