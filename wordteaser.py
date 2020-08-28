#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Purpose: Break phrasesofwordswithoutseparators into words
"""

import argparse
from collections import defaultdict
from typing import NamedTuple, TextIO, Dict, List
from pprint import pprint


class Args(NamedTuple):
    text: str
    wordlist: TextIO


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
    hits = f(text, words)
    pprint(hits)

    def fst(l):
        return l[0]

    for i, group in enumerate(hits, start=1):
        print(i, group)
        # print(''.join(map(fst, group)))

    # char = text[0]
    # parts = []
    # p = []

    # # while True:
    # print(f'char "{char}"')
    # if char in words:
    #     for word in words[char]:
    #         if text.startswith(word):
    #             print(f'hit "{word}"')
    #             p.append((word, text[len(word):]))

    #             # print(f'p = "{p}"')
    #             # # truncate text
    #             # text = text[len(word):]
    #             # if text:
    #             #     char = text[0]
    #             #     continue
    #             # else:
    #             #     parts.append(''.join(p))
    #             #     p = []

    #     # if not text:
    #     #     break

    # print(f'p = {p}')
    # # print('parts = {}'.format('\n'.join(p)))


# --------------------------------------------------
def f(text, words):
    """ Find """

    if not text:
        return []

    char = text[0]
    if char not in words:
        return []

    hits = []
    if char in words:
        for word in filter(lambda w: text.startswith(w), words[char]):
            print(f'hit "{word}"')
            # ret.append(word)
            after = text[len(word):]
            hits.append([word, f(after, words)])
            # start, rest = f(after, words)
            # if not rest:

    return hits


# --------------------------------------------------
def read_wordlist(fh: TextIO) -> Dict[str, List[str]]:
    """ Read wordlist """

    words = defaultdict(list)

    for word in filter(None, map(str.rstrip, fh)):
        words[word[0]].append(word)

    return words


# --------------------------------------------------
if __name__ == '__main__':
    main()
