#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import gzip
import os
import sys
import urllib.request

def main():
    download_dataset()

def download_dataset(dataset_path = os.getcwd() + "/datasets"):
    """This function downloads the input dataset to the given path.

    Keyword arguments:
    dataset_path -- The folder to save the dataset into. Default value is the
    'datasets' folder under the current directory. The backslash will be appended
    automatically.
    """
    dataset_file = dataset_path + "/nytimes.txt.gz"
    if (os.path.exists(dataset_file) == False or os.path.isfile(dataset_file) == False):
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/docword.nytimes.txt.gz"
        urllib.request.urlretrieve(url = url,
                                   filename = dataset_file)

def calc_surprise_number(dataset_file, method = "exact"):
    if (method == "exact"):
        pass
    if (method == "AMS"):
        pass
    return 0

if __name__ == '__main__':
    main()
    
