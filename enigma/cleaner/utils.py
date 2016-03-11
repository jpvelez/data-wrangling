#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from dateutil.parser import parse


def map_state_codes_to_names(states):
    '''
    Return dictionary mapping state abbreviation
    codes to full names
    .'''
    with open(states, 'r') as stream:
        reader = csv.DictReader(stream)
        return {row['state_abbr']: row['state_name'] for row in reader}


def clean_bio(field):
    '''
    Strip tabs, newlines, and excessive whitespace
    from bio fields.
    '''
    return ' '.join(field.split())


def contains_k_numbers(date_field, k):
    '''Check if date field contains used-specified quantity of numbers.'''
    return len(date_field.split('/')) == k


def is_valid(date_field):
    '''
    Detect if date field is valid and should be parsed.
    Rules use substring search and boolean logic.
    '''
    # All dates with backslashes and 3 integers are valid: 05/25/2012, NOT 01/91
    is_slash_date = '/' in date_field and contains_k_numbers(date_field, k=3)
    # All dates with hyphens are valid: 1996-07-14
    is_hyphen_date = '-' in date_field
    # All dates with commas are valid: April 5, 1973
    is_comma_date = ',' in date_field
    return any([is_slash_date, is_hyphen_date, is_comma_date])


def clean_dates(field):
    '''
    Clean valid dates, or return invalid dates as start
    date descriptions.
    '''
    start_date = None
    start_date_description = None
    # If field is valid, parse to datetime using
    # generic datetime string parser, then convert
    # to ISO 8601 timestamp.
    if is_valid(field):
        start_date = parse(field).isoformat()
    else:
        start_date_description = field
    return start_date, start_date_description


def clean_rows(rows, state_code_to_name):
    '''Clean bio, state, and start_date field of dataset.'''
    for row in rows:
        # Clean bio string.
        row['bio'] = clean_bio(row['bio'])
        # Swap state abbreviations for state names.
        row['state'] = state_code_to_name[row['state']]
        # Normalize valid start dates to ISO 8601 timestamps,
        # filter invalid dates to new description column.
        start_date, start_date_description = clean_dates(row['start_date'])
        row['start_date'] = start_date
        row['start_date_description'] = start_date_description
        yield row
