#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
2nd moments calculation using and exact method and the Alon-Matias-Szegedy (AMS) algorithm.
"""

import zipfile
import os
import urllib.request
import random
import re
import string


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

    exact_sn = calc_surprise_number_exact(dataset_filename)
    #ans_sn = calc_surprise_number_ams(dataset_filename, [x/100 for x in range(1, 100)])

    print('Surprise number (exact method) = {}'.format(exact_sn))
    #print('Surprise numbers estimated using the ANS algorithm.')
    #for sn in ans_sn:
    #    print('Surprise number using {} of the values as variables = {}'.format(sn[1]))
    #for sn in ans_sn:
    #    perc = sn[0] * 100
    #    print('Ratio of exact SN and AMS SN using {} of the values as variables = {}'.format(perc, exact_sn / sn[1]))


def download_dataset(url, filename, dataset_path=os.getcwd() + '/datasets'):
    """
    This function downloads the input dataset to the given path.

    Keyword arguments:
    url -- The origin URL to download the dataset file.
    filename -- The destination file name for the dataset.
    dataset_path -- The folder to save the dataset into. Default value is the
    'datasets' folder under the current directory. The backslash will be appended
    automatically.

    Returns:
    downloaded -- True if the dataset was downloaded, or False if it was locally
    present in the given folder.
    dataset_filename -- The full path to the dataset, including it's given name.
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
    resulting values (sum(m_i^2)). This method is exact, however, since the whole
    dataset must be transversed, it is also slow.

    Arguments:
    dataset_filename -- The full path to the dataset file. This file is expected
    to be in txt.gz format.

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

def calc_surprise_number_ams(dataset_filename, num_variables, sample_size):
    """
    This function estimates the 2nd moment of a dataset (a.k.a. surprise number)
    using the Alon-Matias-Szegedy (AMS) algorithm.

    Parameters:
    dataset_filename -- The full path to the dataset file. This file is expected
    to be in txt.gz format.
    num_variables -- The number of variables to be chosen by the algorithm.
    sample_size -- The size of the sample to be used in the reservoir sampling
    algorithm. This number must be smaller than the size of the dataset.

    Returns:
    """

    # Reading the whole file to the memory.
    file_contents = []
    with gzip.open(dataset_filename, 'r') as file_input:
        file_contents = file_input.readlines()

    # Decoding the lines of the file.
    for line_idx, line in enumerate(file_contents):
        file_contents[line_idx] = line.decode('ascii')

    num_unique_words = int(file_contents[1])
    num_words = int(file_contents[2])
    avg_surprise_numbers = []
    for perc in perc_num_variables:
        num_variables = int(perc * num_unique_words)
        # The +3 factor is due to the fact that the file header is composed of 3
        # lines and we don't want them being picked by our sampling.
        var = random.sample(list(range(3, num_unique_words + 3)),
                            num_variables)

        surprise_numbers = []
        for curr_var in range(num_variables):
            _, _, count = file_contents[var[curr_var]].split(' ')
            count = int(count)
            ams = num_words * (2 * count - 1)
            surprise_numbers.append(ams)

        estimated_sn = sum(surprise_numbers) / float(num_variables)
        avg_surprise_numbers.append((perc, estimated_sn))

    return avg_surprise_numbers

if __name__ == '__main__':
    main()
