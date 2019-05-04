#!/usr/bin/python3
import pexpect # to test cli
try:
    from tests.testcases import load_test_cases
except:
    from testcases import load_test_cases

num_tests_run = 0

def is_ascii(s):
    maxAnsiCode = 127
    return all([c <= maxAnsiCode for c in s.encode()])

def run_test_keyword_short(fullName, masterPassword, siteName,
                           siteCounter, resultType, keyPurpose,
                           result, identicon):
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

if __name__ == '__main__':
    test_keyword_short()
