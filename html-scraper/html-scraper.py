import re

import requests
from listing import Listing
from lxml import html


class HtmlScraper():
    def __init__(self):
        # declare class variables to hold parsed HTML
        self.cur_url = -1
        self.cur_page = -1
        self.html_tree = -1

    def parse_url(self, url, cur_page):
        # save the url
        self.cur_url = url

        # save the page number
        self.cur_page = cur_page

        # fetch the webpage
        page = requests.get(url)

        # parse the webpage
        self.html_tree = html.fromstring(page.content)


class KijijiScraper(HtmlScraper):
    # parse until the last page of the given url
    def parse_till_end(self):
        while (1):
            o = self.parse_next_page()
            if o == -1:
                return 0

    # parse the next page of the given url
    def parse_next_page(self):
        # check if the current page is already the last page
        if self.is_last_page():
            print('last page reached\n')
            return -1
        print('current page: ' + str(self.cur_page + 1) + '\n')

        # generate the url of the next page
        nexturl = self.url_page(self.cur_url, self.cur_page + 1)

        # parse the generated url
        self.parse_url(nexturl, self.cur_page + 1)

        return 0

    # generate url to the specified page
    def url_page(self, url, page):
        start = re.search('https://www.kijiji.ca/([a-z]|[A-Z]|[-])+/([a-z]|[A-Z]|[-])+/', url)
        if not start:
            start = re.search('https://kijiji.ca/([a-z]|[A-Z]|[-])+/([a-z]|[A-Z]|[-])+/', url)

        end = re.search('/[a-zA-z0-9]+$', url)

        return start.group(0) + 'page-' + str(page) + end.group(0)

    # parse the "current ads/max ads"
    # check if current ads == max ads
    def is_last_page(self):
        # parsed text will give "Showing <Nat> - <Nat> out of <Nat> Ads"
        text = self.html_tree.xpath('//div[@class="col-2"]//div[@class="top-bar"]//div[@class="showing"]/text()')[
            0].strip()
        matches = re.findall('[0-9]+', text)
        if matches:
            cur = matches[1]
            print(cur)
            max = matches[2]
            print(max)
        else:
            raise ValueError('Parsing failed')

        return cur == max

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
        trimmed = re.search('(([-/_!0-9\'":])|(\w+)| +)+', title.strip())
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

    def get_listings(self):
        ids = self.get_listingids()
        titles = self.get_postingtitles()
        prices = self.get_prices()
        urls = self.get_listingurls()

        listings = []
        for i in range(len(ids)):
            listing = Listing()
            listing.set_id(ids[i])
            listing.set_title(titles[i])
            listing.set_price(prices[i])
            listing.set_url(urls[i])

            listings += [listing]

        return listings
