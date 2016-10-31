#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import gzip
import os
import sys


K = 10
NUM_VALUES_IN_MONTH = 30 * 24 * 60 * 60
DATASET_PATH = os.path.join('datasets', 'household_power_consumption.txt.gz')
OUTPUT_FILE = os.path.join('outputs', 'output_most_frequent.txt')


def main():
    most_common_by_date = {} # most_common_by_date[date_str][time_str] = list of k most common str
    values_of_last_month = collections.deque(maxlen=NUM_VALUES_IN_MONTH)
    is_header = True
    missing_values_age = collections.deque()
    try:
        with gzip.open(DATASET_PATH, 'r') as fin:
            for line in fin:
                if is_header:
                    is_header = False
                    continue
                date_str, time_str, value, _, _, _, _, _, _ = line.decode('ascii').split(';')
                if value == '?':
                    if (len(missing_values_age)
                            and missing_values_age[-1] != NUM_VALUES_IN_MONTH - 1):
                        values_of_last_month.popleft()
                    update_missing_values_age(missing_values_age)
                    missing_values_age.appendleft(0)
                    continue
                date_str_reversed = reverse_date(date_str)
                rounded_value = get_rounded_value(value)
                values_of_last_month.append(rounded_value)
                if date_str_reversed not in most_common_by_date:
                    most_common_by_date[date_str_reversed] = {}
                current_most_frequent = calculate_frequent(values_of_last_month)
                most_common_by_date[date_str_reversed][time_str] = current_most_frequent
                update_missing_values_age(missing_values_age)
    finally:
        if OUTPUT_FILE is not None:
            with open(OUTPUT_FILE, 'a') as fout:
                print_answers(most_common_by_date, fout=fout)
        else:
            print_answers(most_common_by_date, fout=sys.stdout)


def update_missing_values_age(missing_values_age):
    for index, _ in enumerate(missing_values_age):
        missing_values_age[index] += 1
    if len(missing_values_age) and missing_values_age[-1] == NUM_VALUES_IN_MONTH:
        missing_values_age.pop()


def reverse_date(date_str):
    day, month, year = date_str.split('/')
    return '{}/{}/{}'.format(year, month, day)


def get_rounded_value(value):
    return '{:.1f}'.format(float(value))


def calculate_frequent(list_of_items_to_consider):
    def decrement_all_and_remove(most_common):
        list_del = []
        for (elem_name, elem_count) in most_common.items():
            if elem_count == 1:
                list_del.append(elem_name)
            else:
                most_common[elem_name] -= 1
        for elem_name in list_del:
            del most_common[elem_name]
        list_del = None # Let's help the garbage collector

    most_common = {} # most_common[item_name] = item_count
    for item in list_of_items_to_consider:
        if item in most_common:
            most_common[item] += 1
        elif len(most_common) < K:
            most_common[item] = 1
        else:
            decrement_all_and_remove(most_common)
    return list(most_common.keys())


def print_answers(most_common_by_date, fout):
    list_of_sorted_dates = sorted(most_common_by_date.keys())
    for date_rev in list_of_sorted_dates:
        orig_date = reverse_date(date_rev)
        sorted_times_and_common_values = sorted(most_common_by_date[date_rev].items())
        for (time, common_values) in sorted_times_and_common_values:
            print('{} {}'.format(orig_date, time), file=fout)
            print('\t{}'.format(sorted(common_values)), file=fout)


if __name__ == '__main__':
    main()
