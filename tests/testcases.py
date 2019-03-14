import xml.etree.ElementTree as ET # to parse xml file of testcases.
import copy

def load_test_cases(filename):
    result = [_load_xml_entry(case) for case in ET.parse(filename).getroot()]
    result = _resolve_inheritance(result)
    result = _remove_parent_key(result)
    result = _remove_default_testcase(result)
    result = _remove_none_v3_testcases(result)
    result = _remove_none_ascii_testcases(result)
    return result

def _load_xml_entry(case):
    """Load a testcase from previous loaded testcases and a xml.etree.ElementTree element"""
    case_dict = {}
    case_dict['id'] = case.attrib['id']
    if 'parent' in case.attrib:
        case_dict['parent'] = case.attrib['parent']
    for param in case:
        if param.tag in {'siteCounter', 'algorithm'}:
            case_dict[param.tag] = int(param.text);
        else:
            case_dict[param.tag] = param.text;
    return case_dict

def _resolve_inheritance(test_cases):
    return [_get_full_case(test_cases, case) for case in test_cases]

def _get_full_case(test_dict_list, test_case):
    """Recursivly resolve the the testcase"""
    if 'parent' in test_case:
        parent = _find_dict_by_id(test_dict_list, test_case['parent'])
        parent = _get_full_case(test_dict_list, parent)
        full_test_case = copy.deepcopy(parent)
        for param in test_case:
            full_test_case[param] = test_case[param]
        return full_test_case
    else:
        return copy.deepcopy(test_case);


def _load_xml_to_dict_list(filename):
    tests_list = []
    tree = ET.parse(filename)
    tests = tree.getroot()
    for case in tests:
        test_list.append(_load_xml_entry(case))
    return test_list
    

def _find_dict_by_id(test_dict_list, id_tag):
    for test_dict in test_dict_list:
        if test_dict['id'] == id_tag:
            return test_dict
    raise KeyError('Testcase with id: %s not found' % id_tag)

def _remove_default_testcase(test_cases):
    result = []
    for case in test_cases:
        if case['id'] != 'default':
            result.append(case)
    return result

def _remove_parent_key(test_cases):
    for case in test_cases:
        if 'parent' in case:
            del case['parent']
    return test_cases

def _remove_none_v3_testcases(test_cases):
    def is_v3(case):
        return case['algorithm'] == 3
    res = list(filter(is_v3, test_cases))
    def remove_algorithm(case):
        del case['algorithm']
        return case
    return list(map(remove_algorithm, res))

def _ASCII(s):
    maxAnsiCode = 127
    return all([c <= maxAnsiCode for c in s.encode()])

def testcase_is_ascii(test_case):
    return all([_ASCII(test_case[key]) for key in ['fullName',
                                                   'masterPassword',
                                                   'siteName']])
def _remove_none_ascii_testcases(test_cases):
    return [case for case in test_cases if testcase_is_ascii(case)]

