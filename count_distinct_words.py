#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import gzip
import os
import sys


DATASET_PATH = os.path.join('datasets', 'norvig.txt.gz')

def main():
    num_distinct_words = 0
    words_dict = {}
    
    try:
        with gzip.open(DATASET_PATH, 'r') as fin:
            for line in fin:
                words = line.decode('ascii').split()
                for word in words:
                    if not word in words_dict:
                        words_dict[word] = 1
                        num_distinct_words += 1 
    finally:
        print("Number of distinct words: %d" % (num_distinct_words))


if __name__ == '__main__':
    main()
