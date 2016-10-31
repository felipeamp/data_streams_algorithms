#!/usr/bin/python3
# -*- coding: utf-8 -*-

import collections
import gzip
import os
import sys
import urllib.request

def main():
    downloaded, dataset_filename = download_dataset()
    if downloaded:
        print('Dataset downloaded.')
    else:
        print('Dataset locally present.')
        
    exact_sn = calc_surprise_number(dataset_filename, method = 'exact')
    ans_sn = calc_surprise_number(dataset_filename, method = 'ans')
    print('Surprise number (exact method) = '.format(exact_sn))
    print('Surprise number (ans method) = '.format(ans_sn))

def download_dataset(dataset_path = os.getcwd() + '/datasets'):
    """This function downloads the input dataset to the given path.

    Keyword arguments:
    dataset_path -- The folder to save the dataset into. Default value is the
    'datasets' folder under the current directory. The backslash will be appended
    automatically.
    """
    downloaded = False
    dataset_filename = dataset_path + '/nytimes.txt.gz'
    if (os.path.exists(dataset_filename) == False or os.path.isfile(dataset_filename) == False):
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/docword.nytimes.txt.gz'
        urllib.request.urlretrieve(url = url,
                                   filename = dataset_filename)
        downloaded = True
    return downloaded, dataset_filename

def calc_surprise_number(dataset_filename, method = 'exact'):
    surprise_number = 0
    if (method == 'exact'):
        with gzip.open(dataset_filename, 'r') as file_input:
            num_docs = int(file_input.readline().decode('ascii').split('=')[0])
            num_unique_words = int(file_input.readline().decode('ascii').split('=')[0])
            num_words = int(file_input.readline().decode('ascii').split('=')[0])

            for line in file_input:
                doc_id, word_id, count = line.decode('ascii').split(' ')
                surprise_number = surprise_number + int(count) ** 2
                
    elif (method == 'AMS'):
        pass
    
    return surprise_number

if __name__ == '__main__':
    main()
    
