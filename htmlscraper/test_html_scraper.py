#!/usr/bin/python3

import unittest

from .html_scraper import KijijiScraper


class TestScraperMethods(unittest.TestCase):
    def setUp(self):
        self.scraper = KijijiScraper()
        self.html_trees = []
        self.html_trees.append(self.scraper.get_html_tree(
            'https://www.kijiji.ca/v-house-rental/kitchener-waterloo/gorgeous-detached-modern-4-bdrms-hardwood-floors-patio-waterloo/1346206828'))

    def test_get_cat_id(self):
        url = 'https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c43l1700212'
        self.assertEqual(self.scraper.get_cat_id(url), 43)

        url = 'https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c43l1700212/'
        self.assertEqual(self.scraper.get_cat_id(url), 43)

        url = 'https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c3l1700212/'
        self.assertEqual(self.scraper.get_cat_id(url), 3)

    def test_get_loc_id(self):
        url = 'https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c43l1700212'
        self.assertEqual(self.scraper.get_loc_id(url), 1700212)

        url = 'https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c43l1700212/'
        self.assertEqual(self.scraper.get_loc_id(url), 1700212)

        url = 'https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c3l1700212/'
        self.assertEqual(self.scraper.get_loc_id(url), 1700212)

    def test_get_listing_title(self):
        for tree in self.html_trees:
            self.assertEqual(self.scraper.get_listing_title(tree),
                             'GORGEOUS DETACHED-MODERN,4 BDRMS,HARDWOOD FLOORS,PATIO-WATERLOO')

    def test_get_listing_price(self):
        for tree in self.html_trees:
            self.assertEqual(self.scraper.get_listing_price(tree), 1725)


if __name__ == '__main__':
    unittest.main()
