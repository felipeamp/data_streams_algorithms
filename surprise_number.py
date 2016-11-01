#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
2nd moments calculation using and exact method and the Alon-Matias-Szegedy (AMS) algorithm.
"""

import gzip
import os
import urllib.request
import random

def main():
    """
    Main function. Calls the 2nd moment calculation functions and analyzes the
    resulting values and time metrics.
    """
    downloaded, dataset_filename = download_dataset()
    if downloaded:
        print('Dataset downloaded.')
    else:
        print('Dataset locally present.')

    exact_sn = calc_surprise_number_exact(dataset_filename)
    ans_sn = calc_surprise_number_ams(dataset_filename, [0.1, 0.2, 0.3, 0.4, 0.5])
    print('Surprise number (exact method) = {}'.format(exact_sn))
    print('Surprise number (Alon-Matias-Szegedy method) = {}'.format(ans_sn))


def download_dataset(dataset_path=os.getcwd() + '/datasets'):
    """
    This function downloads the input dataset to the given path.

    Keyword arguments:
    dataset_path -- The folder to save the dataset into. Default value is the
    'datasets' folder under the current directory. The backslash will be appended
    automatically.

    Returns:
    downloaded -- True if the dataset was downloaded, or False if it was locally
    present in the given folder.
    dataset_filename -- The full path to the dataset.
    """
    downloaded = False
    dataset_filename = dataset_path + '/nytimes.txt.gz'
    if os.path.exists(dataset_filename) is False or os.path.isfile(dataset_filename) is False:
        print('Downloading dataset.')
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/docword.nytimes.txt.gz'
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
    surprise_number = 0
    with gzip.open(dataset_filename, 'r') as file_input:
        _ = int(file_input.readline().decode('ascii').split('=')[0])
        _ = int(file_input.readline().decode('ascii').split('=')[0])
        _ = int(file_input.readline().decode('ascii').split('=')[0])

        for line in file_input:
            _, _, count = line.decode('ascii').split(' ')
            surprise_number = surprise_number + int(count) ** 2

    return surprise_number

def calc_surprise_number_ams(dataset_filename, perc_num_variables):
    """
    This function estimates the 2nd moment of a dataset (a.k.a. surprise number)
    using the Alon-Matias-Szegedy (AMS) algorithm.

    Parameters:
    dataset_filename -- The full path to the dataset file. This file is expected
    to be in txt.gz format.
    perc_num_variables -- A list containing the percentage of words to be
    classified as variables by the algorithm. Each element in this list must in
    range [0.0, 1.0).

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
        for n in range(num_variables):
            _, _, count = file_contents[var[n]].split(' ')
            count = int(count)
            ams = num_words * (2 * count - 1)
            surprise_numbers.append(ams)

        estimated_sn = sum(surprise_numbers) / float(len(surprise_numbers))
        avg_surprise_numbers.append(estimated_sn)
        print('Estimated surprise number using {} values = {}'.format(num_variables, estimated_sn))

    return avg_surprise_numbers

if __name__ == '__main__':
    main()
