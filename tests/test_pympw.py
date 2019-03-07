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
                        

def present_result(test_cases, passed):
    print('Number of passed Tests: %s' % len([case for case in passed if case is True]))
    print('Number of failed Tests: %s' % len([case for case in passed if case is False]))

        
def test():
    test_cases = load_test_cases('tests/testcases.xml')
    test_cases = [case for case in test_cases if 'keyContext' not in case]
    [run_testcase_identicon(case, verbose=True) for case in test_cases]
    passed = [run_testcase_siteResult(case, verbose=True) for case in test_cases]
    present_result(test_cases, passed)
