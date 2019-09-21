#!/usr/bin/python3
import pexpect # to test cli
from tests.testcases import load_test_cases
import pprint
import sys
import os

num_tests_run = 0

def is_ascii(s):
    maxAnsiCode = 127
    return all([c <= maxAnsiCode for c in s.encode()])

def clear_config():
    config_directory = os.environ['HOME'] + '/.config/mpw/'
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)
    with open(config_directory + 'config.json', 'w') as config:
        config.write('{}')

def run_test_keyword_short(fullName, masterPassword, siteName,
                           siteCounter, resultType, keyPurpose,
                           result, identicon):
    global num_tests_run
    arguments = locals()
    clear_config()
    spawn_command = 'mpw -u \"%s\" -c %s -t %s -p %s %s' % (fullName,
                                                            siteCounter,
                                                            resultType,
                                                            keyPurpose,
                                                            siteName)
    child = pexpect.spawnu(spawn_command)
    if keyPurpose == "Authentication":
        child.expect(r'Do you want to use this name as the default \(y/n\): ')
        child.sendline('y')
        child.expect("Password: ")
        child.sendline(masterPassword)
        output = child.read()
        child.close()
        assert(result in output)
        assert(identicon in output)
    else:
        output = child.read()
        child.close()
        assert("Only Authentication key purpose is currrently supported" in output)

def run_test_do_not_ask_again(fullName, masterPassword, siteName,
                              siteCounter, resultType, keyPurpose,
                              result, identicon):
    global num_tests_run
    arguments = locals()
    clear_config()
    spawn_command = 'mpw -u \"%s\" -c %s -t %s -p %s %s' % (fullName,
                                                            siteCounter,
                                                            resultType,
                                                            keyPurpose,
                                                            siteName)
    child = pexpect.spawnu(spawn_command)
    if keyPurpose == "Authentication":
        child.expect(r'Do you want to use this name as the default \(y/n\): ')
        child.sendline('n')
        child.expect(r'Do you want to to get this question the next time you run mpw \(y/n\): ')
        child.sendline('N')
        child.expect("Password: ")
        child.sendline(masterPassword)
        output = child.read()
        child.close()
        assert(result in output)
        assert(identicon in output)

        child = pexpect.spawnu(spawn_command)
        child.expect("Password: ")
        child.sendline(masterPassword)
        output = child.read()
        child.close()
        assert(result in output)
        assert(identicon in output)

    else:
        output = child.read()
        child.close()
        assert("Only Authentication key purpose is currrently supported" in output)

def run_test_set_password(fullName, masterPassword, siteName,
                          siteCounter, resultType, keyPurpose,
                          result, identicon):
    global num_tests_run
    arguments = locals()
    clear_config()
    spawn_command = 'mpw -u \"%s\" -c %s -t %s -p %s %s' % (fullName,
                                                            siteCounter,
                                                            resultType,
                                                            keyPurpose,
                                                            siteName)
    child = pexpect.spawnu(spawn_command)
    if keyPurpose == "Authentication":
        child.expect(r'Do you want to use this name as the default \(y/n\): ')
        child.sendline('Y')
        child.expect("Password: ")
        child.sendline(masterPassword)
        output = child.read()
        child.close()
        assert(result in output)
        assert(identicon in output)
        child = pexpect.spawnu('mpw -c %s -t %s -p %s %s' % (siteCounter,
                                                             resultType,
                                                             keyPurpose,
                                                             siteName))
        child.expect("Password: ")
        child.sendline(masterPassword)
        output = child.read()
        child.close()
        assert(result in output)
        assert(identicon in output)
    else:
        output = child.read()
        child.close()
        assert("Only Authentication key purpose is currrently supported" in output)

def test_keyword_short():
    test_cases = [case for case in load_test_cases('tests/testcases.xml') if
                  ('keyContext' not in case) and
                  (case['algorithm'] == 3)]
    assert(len(test_cases) > 1)
    for case in test_cases:
        run_test_keyword_short(case['fullName'], case['masterPassword'],
                               case['siteName'], case['siteCounter'],
                               case['resultType'], case['keyPurpose'],
                               case['result'], case['identicon'])
        run_test_do_not_ask_again(case['fullName'], case['masterPassword'],
                                  case['siteName'], case['siteCounter'],
                                  case['resultType'], case['keyPurpose'],
                                  case['result'], case['identicon'])
        run_test_set_password(case['fullName'], case['masterPassword'],
                              case['siteName'], case['siteCounter'],
                              case['resultType'], case['keyPurpose'],
                              case['result'], case['identicon'])
