#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Purpose: Break phrasesofwordswithoutseparators into words
"""

import argparse
import io
from itertools import chain
from collections import defaultdict
from typing import NamedTuple, TextIO, Dict, List, Any
from pprint import pprint


class Args(NamedTuple):
    text: str
    wordlist: TextIO


Lookup = Dict[str, List[str]]


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Break phrasesofwordswithoutseparators into words',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text', metavar='str', help='Input text')

    parser.add_argument('-w',
                        '--wordlist',
                        help='Wordlist file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='/usr/share/dict/words')

    args = parser.parse_args()

    return Args(args.text, args.wordlist)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    words = read_wordlist(args.wordlist)
    text = args.text
    hits = find(text, words)

    for i, combo in enumerate(chain.from_iterable(map(flatten, hits)), start=1):
        print(i, combo)

    # for i, group in enumerate(hits, start=1):
    #     print(flatten(group))


# --------------------------------------------------
def read_wordlist(fh: TextIO) -> Lookup:
    """ Read wordlist """

    words = defaultdict(list)

    for word in filter(None, map(str.rstrip, fh)):
        words[word[0]].append(word)

    return words


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
def find(text: str, words: Lookup) -> List[Any]:
    """
    Look in "text" for any occurrence of the "words"
    """

    if not text:
        return ['']

    char = text[0]
    if char not in words:
        return ['']

    hits = []
    if char in words:
        for word in filter(lambda w: text.startswith(w), words[char]):
            hits.append([word] + find(text[len(word):], words))

    return hits


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
def stringer(xs: List[Any]) -> str:
    """
    Turn the nested list of lists from find() into a string
    """

    if not xs:
        return ''

    # e.g., ['c', '']
    if xs[1] == '':
        return xs[0]

    def cat(a, b=''):
        return f'{a}+{b}' if b else a

    return ':'.join([cat(xs[0], stringer(x)) for x in xs[1:]])


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
def flatten(xs: List[Any]) -> str:
    """
    Turn the nested list of lists from find() into single list
    """

    return [word.split('+') for word in stringer(xs).split(':')]


# --------------------------------------------------
def test_flatten() -> None:
    """ Test flatten """

    # hits = [['a', ['b', ['c', '']], ['bc', '']], ['ab', ['c', '']],
    #         ['abc', '']]

    hits = ['a', ['b', ['c', '']], ['bc', '']]

    assert flatten(hits) == [['a', 'b', 'c'], ['a', 'bc']]


# --------------------------------------------------
if __name__ == '__main__':
    main()
