#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
2nd moments calculation using and exact method and the Alon-Matias-Szegedy (AMS) algorithm.
"""

import zipfile
import os
import random
import re
import string
import numpy as np
import urllib.request

def main():
    """
    Main function. Calls the 2nd moment calculation functions and analyzes the
    resulting values and time metrics.
    """
    fileurl = 'http://www-di.inf.puc-rio.br/~laber/ExpandedNrvg.zip'
    downloaded, dataset_filename = download_dataset(url=fileurl,
                                                    filename='norvig.zip')
    if downloaded:
        print('Dataset downloaded.')
    else:
        print('Dataset locally present.')

    #exact_sn = calc_surprise_number_exact(dataset_filename)
    ans_sn = calc_surprise_number_ams(dataset_filename, 10)

    #print('Surprise number (exact method) = {}'.format(exact_sn))
    #print('Surprise numbers estimated using the ANS algorithm.')
    #for sn in ans_sn:
    #    print('Surprise number using {} of the values as variables = {}'.format(sn[1]))
    #for sn in ans_sn:
    #    perc = sn[0] * 100
    #    print('Ratio of exact SN and AMS SN using {} of the values as variables = {}'.format(perc, exact_sn / sn[1]))


def download_dataset(url, filename, dataset_path=os.getcwd() + '/datasets'):
    """
    This function downloads the input dataset to a local file.

    Keyword arguments:
    url -- The origin URL to download the dataset file.
    filename -- The destination file name for the dataset.
    dataset_path -- The folder to save the dataset into. Default value is the
    'datasets' folder under the current directory. The backslash will be appended
    automatically.

    Returns:
    downloaded -- True if the dataset was downloaded, or False if it was locally
    present in the given folder.
    dataset_filename -- The full path to the dataset, including its given name.
    """
    downloaded = False
    dataset_filename = dataset_path + '/' + filename
    if not os.path.exists(dataset_filename) or not os.path.isfile(dataset_filename):
        print('Downloading dataset.')
        urllib.request.urlretrieve(url=url,
                                   filename=dataset_filename)
        downloaded = True
    return downloaded, dataset_filename


def calc_surprise_number_exact(dataset_filename):
    """
    This function calculates the exact surprise number of a dataset.
    The surprise number is defined as the second moment of a set. The exact way
    to calculate it involves counting the number of occurrences of each i-th
    element of a dataset (named as m_i), squaring them (m_i^2) and summing the
    resulting values (sum(m_i^2)). This method is exact, however it is slow,
    since the whole dataset must be transversed.

    Arguments:
    dataset_filename -- The full path to the dataset file. This file is expected
    to be in .zip format.

    Returns:
    The 2nd moment, a.k.a. surprise number, of the dataset.
    """

    # Since the file is small, we read it into the memory.
    file_contents = []
    with zipfile.ZipFile(dataset_filename, 'r').open('Norvig.txt', 'r') as file_input:
        file_contents = file_input.readlines()

    # Decoding the file's contents line-by-line.
    for line_idx, line in enumerate(file_contents):
        file_contents[line_idx] = line.decode('ascii')

    ## Building the word dictionary.
    token_dict = {}
    for line in file_contents:
        ## Splitting the line by punctuation and whitspace characters, however,
        ## some empty strings are returned, thus the call to the 'filter'
        ## function.
        split_line = re.split('[' + string.punctuation + string.whitespace + ']', line)
        split_line = list(filter(None, split_line))
        for token in split_line:
            if token in token_dict:
                token_dict[token] = token_dict[token] + 1
            else:
                token_dict[token] = 1

    # Calculating the surprise number.
    surprise_number = 0
    for _, count in token_dict.items():
        surprise_number = surprise_number + count ** 2

    return surprise_number

def calc_surprise_number_ams(dataset_filename, sample_size):
    """
    This function estimates the 2nd moment of a dataset (a.k.a. surprise number)
    using the Alon-Matias-Szegedy (AMS) algorithm.

    Parameters:
    dataset_filename -- The full path to the dataset file. This file is expected
    to be in txt.gz format.
    sample_size -- The size of the sample to be used in the reservoir sampling
    algorithm. This number must be smaller than the size of the dataset.

    Returns:
    """

    # Since the file is small, we read it into the memory.
    file_contents = []
    with zipfile.ZipFile(dataset_filename, 'r').open('Norvig.txt', 'r') as file_input:
        file_contents = file_input.readlines()

    # Decoding the file's contents line-by-line.
    for line_idx, line in enumerate(file_contents):
        file_contents[line_idx] = line.decode('ascii')

    sample_dict = {}
    count_dict = {}
    stream_elements_visited = 0

    for line in file_contents:
        # Splitting the line by punctuation and whitespace characters.
        split_line = re.split('[' + string.punctuation + string.whitespace + ']',
                              line)
        split_line = list(filter(None, split_line))
        for token in split_line:
            # If the number of stream elements visited is less than the sample
            # size, the element is automatically included in the samples
            # dictionary.
            if stream_elements_visited < sample_size:
                # If the element is not in the dictionary, we add it to the
                # counter dict and the samples dict, else, we add another
                # counter to the count dict and increment all counters in the
                # token dict inside the samples dict.
                if not (token in count_dict):
                    count_dict[token] = 1
                    sample_dict[token] = {0: 1}
                else:
                    for k, v in sample_dict[token].items():
                        sample_dict[token][k] = v + 1
                    sample_dict[token][count_dict[token]] = 1
                    count_dict[token] = count_dict[token] + 1
            else:
                if random.random() > sample_size / stream_elements_visited:
                    # If the random number generator returns a value larger
                    # than sample_size / N, then we must add the new stream
                    # element to our sample. Since our sample is full, we must
                    # choose an element to remove from it. To remove an element,
                    # we choose one uniformly at random, remove it and add the
                    # new element to our sample set.
                    elem = np.random.choice(a=list(sample_dict.keys()),
                                            p=[len(v.keys()) / sum(count_dict.values()) for _, v in sample_dict.items()],
                                            replace=False)
                    if len(sample_dict[elem]) == 1:
                        del(sample_dict[elem])
                        del(count_dict[elem])
                    else:
                        to_del = np.random.choice(a=list(sample_dict[elem].keys()))
                        del(to_del)

                    ## Adding the new element to the sample.
                    if token in sample_dict:
                        pass
                    else:
                        pass
                    
            
            stream_elements_visited = stream_elements_visited + 1


if __name__ == '__main__':
    main()
