#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import gzip
import os
import sys
import random
import numpy
import timeit


DATASET_PATH = os.path.join('datasets', 'norvig.txt.gz')
M = 2038074743 # Prime number


class Hash:
    def __init__(self, M):
        self.M = M

        self.a = random.randint(0, M - 1)
        self.b = random.randint(0, M - 1)
    
    def hash(self, x):
        int_x = abs(hash(x)) % sys.maxsize

        return (self.a * int_x + self.b) % self.M


def count_distinct_words_with_hash_functions(num_hash_functions):
    h_array = []
    min_array = []
    
    for i in range(num_hash_functions):
        h = Hash(M)
        h_array.append(h)
        
        min_array.append(M + 1)

    with gzip.open(DATASET_PATH, 'r') as fin:
        for line in fin:
            words = line.decode('ascii').split()
            for word in words:
                word = word.lower()
                for i in range(len(h_array)):
                    num = h_array[i].hash(word)

                    if num < min_array[i]:
                        min_array[i] = num
    
    median = numpy.median(min_array)

    return M / median


def count_distinct_words_with_exact_method():
    num_distinct_words = 0
    words_dict = {}
    
    with gzip.open(DATASET_PATH, 'r') as fin:
        for line in fin:
            words = line.decode('ascii').split()
            for word in words:
                word = word.lower()
                if not word in words_dict:
                    words_dict[word] = 1
                    num_distinct_words += 1 

    return num_distinct_words


def main():
    start_time = timeit.default_timer()
    num_distinct_words = count_distinct_words_with_exact_method()
    end_time = timeit.default_timer()
    print('Number of distinct words with exact method: %d' % (num_distinct_words))
    print('Time spent to calculate: %d seconds\n\n' % (end_time - start_time))
    
    for num_hash_functions in [1, 2, 5, 10, 20, 30, 40, 50]:
        start_time = timeit.default_timer()
        num_distinct_words = count_distinct_words_with_hash_functions(num_hash_functions)
        end_time = timeit.default_timer()
        print('Number of distinct words with %d hash function(s): %d' % (num_hash_functions, num_distinct_words))
        print('Time spent to calculate: %d seconds\n\n' % (end_time - start_time))


if __name__ == '__main__':
    main()
