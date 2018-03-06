import re

import requests
from listing import Listing
from lxml import html, etree


class HtmlScraper():
    def __init__(self):
        # declare class variables to hold parsed HTML
        self.html_tree = -1

    def parse_url(self, url):
        # fetch the webpage
        page = requests.get(url)

        # parse the webpage
        self.html_tree = html.fromstring(page.content)


class KijijiScraper(HtmlScraper):
    def __init__(self):
        super(KijijiScraper, self).__init__()

        self.rss_tree = -1

    def parse_url(self, url):
        super(KijijiScraper, self).parse_url(url)

        rss_url = 'https://kijiji.ca' + \
                  self.html_tree.xpath('//div[@class="pagination"]/a[@class="rss-link" and @title="RSS Feed"]/@href')[0]
        rss = requests.get(rss_url)
        self.rss_tree = etree.fromstring(rss.content)

    # remove extra symbols from the parsed price using string pattern matching
    def price_trim(self, price):
        # extract a chain of characters containing '$' ',' numbers or '.'
        trimmed = re.search('[$,0-9.]+|\w+ \w+', price)
        if trimmed:  # if pattern is matched
            return trimmed.group(0)
        else:  # if pattern is not found
            # print(repr(price))
            return -1  # -1 signal there is a problem

    def get_prices(self):
        # extract prices into a list of prices
        prices = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@class="info-container"]//div[@class="price"]/text()')
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

    def get_postingtitles(self):
        # extract product names into a list of names
        titles = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@class="title"]//a[@href and @class="title enable-search-navigation-flag "]/text()')
        # remove useless characters from the extracted titles
        titles = list(map(self.title_trim, titles))
        return titles

    def get_listingids(self):
        # extract listing ids into a list of ids
        ids = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@data-ad-id and @data-vip-url]/@data-ad-id')
        return ids

    def get_listingurls(self):
        # extract listing urls into a list of urls
        urls = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@data-ad-id and @data-vip-url]/@data-vip-url')
        return urls

    def get_pubdates(self):
        # extract publishing dates into a list of dates
        dates = self.rss_tree.xpath('//rss//channel//item//*[name()="dc:date"]/text()')
        return dates

    def get_listings(self):
        ids = self.get_listingids()
        titles = self.get_postingtitles()
        prices = self.get_prices()
        # pubdates = self.get_pubdates()
        urls = self.get_listingurls()

        listings = []
        for i in range(len(ids)):
            listing = Listing()
            listing.set_id(ids[i])
            listing.set_title(titles[i])
            listing.set_price(prices[i])
            # listing.set_pubdate(pubdates[i])
            listing.set_url(urls[i])

            listings += [listing]

        return listings
