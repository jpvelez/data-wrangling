#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Scraper class used by client to scrape edgar company listings site.
'''

import logging

import requests
from bs4 import BeautifulSoup
from concurrent import futures

# Log page requests, silence library logs.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)


class EdgarScraper(object):

    def __init__(self, url):
        self.url = url

    def fetch_and_parse_page(self, company_name=False, page_id=False):
        '''
        Fetch edgar page, specified by company name or page id,
        and parse with BeautifulSoup.
        '''
        url = self.url
        if company_name:
            url += company_name
            display_entity = company_name
        params = {}
        if page_id:
            params['page'] = page_id
            display_entity = 'listings page ' + str(page_id)
        logging.info('Getting page: {}'.format(display_entity))
        html = requests.get(url, params=params).content
        return BeautifulSoup(html, "html.parser")

    def get_total_pages(self):
        '''
        Compute the total number of pages on the site, based on the total
        number of listings and the number of listings shown per page. These
        fields are gathered from the pagination info displayed above the
        listings table.

        This is useful in case more listings are added to the site, because
        we avoid hardcoding which pages to get.
        '''
        # To correctly infer number of listings per page, and thus total pages,
        # we must grab page 1. Guarantee it.
        soup = self.fetch_and_parse_page(page_id=1)
        pagination_info = soup.find('div', attrs={'class': 'pagination-page-info'})
        listings_shown, total_listings = [tag.text for tag in pagination_info.find_all('b')]
        # On page 1, the highest listing id displayed in the "listings
        # displayed range" equals the number of listings per page. Grab it.
        listings_per_page = listings_shown.split(' - ')[1]
        return int(total_listings) / int(listings_per_page)

    def get_listing_page_company_names(self, page_id):
        '''
        Get all company names on the listing page
        with the supplied page id.
        '''
        soup = self.fetch_and_parse_page(page_id=page_id)
        company_urls = soup.find('tbody').find_all('a')
        return [tag['href'].split('/companies/')[1]
                for tag in company_urls]

    def get_all_company_names(self):
        '''
        Get all company names on all listings pages.

        Company names are used to fetch company pages.
        '''
        # Make sequence of listing page ids to get company names from.
        total_pages = self.get_total_pages()
        listing_page_ids = range(1, total_pages + 1)
        # Parallelize extraction of company names from listing pages.
        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            company_names = executor.map(self.get_listing_page_company_names,
                                         listing_page_ids)
        # get_listing_page_company_names returns a list,
        # so map returns a nested list. Flatten it.
        return reduce(lambda x, y: x + y, company_names)

    def get_company_info(self, company_name):
        '''
        Get info page of given company, parse company data fields
        into dictionary.
        '''
        soup = self.fetch_and_parse_page(company_name=company_name)
        company = {}
        # Loop through company table rows.
        table_rows = soup.find('tbody').find_all('tr')
        for row in table_rows:
            # Grab company attribute name and value
            # from the second cell of every row.
            second_column = row.find_all('td')[1]
            attr = second_column.get('id')  # Tag id has good attribute names.
            value = second_column.getText()
            company[attr] = value
        return company

    def get_all_companies(self):
        '''
        Return dictionaries of every company on edgar. Fetches
        and parses companies' pages based on their names.
        '''
        # Get name of every company on site, so we fetch their pages.
        company_names = self.get_all_company_names()
        # Parallelize getting and parsing of company pages with threads. ~7x faster.
        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            companies = executor.map(self.get_company_info, company_names)
        # Return parsed companies asynchronously as jobs complete.
        for company in companies:
            yield company
