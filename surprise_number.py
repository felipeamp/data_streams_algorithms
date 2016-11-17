#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
2nd moments calculation using and exact method and the Alon-Matias-Szegedy (AMS) algorithm.
"""

import zipfile
import os
import re
import string
import timeit
import urllib.request
from collections import Counter
import numpy as np

run_number = 1
OUTPUT_FILE = os.path.join('outputs', 'output_ams_surprisenumber_run_' + str(run_number) + '.txt')
BENCHMARK_FILE = os.path.join('outputs', 'benchmark_ams_surprisenumber_run_' + str(run_number) + '.txt')
NUM_SAMPLES = 10000

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

    dataset = tokenize_dataset(dataset_filename)
    token_dict = get_token_count_dict(dataset)

    exact_sn = calc_surprise_number_exact(dataset, True)
    ams_sn = calc_surprise_number_ams(dataset, NUM_SAMPLES, True)

    with open(BENCHMARK_FILE, 'w') as benchmark_out:
        benchmark_out.write('Number of samples = {}\n'.format(NUM_SAMPLES))
        benchmark_out.write('Exact algorithm processing time = {}\n'.format(exact_sn[1]))
        benchmark_out.write('AMS total processing time = {}\n'.format(ams_sn[1]))
        benchmark_out.write('Average processing time per sample update (AMS) = {}\n'.format(ams_sn[1] / sum(token_dict.values())))

    print('Surprise number (exact method) = {}; Processing time = {}'.format(exact_sn[0], exact_sn[1]))
    print('Surprise number estimated using the AMS algorithm = {}; Total processing time = {}'.format(ams_sn[0], ams_sn[1]))
    print('Average processing time per sample update (AMS) = {}'.format(ams_sn[1] / sum(token_dict.values())))


def download_dataset(url, filename, dataset_path=os.path.join(os.getcwd(), 'datasets')):
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
    dataset_filename = os.path.join(dataset_path, filename)
    if not os.path.exists(dataset_filename) or not os.path.isfile(dataset_filename):
        print('Downloading dataset.')
        urllib.request.urlretrieve(url=url,
                                   filename=dataset_filename)
        downloaded = True
    return downloaded, dataset_filename

def tokenize_dataset(dataset_filename):
    """
    This function opens the dataset file, reads it line-by-line and splits each
    line by punctuation and whitespaces, returning a list of lists of tokens.

    Arguments:
    dataset_filename -- The full path to the dataset in zip format.

    Returns:
    lines_list -- A list of lines, where each line is a list of strings split
    by whitespace and punctuation characters.
    """
    file_contents = []
    with zipfile.ZipFile(dataset_filename, 'r').open('Norvig.txt', 'r') as file_input:
        file_contents = file_input.readlines()

    for line_idx, line in enumerate(file_contents):
        file_contents[line_idx] = line.decode('ascii')

    lines_list = []
    for line in file_contents:
        split_line = re.split('[' + string.punctuation + string.whitespace + ']',
                              line.lower())
        split_line = list(filter(None, split_line))
        lines_list.append(split_line)

    return lines_list

def get_token_count_dict(dataset):
    """
    This function builds a dictionary with the dataset's tokens and the number
    of occurences of each token.

    A token is defined by a lowercase word. Punctuation and whitespaces are
    excluded.

    Arguments:
    dataset -- A list of lines. Each sublist is contains the words of that line.
    These words will be used as keys in the resulting dictionary.

    Returns:
    A boolean value indicating if the operation was successful.
    word_dict -- A dictionary with the dataset's tokens as keys and their number
    of ocurrences as values. If the operation failed and empty dictionary is
    returned.
    """
    if len(dataset) == 0:
        return {}

    ## Building the word dictionary.
    counter = Counter()
    for line in dataset:
        counter.update(line)

    return dict(counter)


def calc_surprise_number_exact(dataset, measure_performance=False):
    """
    This function calculates the exact surprise number of a dataset.
    The surprise number is defined as the second moment of a set. The exact way
    to calculate it involves counting the number of occurrences of each i-th
    element of a dataset (named as m_i), squaring them (m_i^2) and summing the
    resulting values (sum(m_i^2)). This method is exact, however it is slow,
    since the whole dataset must be transversed.

    Arguments:
    dataset -- A list of lines. Each sublist is contains the words of that line.

    measure_performance -- Switch to indicate if the time to calculate the 2nd
    moment should be measured. If set to True, the resulting time is returned
    following the surprise number. The default value is False.

    Returns:
    The 2nd moment, a.k.a. surprise number, of the dataset. And the time it took
    to calculate the surprise number (if the measure_performance parameter is
    set to True). If the operation failed, then the surprise number returned will
    be -1 and the measured time will be returned as None, regardless of the
    measure_performance parameter value.
    """
    token_dict = get_token_count_dict(dataset)
    if len(token_dict) == 0:
        return -1, None

    start_time = timeit.default_timer()
    surprise_number = sum(count ** 2 for count in token_dict.values())
    end_time = timeit.default_timer() - start_time

    return surprise_number, (end_time if measure_performance else None)

def calc_surprise_number_ams(dataset, sample_size, measure_performance=False):
    """
    This function estimates the 2nd moment of a dataset (a.k.a. surprise number)
    using the Alon-Matias-Szegedy (AMS) algorithm.

    Arguments:
    dataset -- A list of lines. Each sublist is contains the words of that line.

    sample_size -- The size of the sample to be used in the reservoir sampling
    algorithm. This number must be smaller than the size of the dataset.

    measure_performance -- Switch to indicate if the time to calculate the 2nd
    moment should be measured. If set to True, the resulting time is returned
    following the surprise number. The default value is False.

    Returns:
    """
    def add_token_to_sample(token):
        """
        Helper function to add a new token to the sample data structures.

        Arguments:
        token -- The new element to be added to the sample.
        """
        if token not in count_dict:
            count_dict[token] = 1
            sample_dict[token] = {0: 1}
        else:
            for k in sample_dict[token].keys():
                sample_dict[token][k] += 1
            sample_dict[token][count_dict[token]] = 1
            count_dict[token] += 1

    def del_token_from_sample(token):
        """
        Helper function to remove a token from the sample data structures.

        Arguments:
        token -- The token to be removed.
        """
        if len(sample_dict[token]) == 1:
            del sample_dict[token]
            del count_dict[token]
        else:
            to_del = np.random.choice(a=list(sample_dict[token].keys()))
            del sample_dict[token][to_del]

    sample_dict = {}
    count_dict = {}
    stream_elements_visited = 0
    surprise_number_list = []

    start_time = timeit.default_timer()
    for line_idx, line in enumerate(dataset):
        chance_to_remove_token = np.random.rand(len(line))
        # Iterating through the tokens.
        for token_idx, token in enumerate(line):
            # If the number of stream elements visited is less than the sample
            # size, the element is automatically included in the samples
            # dictionary.
            if stream_elements_visited < sample_size:
                # If the element is not in the dictionary, we add it to the
                # counter dict and the samples dict, else, we add another
                # counter to the count dict and increment all counters in the
                # token dict inside the samples dict.
                add_token_to_sample(token)
            else:
                if chance_to_remove_token[token_idx] > (sample_size / stream_elements_visited):
                    # If the random number generator returns a value larger
                    # than sample_size / N, then we must add the new stream
                    # element to our sample. Since our sample is full, we must
                    # choose an element to remove from it. To remove an element,
                    # we choose one uniformly at random, remove it and add the
                    # new element to our sample set.
                    key_probs = [(k, len(v) / sample_size) for k, v in sample_dict.items()]
                    keys, probs = zip(*key_probs)
                    elem = np.random.choice(a=keys,
                                            p=probs,
                                            replace=False)
                    del_token_from_sample(elem)
                    # Adding the new element to the sample.
                    add_token_to_sample(token)

            # Updating the 2nd moment estimate.
            num_samples = sample_size
            if stream_elements_visited < sample_size:
                num_samples = sum(len(d) for d in sample_dict.values())

            surprise_number = sum((2 * c - 1)
                                  for d in sample_dict.values()
                                  for c in d.values()) * stream_elements_visited / num_samples

            surprise_number_list.append(surprise_number)
            if len(surprise_number_list) >= 100000:
                # Save buffer to file
                if OUTPUT_FILE is not None:
                    with open(OUTPUT_FILE, 'a') as file_out:
                        for item in surprise_number_list:
                            file_out.write('{}\n'.format(item))
                    surprise_number_list = []

            stream_elements_visited = stream_elements_visited + 1

        if (line_idx % 1000) == 0:
            print("Processed line {}/{}".format(line_idx, len(dataset)))

    end_time = timeit.default_timer() - start_time
    return surprise_number_list[-1], end_time if measure_performance else None

if __name__ == '__main__':
    main()
