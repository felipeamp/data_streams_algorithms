#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import gzip
import os
import sys


DATASET_PATH = os.path.join('datasets', 'norvig.txt.gz')
num_distinct_words = 0

def main():
    try:
        with gzip.open(DATASET_PATH, 'r') as fin:
            for line in fin:
                line = line.decode('ascii')
    finally:
        print("Number of distinct words: %d" % (num_distinct_words))


if __name__ == '__main__':
    main()
