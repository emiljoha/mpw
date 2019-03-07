#!/usr/bin/python3
import pexpect # to test cli
import re
from tests.testcases import load_test_cases
import pprint
import sys

num_tests_run = 0

def run_test_keyword_short(id, fullName, masterPassword, keyID, siteName,
                           siteCounter, resultType, keyPurpose, result):
    global num_tests_run
    arguments = locals()
    try:
        spawn_command = 'mpw -u \"%s\" -c %s -t %s -p %s %s' % (fullName,
                                                                siteCounter,
                                                                resultType,
                                                                keyPurpose,
                                                                siteName)
        child = pexpect.spawnu(spawn_command)
        child.expect("Password: ")
        child.sendline(masterPassword)
        child.expect(re.escape(result))
        child.close()
        num_tests_run += 1
        sys.stdout.write("Number of tests run: %s\r" % num_tests_run)
        sys.stdout.flush()
    except Exception as e:
        print("Test: %s failed.\n" % id)
        pprint.pprint(arguments)
        print("spawn command: %s" % spawn_command)
        print(e)
        return False
    return True


def test_keyword_short():
    test_cases = load_test_cases('tests/testcases.xml')
    test_cases = [case for case in test_cases if 'keyContext' not in case]
    # passed = [run_test_keyword_short(**case) for case in test_cases]
    # print('Number of passed Tests: %s\n' % len([case for case in passed if case is True]))
    # print('Number of failed Tests: %s\n' % len([case for case in passed if case is False]))


