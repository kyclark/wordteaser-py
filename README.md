# wordteaser-py

Break phrasesofwordswithoutseparators into words

## Description

The goal is to use a dictionary of terms to use in decomposing a longer string that contains no separators between terms.
For instance, given a dictionary like this:

```
a
b
c
ab
bc
```

And the input string "abc," we would like to find the following combinations of strings:

```
a + b + c
ab + c
a + bc
```

In more practical terms, a string like "ptdx" represents "patient diagnosis."
It would be better to encounter "pt_dx" or "PtDx," to split that into "pt" and "dx" and then expand those using a thesaurus where "pt" is "patient" and "dx" is diagnosis."

## Wordteaser

The "wordteaser.py" program is an implementation of this idea:

```
$ ./wordteaser.py -h
usage: wordteaser.py [-h] [-w FILE] str

Break phrasesofwordswithoutseparators into words

positional arguments:
  str                   Input text

optional arguments:
  -h, --help            show this help message and exit
  -w FILE, --wordlist FILE
                        Wordlist file (default: /usr/share/dict/words)
```

Given the following dictionary:

```
$ cat tests/dict1.txt
a
b
c
d
ab
bc
cd
ad
abc
bcd
```

The program will return the following combinations:

```
$ ./wordteaser.py -w tests/dict1.txt abc
['a', 'b', 'c']
['a', 'bc']
['ab', 'c']
['abc']
```

It is currently failing with the input "abcd" as the 2nd group is missing the "a":

```
$ ./wordteaser.py -w tests/dict1.txt abcd
['a', 'b', 'c', 'd']
['b', 'cd']
['a', 'bc', 'd']
['a', 'bcd']
['ab', 'c', 'd']
['ab', 'cd']
['abc', 'd']
```

The `find()` function that finds the possible combinations works.
Here is a representation of the nested lists it finds with each prefix; that is, starting with the prefix "a," then "ab," then "abc":

```
['a', ['b', ['c', ['d', '']], ['cd', '']], ['bc', ['d', '']], ['bcd', '']]
['ab', ['c', ['d', '']], ['cd', '']]
['abc', ['d', '']]
```

We can see the first grouping finds that "a" could be followed by "b" which might be followed either by "c" and "d" or by "cd":

```
['a',
    ['b', 
        ['c', ['d', '']],   => ['a', 'b', 'c', 'd']
        ['cd', '']],        => ['b', 'cd']      <=== Missing the leading "a"
    ['bc', ['d', '']],      => ['a', 'bc', 'd']
    ['bcd', '']             => ['a', 'bcd']
]
```

I should probably consider using a directed graph to find my way through the nested lists, and for that I've looked at Python's "anytree" and "networkx" modules (see below).

FWIW, given this dictionary:

```
$ cat tests/dict3.txt
pt
patient
dx
diagnosis
```

It does appear to work:

```
$ ./wordteaser.py -w tests/dict3.txt ptdx
['pt', 'dx']
```

# See also

* https://github.com/keredson/wordninja
* https://github.com/networkx/networkx
* https://nlp.stanford.edu/IR-book/html/htmledition/tokenization-1.html
* https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
* http://norvig.com/ngrams/
* https://pypi.org/project/anytree/

## Author

Ken Youens-Clark <kyclark@gmail.com>
