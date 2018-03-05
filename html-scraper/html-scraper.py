import re

import requests
from lxml import html


class HtmlScraper():
    def __init__(self):
        # declare class variables to hold parsed HTML
        self.page = 0
        self.html_tree = 0

    def parse_url(self, url):
        # fetch the webpage
        self.page = requests.get(url)

        # parse the webpage
        self.html_tree = html.fromstring(self.page.content)


class KijijiScraper(HtmlScraper):
    # remove extra symbols from the parsed price using string pattern matching
    def price_trim(self, price):
        # extract a chain of characters containing '$' ',' numbers or '.'
        trimmed = re.search('[$,0-9.]+|\w+ \w+', price)
        if trimmed:  # if pattern is matched
            return trimmed.group(0)
        else:  # if pattern is not found
            # print(repr(price))
            return -1  # -1 signal there is a problem

    def get_price(self):
        # extract prices into a list of prices
        prices = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@class="info-container"]//div[@class="price"]/text()')
        print(prices)
        # remove useless characters from the extracted prices
        prices = list(map(self.price_trim, prices))
        return prices

    def title_trim(self, title):
        # extract the title where only whitespaces, numbers and alphebetical characters are allowed
        trimmed = re.search('(([-/_!0-9\'"])|(\w+)| +)+', title.strip())
        if trimmed:  # if pattern is matched
            return trimmed.group(0)
        else:  # if pattern is not found
            # print(erpr(title))
            return -1  # -1 signal there is a problem

    def get_postingtitle(self):
        # extract product names into a list of names
        titles = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@class="title"]//a[@href and @class="title enable-search-navigation-flag "]/text()')
        # remove useless characters from the extracted titles
        titles = list(map(self.title_trim, titles))
        return titles
