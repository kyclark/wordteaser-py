.PHONY: test

run:
	./wordteaser.py -w tests/dict1.txt abcd

run2:
	./wordteaser.py -w tests/dict2.txt aabbbcccc

test:
	python3 -m pytest -xv
