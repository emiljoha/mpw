#!/usr/bin/python3
import pexpect # to test cli
from tests.testcases import load_test_cases
import pprint
import sys

num_tests_run = 0

def run_test_keyword_short(id, fullName, masterPassword, keyID, siteName,
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
        assert(result in output)
    else:
        output = child.read()
        child.close()
        assert(output == "Only Authentication key purpose is currrently supported\r\n")
        

def test_keyword_short():
    test_cases = load_test_cases('tests/testcases.xml')
    assert(len(test_cases) > 1)
    test_cases = [case for case in test_cases if 'keyContext' not in case]
    for case in test_cases:
        run_test_keyword_short(**case)


