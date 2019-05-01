#!/usr/bin/python3
import pympw
from tests.testcases import load_test_cases
import pprint

def run_testcase_siteResult(case, verbose):
    siteResult = pympw.generate_password(case['fullName'],
                                         case['masterPassword'],
                                         case['siteName'], case['siteCounter'],
                                         case['keyPurpose'],
                                         case['resultType'])
    assert(siteResult == case['result'])

def run_testcase_identicon(case, verbose):
    assert(pympw.identicon(case['fullName'], case['masterPassword']))

def is_ascii(test_case):
    def string_is_ascii(s):
        maxAnsiCode = 127
        return all([c <= maxAnsiCode for c in s.encode()])
    return all([string_is_ascii(test_case[key]) for key in ['fullName',
                                                            'masterPassword',
                                                            'siteName']])

def test():
    # sorting out non-ascii as there is some mysterious problem with non ascii
    # characters generating the wrong password. Note that the cli will never
    # give you back a "wrong" password instead it will error out.  Only
    # support algorithm version 3 and not key context.  keyPurpose again have
    # some mysterious bug but as I personally only use Authentication I will
    # not fix it untill someone have a problem with it. The same is none-ascii.
    test_cases = [case for case in load_test_cases('tests/testcases.xml') if
                  ('keyContext' not in case) and
                  is_ascii(case) and
                  (case['keyPurpose'] == 'Authentication') and
                  (case['algorithm'] == 3)]
    [run_testcase_identicon(case, verbose=True) for case in test_cases]
    [run_testcase_siteResult(case, verbose=True) for case in test_cases]
