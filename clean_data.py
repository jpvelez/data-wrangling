#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Clean CSV file.

Usage:

python clean_data.py test.csv state_abbreviation.csv --output solution.csv
'''

import sys
import csv
import argparse

from enigma.cleaner import clean_rows, map_state_codes_to_names


def init_parser():
    '''
    Initialize argument parser instance for test data cleaner client.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('test_data', help='CSV of test data you want to clean.')
    parser.add_argument('state_abbr', help='CSV of state abbreviations to help in cleaning.')
    parser.add_argument('--output', help='File path to store CSV output of the cleaner.')
    return parser

if __name__ == '__main__':
    # Parse command line arguments.
    args = init_parser().parse_args()
    # Load state abbreviation csv into dict.
    state_code_to_name = map_state_codes_to_names(args.state_abbr)
    # Read in and parse csv.
    reader = csv.DictReader(open(args.test_data, 'r'))
    # If output flag supplied, write cleaner output
    # to disk. Otherwise, stream to stdout.
    stream = sys.stdout
    if args.output:
        stream = open(args.output, 'w')
    with stream:
        # Clean rows and write out to csv.
        writer = csv.DictWriter(stream,
                                reader.fieldnames + ['start_date_description'])
        writer.writeheader()
        for clean_row in clean_rows(reader, state_code_to_name):
            writer.writerow(clean_row)
