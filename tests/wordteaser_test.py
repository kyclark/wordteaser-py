import os
import io
from subprocess import getstatusoutput
from wordteaser import read_wordlist

PRG = './wordteaser.py'
DICT1 = './tests/dict1.txt'


# --------------------------------------------------
def test_read_wordlist():
    """ Test read_wordlist """

    d1 = io.StringIO('aa\nbbb\naaa\ncccc')
    expected1 = {'a': ['aa', 'aaa'], 'b': ['bbb'], 'c': ['cccc']}
    assert read_wordlist(d1) == expected1


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
    assert sorted(out.splitlines()) == ['a', 'b', 'c', 'ab', 'bc', 'abc']
