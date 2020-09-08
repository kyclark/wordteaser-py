#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Purpose: Break phrasesofwordswithoutseparators into words
"""

import argparse
from collections import defaultdict
from typing import NamedTuple, TextIO, Dict, List, Any


class Args(NamedTuple):
    text: List[str]
    wordlist: TextIO
    min_word_len: int


Lookup = Dict[str, List[str]]


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Break phrasesofwordswithoutseparators into words',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('text',
                        metavar='str',
                        help='Input text',
                        type=str,
                        nargs='+')

    parser.add_argument('-w',
                        '--wordlist',
                        help='Wordlist file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default='/usr/share/dict/words')

    parser.add_argument('-m',
                        '--min',
                        help='Minimum word length',
                        metavar='min',
                        type=int,
                        default=1)

    args = parser.parse_args()

    return Args(args.text, args.wordlist, args.min)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    words = read_wordlist(args.wordlist, args.min_word_len)

    for text in args.text:
        for path in find_paths(text, words):
            print(' + '.join(path))


# --------------------------------------------------
def find_paths(text, words):
    """
    Find all possible paths of the words through the text
    Return only those paths that complete the given text (no partial matches)
    in the order of the shortest paths (so using the longest words)
    """

    paths = find(text, words)

    return list(
        filter(lambda p: len(''.join(p)) == len(text),
               sorted(get_leaf_paths(paths), key=len)))


# --------------------------------------------------
def read_wordlist(fh: TextIO, min_len: int) -> Lookup:
    """
    Find all the words of a minimum length in the wordlist
    Return a dictionary where the keys are the first letters of the words
    """

    words = defaultdict(list)

    for word in filter(lambda w: len(w) >= min_len, map(str.rstrip, fh)):
        words[word[0]].append(word)

    return words


# --------------------------------------------------
def find(text: str, words: Lookup) -> Dict[str, Any]:
    """
    Look in "text" for any occurrence of the "words"
    Return a nested dictionary representing all possible paths
    Some of the paths may be incomplete
    """

    if not text:
        return {}

    char = text[0]
    if char not in words:
        return {}

    hits = {}
    if char in words:
        for word in filter(lambda w: text.startswith(w), words[char]):
            hits[word] = find(text[len(word):], words)

    return hits


# --------------------------------------------------
def get_leaf_paths(tree: Dict[str, Any]) -> List[List[str]]:
    """
    Find all paths
    Had to write the "helper" function due to
    some sort of weird persistence of the accumulator b/w calls!

    Cf https://stackoverflow.com/questions/60039297/
    return-a-list-of-paths-to-leaf-nodes-from-a-nested-list-of-lists
    """
    def helper(tree: Dict[str, Any], path: List[Any],
               acc: List[Any]) -> List[List[str]]:
        for node, children in tree.items():
            if children:  # not leaf
                helper(children, path + [node], acc)
            else:
                acc.append(path + [node])

        return acc

    return helper(tree, [], [])


# --------------------------------------------------
if __name__ == '__main__':
    main()
