import os
import io
from subprocess import getstatusoutput
from wordteaser import read_wordlist, find, stringer, flatten

PRG = './wordteaser.py'
DICT1 = './tests/dict1.txt'


# --------------------------------------------------
def test_read_wordlist() -> None:
    """ Test read_wordlist """

    text = '\n'.join(
        ['a', 'b', 'c', 'd', 'ab', 'bc', 'cd', 'ad', 'abc', 'bcd'])

    assert read_wordlist(io.StringIO(text)) == {
        'a': ['a', 'ab', 'ad', 'abc'],
        'b': ['b', 'bc', 'bcd'],
        'c': ['c', 'cd'],
        'd': ['d']
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

    assert find('abc', words) == [['a', ['b', ['c', '']], ['bc', '']],
                                  ['ab', ['c', '']], ['abc', '']]


# --------------------------------------------------
def test_stringer() -> None:
    """ Test stringer """

    assert stringer(['a', '']) == 'a'
    assert stringer(['abc', '']) == 'abc'
    assert stringer(['a', ['b', ['c', '']]]) == 'a+b+c'
    assert stringer(['ab', ['c', '']]) == 'ab+c'
    assert stringer(['a', ['b', ['c', '']], ['bc', '']]) == 'a+b+c:a+bc'
    assert stringer(['a', ['b', ['c', ['d', '']]]]) == 'a+b+c+d'


# --------------------------------------------------
def test_flatten() -> None:
    """ Test flatten """

    hits1 = ['a', ['b', ['c', '']], ['bc', '']]
    assert flatten(hits1) == [['a', 'b', 'c'], ['a', 'bc']]


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
    expected = '\n'.join(
        ["['a', 'b', 'c']", "['a', 'bc']", "['ab', 'c']", "['abc']"])
    assert out == expected
