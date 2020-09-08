import os
import io
from subprocess import getstatusoutput
from wordteaser import read_wordlist, find, get_leaf_paths, find_paths

PRG = './wordteaser.py'
DICT1 = './tests/dict1.txt'
DICT3 = './tests/dict3.txt'


# --------------------------------------------------
def test_read_wordlist() -> None:
    """ Test read_wordlist """

    text = '\n'.join(
        ['a', 'b', 'c', 'd', 'ab', 'bc', 'cd', 'ad', 'abc', 'bcd'])

    assert read_wordlist(io.StringIO(text), 1) == {
        'a': ['a', 'ab', 'ad', 'abc'],
        'b': ['b', 'bc', 'bcd'],
        'c': ['c', 'cd'],
        'd': ['d']
    }


# --------------------------------------------------
def test_read_wordlist_min_len() -> None:
    """ Test read_wordlist with min length """

    text = '\n'.join(
        ['a', 'b', 'c', 'd', 'ab', 'bc', 'cd', 'ad', 'abc', 'bcd'])

    assert read_wordlist(io.StringIO(text), 2) == {
        'a': ['ab', 'ad', 'abc'],
        'b': ['bc', 'bcd'],
        'c': ['cd']
    }


# --------------------------------------------------
def test_find() -> None:
    """ Test find """

    words = {
        'a': ['a', 'ab', 'ad', 'abc'],
        'b': ['b', 'bc', 'bcd'],
        'c': ['c', 'cd'],
        'd': ['d']
    }

    assert find('abc', words) == {
        'a': {
            'b': {
                'c': {}
            },
            'bc': {}
        },
        'ab': {
            'c': {}
        },
        'abc': {}
    }


# --------------------------------------------------
def test_get_leaf_paths() -> None:
    """ Test get_leaf_paths """

    p1 = {'a': {'b': {'c': {}}, 'bc': {}}, 'ab': {'c': {}}, 'abc': {}}

    assert get_leaf_paths(p1) == [['a', 'b', 'c'], ['a', 'bc'], ['ab', 'c'],
                                  ['abc']]

    p2 = {'ab': {}, 'abc': {}}
    assert get_leaf_paths(p2) == [['ab'], ['abc']]


# --------------------------------------------------
def test_find_paths():
    """ Test find_paths """

    words = {
        'a': ['a', 'ab', 'ad', 'abc'],
        'b': ['b', 'bc', 'bcd'],
        'c': ['c', 'cd'],
        'd': ['d']
    }

    assert find_paths('abc', words) == [['abc'], ['a', 'bc'], ['ab', 'c'],
                                        ['a', 'b', 'c']]


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Usage """

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{PRG} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_abc():
    """ OK """

    rv, out = getstatusoutput(f'{PRG} -w {DICT1} abc')
    assert rv == 0
    expected = '\n'.join(['abc', 'a + bc', 'ab + c', 'a + b + c'])
    assert out == expected


# --------------------------------------------------
def test_ptdx():
    """ OK """

    rv, out = getstatusoutput(f'{PRG} -w {DICT3} ptdx patientdiagnosis')
    assert rv == 0
    expected = '\n'.join(['pt + dx', 'patient + diagnosis'])
    assert out == expected
