import unittest

from html_scraper import KijijiScraper


class TestScraperMethods(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.scraper = KijijiScraper()
