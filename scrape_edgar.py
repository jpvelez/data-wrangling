#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Scrape Enigma's edgar company listings site.

Usage:

python scrape_edgar.py --input http://data-interview.enigmalabs.org/companies/ --output solutions.json
'''

import sys
import json
import argparse

from scraper import EdgarScraper


def init_parser():
    '''
    Initialize argument parser instance for Edgar scraper client.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The URL for the instance of the Edgar \
                                     site you want to scrape.')
    parser.add_argument('--output', help='File path to store JSON output of \
                                          the scraper.')
    return parser


if __name__ == '__main__':

    # Parse command line arguments.
    args = init_parser().parse_args()
    # Initialize scraper with user-supplied url.
    scraper = EdgarScraper(args.url)
    # If output flag supplied, write scraper output
    # to disk. Otherwise, stream to stdout.
    stream = sys.stdout
    if args.output:
        stream = open(args.output, 'w')
    # Run the scraper, serialize output to JSON.
    with stream:
        for company in scraper.get_all_companies():
            stream.write(json.dumps(company))
