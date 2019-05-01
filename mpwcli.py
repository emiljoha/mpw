#!/usr/bin/python3
import os # to get environment variables
import argparse # Parsing arguments
import pympw # The master password algorithm
import pyperclip # Copy to clipboard
import getpass # Password prompt
from argparse import RawTextHelpFormatter
import hashlib
import json
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
        args.site_result_type = short_site_result_type_dict[args.pw_type]
    return args


def generate_results(args, master_password):
    try:
        identicon = pympw.identicon(args.full_name, master_password)
        site_result = pympw.generate_password(args.full_name, master_password,
                                              args.site_name, args.counter,
                                              args.key_purpose,
                                              args.site_result_type)
        masterKey = pympw.masterKey(args.full_name, master_password,
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
