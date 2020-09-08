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
usage: wordteaser.py [-h] [-w FILE] [-m min] str [str ...]

Break phrasesofwordswithoutseparators into words

positional arguments:
  str                   Input text

optional arguments:
  -h, --help            show this help message and exit
  -w FILE, --wordlist FILE
                        Wordlist file (default: /usr/share/dict/words)
  -m min, --min min     Minimum word length (default: 1)
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
abc
a + bc
ab + c
a + b + c
```

Notice that the shortest paths/longest words are returned first:

```
$ ./wordteaser.py -w tests/dict1.txt abcd
a + bcd
ab + cd
abc + d
a + b + cd
a + bc + d
ab + c + d
a + b + c + d
```

You can require that the composite words be of a minimum length:

```
$ ./wordteaser.py -w tests/dict1.txt -m 2 abcd
ab + cd
```

For instance, if you use the default dictionary that has single-letters, then you really need to indicate a word length of at least 2:

```
$ ./wordteaser.py -m 2 tableapplechairtablecupboard
table + apple + chair + table + cupboard
table + apple + chair + table + cup + board
```

For practical application, we can use this dictionary:

```
$ cat tests/dict3.txt
pt
patient
dx
diagnosis
```

```
$ ./wordteaser.py -w tests/dict3.txt ptdx patientdiagnosis
pt + dx
patient + diagnosis
```

Only complete paths will be returned, so if part of the input string is not found in your dictionary, you may have problems.

## Tests

Run `make test` or `python3 -m pip pytest`:

```
$ make test
python3 -m pytest -xv
============================= test session starts ==============================
...

tests/wordteaser_test.py::test_read_wordlist PASSED                      [ 11%]
tests/wordteaser_test.py::test_read_wordlist_min_len PASSED              [ 22%]
tests/wordteaser_test.py::test_find PASSED                               [ 33%]
tests/wordteaser_test.py::test_get_leaf_paths PASSED                     [ 44%]
tests/wordteaser_test.py::test_find_paths PASSED                         [ 55%]
tests/wordteaser_test.py::test_exists PASSED                             [ 66%]
tests/wordteaser_test.py::test_usage PASSED                              [ 77%]
tests/wordteaser_test.py::test_abc PASSED                                [ 88%]
tests/wordteaser_test.py::test_ptdx PASSED                               [100%]

============================== 9 passed in 0.29s ===============================
```

## Author

Ken Youens-Clark <kyclark@gmail.com>
