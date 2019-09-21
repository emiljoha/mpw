#!/usr/bin/python3
import os # to get environment variables
import argparse # Parsing arguments
import mpwalg # The master password algorithm
import pyperclip # Copy to clipboard
import getpass # Password prompt
from argparse import RawTextHelpFormatter
import hashlib
import json
import copy

def parse_commandline_arguments(config_path_for_help_message):
    """Parse commandline argument and return namespace"""
    # Define what arguments to accept and with what help message and defaults.
    parser = argparse.ArgumentParser(
        description="""Generate passwords

JSON style configuration file can be found in %s
Parameters:
FULL_NAME: set default name to avoid specifying it every time.
""" % config_path_for_help_message,
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-u', '--full-name', type=str,
                        default=None,
                        help="Specify the full name of the user.\n"
                             "-u checks the master password against the config,\n"
                             "-U allows updating to a new master password.\n"
                             "Defaults to MPW_FULLNAME in env or prompts.\n")
    parser.add_argument('-c', '--counter', type=int,
                        help='Counter', default=1)
    parser.add_argument('-t', '--site-result-type', type=str, default="Long",
                        help = "Specify the password's template\n"
                        "Defaults to 'long' (-t a)\n"
                        "x, Maximum  | 20 characters, contains symbols.\n"
                        "l, Long     | Copy-friendly, 14 characters, symbols.\n"
                        "m, Medium   | Copy-friendly, 8 characters, symbols.\n"
                        "b, Basic    | 8 characters, no symbols.\n"
                        "s, Short    | Copy-friendly, 4 characters, no symbols.\n"
                        "i, Pin      | 4 numbers.\n"
                        "n, Name     | 9 letter name.\n"
                        "p, Phrase   | 20 character sentence.\n")
    parser.add_argument('-p', '--key-purpose', type=str, default="Authentication",
                        help="Purpose of site result.\n"
                        "Currently only Authentication is supported.\n"
                        "Comment on/create a issue on github for this to be fixed\n"
                        "if this is a problem to you.\n"
                        "One of: Authentication, [Identification, Recovery].\n")
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help="Increase output verbosity.\n")
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help="Decrease output verbosity.\n")
    parser.add_argument('site_name', type=str, nargs='?',
                        help='Name of the site for which to generate a token.', default=None)
    args = parser.parse_args()
    if not args.key_purpose == "Authentication":
        print("Only Authentication key purpose is currrently supported")
        quit()
    return args

def read_config(config_path):
    if 'HOME' in os.environ:
        try:
            config_file = open(config_path)
        except IOError:
            print("Warning: Failed to open config file")
            return dict()
        try:
            config = json.loads(config_file.read())
        except ValueError:
            print("Warning: Config file not valid json")
            return dict()
    else:
        print('Warning: Could not find HOME enviromental variable')
        return dict()
    return config

def write_config(config, config_path):
    f = open(config_path, 'w')
    f.write(json.dumps(config, indent=4))
    f.close()

def process_arguments(args, config):
    # Check if environment variables are set.
    if args.full_name is None:
        if 'FULL_NAME' in config:
            args.full_name = config['FULL_NAME']
        else:
            args.full_name = input('Full Name: ')
    if args.site_name is None:
        args.site_name = input('Site Name: ')
    short_site_result_type_dict = {'x': 'Maximum', 'l': 'Long', 'm': 'Medium', 'b': 'Basic',
                                   's': 'Short', 'i': 'PIN', 'n': 'Name', 'p': 'Phrase'}
    if args.site_result_type in short_site_result_type_dict:
        args.site_result_type = short_site_result_type_dict[args.site_result_type]
    return args

def update_config(args, config):
    new_config = copy.deepcopy(config)
    do_not_ask = 'ASK_TO_SET_DEFAULT_NAME' in config and config['ASK_TO_SET_DEFAULT_NAME'] == False
    if 'FULL_NAME' not in config and not do_not_ask:
        answer = input('Do you want to use this name as the default (y/n): ')
        if answer.lower() == 'y':
            new_config['FULL_NAME'] = args.full_name
        if answer.lower() == 'n':
            ask_again_answer = input('Do you want to to get this question the '
                                     'next time you run mpw (y/n): ')
            if ask_again_answer.lower() == 'n':
                new_config['ASK_TO_SET_DEFAULT_NAME'] = False
    return new_config

def generate_results(args, master_password):
    try:
        identicon = mpwalg.identicon(args.full_name, master_password)
        site_result = mpwalg.generate_password(args.full_name, master_password,
                                              args.site_name, args.counter,
                                              args.key_purpose,
                                              args.site_result_type)
        masterKey = mpwalg.masterKey(args.full_name, master_password,
                                    "Authentication")
        sha256 = hashlib.sha256()
        sha256.update(masterKey)
        masterKeyHash = sha256.hexdigest()
    except Exception as e:
        print("%s" % str(e))
        print("Error generating result, aborting")
        quit()
    return site_result, identicon, masterKeyHash

def print_results(site_result, identicon, args):
    # Print output.
    if args.verbose:
        print("""
    ------------------
    fullName         : %s
    siteName         : %s
    siteCounter      : %s
    resultType       : %s
    resultParam      : (null)
    keyPurpose       : %s
    keyContext       : (null)
    ------------------""" % (args.full_name, args.site_name,
                             args.counter, args.site_result_type,
                             args.key_purpose))
    if not args.quiet:
        print("[ %s ]: %s" % (identicon, site_result))


def main():
    run(os.environ['HOME'] + '/.config/mpw/config.json')

def main_snap():
    run(os.environ['SNAP_DATA'] + '/config.json')

def run(config_path):
    # Define and read commandline arguments. (Need config path for help message.)
    args = parse_commandline_arguments(config_path)
    # Look for environment variables or ask when missing information in arguments.
    config = read_config(config_path)
    args = process_arguments(args, config)
    new_config = update_config(args, config)
    write_config(new_config, config_path)
    # Get password from user.
    master_password = getpass.getpass()
    # Run the algorithm.
    site_result, identicon, masterKeyHash = generate_results(args, master_password)
    # Copy to clipboard
    try:
        pyperclip.copy(site_result)
    except pyperclip.PyperclipException as e:
        if not args.quiet:
            print("Warning: Could not find a copy/paste mechanism for your system.")
        if args.verbose:
            print(str(e))
    print_results(site_result, identicon, args)

if '__main__' == __name__:
    run('config.json')
