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
    with gzip.open(DATASET_PATH, 'r') as fin:
        for line in fin:
            if is_header:
                is_header = False
                continue
            date_str, time_str, value, _, _, _, _, _, _ = line.decode('ascii').split(';')
            if value == '?':
                values_of_last_month.popleft()
                continue
            date_str_reversed = reverse_date(date_str)
            rounded_value = get_rounded_value(value)
            values_of_last_month.append(rounded_value)
            # if len(values_of_last_month) < values_of_last_month.maxlen:
            #     continue
            if date_str_reversed not in most_common_by_date:
                most_common_by_date[date_str_reversed] = {}
            current_most_frequent = calculate_frequent(list(values_of_last_month))
            most_common_by_date[date_str_reversed][time_str] = current_most_frequent
    if OUTPUT_FILE is not None:
        with open(OUTPUT_FILE, 'w')as fout:
            print_answers(most_common_by_date, fout=fout)
    else:
        print_answers(most_common_by_date, fout=sys.stdout)

def reverse_date(date_str):
    day, month, year = date_str.split('/')
    return '{}/{}/{}'.format(year, month, day)

def get_rounded_value(value):
    return '{:.1f}'.format(float(value))

def calculate_frequent(list_of_items_to_consider):
    def increment_item(item_name, most_common_list):
        for elem_index, (elem_name, _) in enumerate(most_common_list):
            if elem_name == item_name:
                most_common_list[elem_index][1] += 1
                break

    def decrement_all_and_remove(most_common_list):
        new_most_common_list = []
        new_items_in_list = set([])
        for (elem_name, elem_count) in most_common_list:
            if elem_count == 1:
                continue
            else:
                new_most_common_list.append([elem_name, elem_count - 1])
                new_items_in_list.add(elem_name)
        return new_most_common_list, new_items_in_list

    most_common_list = [] # list of [item_name, item_count]
    items_in_list = set([])
    for item in list_of_items_to_consider:
        if item in items_in_list:
            increment_item(item, most_common_list)
        elif len(most_common_list) < K:
            most_common_list.append([item, 1])
            items_in_list.add(item)
        else:
            most_common_list, items_in_list = decrement_all_and_remove(most_common_list)
    return items_in_list

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
