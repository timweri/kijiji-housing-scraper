#!/usr/bin/python3

import json
import logging
import re
import time
from datetime import datetime

import requests
from lxml import html

from htmlscraper.listing import Listing

logger = logging.getLogger(__name__)


class KijijiScraper():
    KIJIJI_URL_PREFIX = 'https://kijiji.ca'

    def __init__(self):
        # declare class variable
        self._cur_url = -1
        self._cur_page = -1
        self._html_tree = -1

        # unique id of a category
        self._cur_cat_id = -1

        # unique id of a location
        self._cur_loc_id = -1

    # prepare to scrape the category of the given url
    # returns nothing
    def scrape_cat_ini(self, url):
        if type(url) != str:
            logger.error('TypeError: The url has to be a str')
            raise TypeError('The url has to be a str')

        # ini class parameters
        self._cur_url = url
        self._cur_page = 1

        # fetch the webpage
        page = requests.get(url)

        # parse the webpage
        self._html_tree = html.fromstring(page.content)

        self._cur_cat_id = self.get_cat_id(url)
        self._cur_loc_id = self.get_loc_id(url)

    # extract the cat_id from the given url
    # return the cat_id as an int
    @staticmethod
    def get_cat_id(url):
        logger.debug('Extracting cat_id from url')
        if type(url) != str:
            logger.error('TypeError: The url has to be a str')
            raise TypeError('The url has to be a str')

        tmp = re.search('(?<=/c)[0-9]+(?=l[0-9]{4})', url)
        if not tmp:
            logger.error('ValueError: cat_id extraction unsuccessful')
            raise ValueError('cat_id extraction unsuccessful')

        tmp = int(tmp.group(0))

        logger.debug('cat_id extraction successful')
        return tmp

    # extract the loc_id from the given url
    # return the loc_id as an int
    @staticmethod
    def get_loc_id(url):
        logger.debug('Extracting loc_id from url')
        if type(url) != str:
            logger.error('TypeError: The url has to be a str')
            raise TypeError('The url has to be a str')

        tmp = re.search('(?<=/c)[0-9]+l[0-9]+', url)
        if not tmp:
            logger.error('ValueError: cat_id extraction unsuccessful')
            raise ValueError('cat_id extraction unsuccessful')

        tmp = re.search('(?<=l)[0-9]+', tmp.group(0))
        if not tmp:
            logger.error('ValueError: cat_id extraction unsuccessful')
            raise ValueError('cat_id extraction unsuccessful')

        tmp = int(tmp.group(0))

        logger.debug('loc_id extraction successful')
        return tmp

    # parse the description and return a string
    @staticmethod
    def get_listing_description(html_tree):
        raw = html_tree.xpath(
            '//div[@class="descriptionContainer-2832520341"]//div//*/text() | //div[@class="descriptionContainer-2832520341"]//div/text()')
        if not raw:
            raise UserWarning('"description" attribute not found')

        value = ""

        for s in raw:
            value += s + '\n'

        logger.debug('"description" attribute extraction successful')
        return value

    # parse the address and return a string
    @staticmethod
    def get_listing_addr(html_tree):
        raw = html_tree.xpath('//span[@class="address-2932131783"]/text()')
        if raw:
            value = raw[0].strip()
        else:
            logger.error('"address" attribute not found')
            raise UserWarning('"address" attribute not found')

        logger.debug('"address" attribute extraction successful')
        return value

    # parse the value of "Pet Friendly" and return a bool
    @staticmethod
    def get_listing_pet_friendly(html_tree):
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Pet Friendly")]/dd[@class="attributeValue-1550499923"]/text()')
        if raw:
            value = raw[0].strip()
        else:
            logger.debug('"pet friendly" attribute not found')
            return -1

        if value == 'No':
            logger.debug('"pet_friendly" attribute extraction successful')
            return False
        elif value == 'Yes':
            logger.debug('"pet_friendly" attribute extraction successful')
            return True
        else:
            logger.error('ValueError: invalid "pet friendly" attribute value')
            raise ValueError('Invalid "pet friendly" attribute value')

    # parse the value of "Furnished" and return an int
    @staticmethod
    def get_listing_size(html_tree):
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Size")]/dd[@class="attributeValue-1550499923"]/text()')
        if not raw:
            logger.debug('"size" attribute not found')
            return -1

        value = raw[0].strip()

        logger.debug('"size" attribute extraction successful')
        return float(value)

    # parse the value of "Furnished" and return a bool
    @staticmethod
    def get_listing_furnished(html_tree):
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Furnished")]/dd[@class="attributeValue-1550499923"]/text()')
        if raw:
            value = raw[0].strip()
        else:
            logger.debug('"furnished" attribute not found')
            return -1

        if value == 'No':
            logger.debug('"furnished" attribute extraction successful')
            return False
        elif value == 'Yes':
            logger.debug('"furnished" attribute extraction successful')
            return True
        else:
            logger.error('ValueError: invalid "furnished" attribute value')
            raise ValueError('Invalid "furnished" attribute value')

    # parse the number of bathrooms and return a float
    @staticmethod
    def get_listing_bathroomqty(html_tree):
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Bathroom")]/dd[@class="attributeValue-1550499923"]/text()')
        if not raw:
            logger.debug('"bathroom quantity" attribute not found')
            return -1

        value = re.search('[0-9.]+', raw[0])
        logger.debug('"bathroom quantity" extraction successful')
        return float(value.group(0))

    # parse the number of bedrooms and return a float
    # called in listing parsing
    @staticmethod
    def get_listing_bedroomqty(html_tree):
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Bedroom")]/dd[@class="attributeValue-1550499923"]/text()')
        if not raw:
            logger.debug('"bedroom quantity" attribute not found')
            return -1

        value = re.search('[0-9.]+', raw[0])
        logger.debug('"bedroom quantity" extraction successful')
        return float(value.group(0))

    # get price
    # called in listing parsing
    @staticmethod
    def get_listing_price(html_tree):
        raw = html_tree.xpath(
            '//span[@class="currentPrice-2872355490"]/text() | //span[@class="currentPrice-2872355490"]//span/text()')
        if not raw:
            logger.error('price not found')
            raise ValueError('price not found')
        if raw[0] == "Please Contact" or raw[0] == "Swap/Trade":
            price = 0.0
        else:
            price = re.sub('[$,]', '', raw[0])
            price = float(price)

        logger.debug('price extraction successful')
        return price

    # get listing title
    # called in listing parsing
    @staticmethod
    def get_listing_title(html_tree):
        # extract product names into a list of names
        raw = html_tree.xpath(
            '//h1[@class="title-3283765216"]/text()')

        if not raw:
            logger.error('title not found')
            raise ValueError('title not found')

        # process the raw strings:
        value = ' '.join(raw)

        value = re.sub(' +', ' ', value)

        logger.debug('title extraction successful')
        return value

    # get listing ids
    # called in listing parsing
    @staticmethod
    def get_listing_id(html_tree):
        raw = html_tree.xpath(
            '//li[@class="currentCrumb-2617455686"]//span/text()')
        if not raw:
            logger.error('id not found')
            raise ValueError('id not found')

        value = int(raw[0])
        logger.debug('id extraction successful')
        return value

    # scrape the individual listing
    # return a Listing object
    def scrape_listing(self, listing_url):
        if type(listing_url) != str:
            logger.error('TypeError: listing_url has to be a str')
            raise TypeError('listing_url has to be a str')

        listing = Listing(url=listing_url, loc_id=self._cur_loc_id, cat_id=self._cur_cat_id)

        html_tree = self.get_html_tree(listing_url)

        # scrape all the individual listing attributes
        listing.title = self.get_listing_title(html_tree)
        listing.id = self.get_listing_id(html_tree)
        listing.addr = self.get_listing_addr(html_tree)
        listing.price = self.get_listing_price(html_tree)
        listing.pubdate = datetime.now()

        listing.bedroomqty = self.get_listing_bedroomqty(html_tree)
        listing.bathroomqty = self.get_listing_bathroomqty(html_tree)

        listing.furnished_flag = self.get_listing_furnished(html_tree)
        listing.pet_friendly_flag = self.get_listing_pet_friendly(html_tree)

        listing.description = self.get_listing_description(html_tree)

        logger.debug('Listing successfully scraped')
        return listing

    def parse_all_category(self, filename):
        self.subcategory_url_fetcher(self._cur_url, filename)
        with open(filename, 'r') as fp:
            data = json.load(fp)
        for url in data['url']:
            self.parse_url(url, 1)
            self.par

    # fetch all Kijiji subcategories on the given Kijiji page
    # organize these subcategories into a dict
    # dump this dict into a JSON file titled <filename>
    def subcategory_url_fetcher(self, url, filename):
        page = requests.get(url)
        html_tree = html.fromstring(page.content)

        urls = html_tree.xpath(
            '//div[@class="content"]//li//a[@class="category-selected" and @data-event="ChangeCategory"]/@href')
        urls = list(map(lambda x: "https://www.kijiji.ca" + x, urls))
        titles = html_tree.xpath(
            '//div[@class="content"]//li//a[@class="category-selected" and @data-event="ChangeCategory"]/text()')
        titles = list(map(lambda x: x.strip(), titles))
        ids = html_tree.xpath(
            '//div[@class="content"]//li//a[@class="category-selected" and @data-event="ChangeCategory"]/@data-id')
        ids = list(map(lambda x: int(x.strip()), ids))

        d = dict()
        d['category'] = []

        for i in range(0, len(urls)):
            cat = dict()
            cat['id'] = ids[i]
            cat['title'] = titles[i]
            cat['url'] = urls[i]
            d['category'].append(cat)

        return d

    # parse until the last page of the given url
    def parse_till_end(self):
        while (1):
            o = self.parse_next_page()
            if o == -1:
                return 0
            else:
                self.get_listings()

    # parse the next page of the given url
    def parse_next_page(self):
        # check if the current page is already the last page
        if self.is_last_page():
            print('Last page reached\n')
            return -1
        print('Current page: ' + str(self._cur_page + 1) + '\n')

        # generate the url of the next page
        nexturl = self.url_page(self._cur_url, self._cur_page + 1)

        # parse the generated url
        self.parse_url(nexturl, self._cur_page + 1)

        return 0

    # generate url to the specified page
    def url_page(self, url, page):
        start = re.search(self.KIJIJI_URL_PREFIX + '/([a-z]|[A-Z]|[-])+/([a-z]|[A-Z]|[-])+/', url)
        if not start:
            start = re.search(self.KIJIJI_URL_PREFIX + '/([a-z]|[A-Z]|[-])+/([a-z]|[A-Z]|[-])+/', url)

        end = re.search('/[a-zA-z0-9]+$', url)

        return start.group(0) + 'page-' + str(page) + end.group(0)

    # parse the "current ads/max ads"
    # check if current ads == max ads
    def is_last_page(self):
        # parsed text will give "Showing <Nat> - <Nat> out of <Nat> Ads"
        text = self._html_tree.xpath('//div[@class="col-2"]//div[@class="top-bar"]//div[@class="showing"]/text()')[
            0].strip()
        matches = re.findall('[0-9]+', text)
        if matches:
            cur = matches[1]
            print(cur)
            max = matches[2]
            print(max)
        else:
            raise ValueError('Page numebr not found')
            return -1

        return cur == max

    # get listing urls from the current category
    # called in category parsing
    def get_cat_urls(self):
        # extract listing urls into a list of urls
        raws = self._html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@data-ad-id and @data-vip-url]/@data-vip-url')
        print(raws)
        logger.debug('Category urls extraction successful')
        return raws

    # scrape all listings on a category page
    # compile all listings into a list of Listing objects.
    def get_cat_listings(self):
        logger.info('Scraping listings from {:s}'.format(self._cur_url))
        # get all the urls on the page
        urls = self.get_cat_urls()

        # initiate list of Listing objects
        listings = []

        for i in range(len(urls)):
            url = self.KIJIJI_URL_PREFIX + str(urls[i])
            listing = self.scrape_listing(url)
            listings += [listing]
            time.sleep(0.5)

        logger.info('Category successfully scraped')
        return listings

    @staticmethod
    def get_html_tree(url):
        page = requests.get(url)
        html_tree = html.fromstring(page.content)
        return html_tree
