#!/usr/bin/python3
import pexpect # to test cli
from tests.testcases import load_test_cases
import pprint
import sys

num_tests_run = 0

def is_ascii(s):
    maxAnsiCode = 127
    return all([c <= maxAnsiCode for c in s.encode()])

def run_test_keyword_short(fullName, masterPassword, siteName,
                           siteCounter, resultType, keyPurpose, result):
    global num_tests_run
    arguments = locals()
    spawn_command = 'mpw -u \"%s\" -c %s -t %s -p %s %s' % (fullName,
                                                            siteCounter,
                                                            resultType,
                                                            keyPurpose,
                                                            siteName)
    child = pexpect.spawnu(spawn_command)
    if keyPurpose == "Authentication":
        child.expect("Password: ")
        child.sendline(masterPassword)
        output = child.read()
        child.close()
        if not all([is_ascii(fullName), is_ascii(siteName),
                   is_ascii(masterPassword)]):
            assert("Error generating result, aborting" in output)
            if not is_ascii(fullName):
                assert("Name contains characters that are not ascii" in output)
            if not is_ascii(masterPassword):
                assert("Password contains characters that are not ascii" in output)
            if not is_ascii(siteName):
                assert("Site name contains characters that are not ascii" in output)
        else:
            assert(result in output)
    elif keyPurpose == "Authentication":
        output = child.read()
        child.close()
        assert(output == "Only Authentication key purpose is currrently supported\r\n")
        output = child.read()
        child.close()

def test_keyword_short():
    test_cases = [case for case in load_test_cases('tests/testcases.xml') if
                  ('keyContext' not in case) and
                  (case['algorithm'] == 3)]
    assert(len(test_cases) > 1)
    for case in test_cases:
        run_test_keyword_short(case['fullName'], case['masterPassword'],
                               case['siteName'], case['siteCounter'],
                               case['resultType'], case['keyPurpose'],
                               case['result'])
