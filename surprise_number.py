#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import gzip
import os
import sys
import urllib.request

def main():
    dataset_filename = download_dataset()
    calc_surprise_number(dataset_filename)    

def download_dataset(dataset_path = os.getcwd() + "/datasets"):
    """This function downloads the input dataset to the given path.

    Keyword arguments:
    dataset_path -- The folder to save the dataset into. Default value is the
    'datasets' folder under the current directory. The backslash will be appended
    automatically.
    """
    dataset_filename = dataset_path + "/nytimes.txt.gz"
    if (os.path.exists(dataset_filename) == False or os.path.isfile(dataset_filename) == False):
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/docword.nytimes.txt.gz"
        urllib.request.urlretrieve(url = url,
                                   filename = dataset_filename)
    return dataset_filename

def calc_surprise_number(dataset_filename, method = "exact"):
    with gzip.open(dataset_filename, 'r') as file_input:
        num_docs = int(file_input.readline().decode('ascii').split('=')[0])
        num_unique_words = int(file_input.readline().decode('ascii').split('=')[0])
        num_words = int(file_input.readline().decode('ascii').split('=')[0])

        i = 0
        for line in file_input:
            doc_id, word_id, count = line.decode('ascii').split(' ')
            print('{}'.format(count))
            i = i + 1
            if i >= 50:
                break
    
    if (method == 'exact'):
        pass
    if (method == 'AMS'):
        pass
    return 0

def moment_exact(dataset):
    pass

def moment_ams(dataset):
    pass

if __name__ == '__main__':
    main()
    
