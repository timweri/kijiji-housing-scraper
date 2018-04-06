#!/usr/bin/python3

import json
import re
import time
from datetime import datetime

import requests
from listing import Listing
from lxml import html


class HtmlScraper:
    def __init__(self):
        # declare class variables to hold parsed HTML
        self.cur_url = -1
        self.cur_page = -1
        self.html_tree = -1

        self.out_list = []

    def parse_url(self, url, cur_page):
        if type(url) != str:
            raise TypeError('The url has to be a str.')

        if type(cur_page) != int:
            raise TypeError('The page has to be an int.')

        # save the url
        self.cur_url = url

        # save the page number
        self.cur_page = cur_page

        # fetch the webpage
        page = requests.get(url)

        # parse the webpage
        self.html_tree = html.fromstring(page.content)

        # reset output list
        self.out_list = []


class KijijiScraper(HtmlScraper):
    KIJIJI_URL_PREFIX = 'https://kijiji.ca'

    # parse the individual listing
    # return the filled in listing object
    def parse_listing(self, listing_url, listing):
        if type(listing_url) != str:
            raise TypeError('listing_url has to be a str.')
        if not isinstance(listing, Listing):
            raise TypeError('lising has to be a Listing')

        # fetch the webpage of individual listing
        page = requests.get(listing_url)

        # parse the webpage
        html_tree = html.fromstring(page.content)

        # read all the individual listing attributes
        listing.set_title(self.get_postingtitle(html_tree))
        listing.set_location(self.get_listing_loc(html_tree))
        listing.set_bedrooms(self.get_listing_bedroom(html_tree))

        tmp = self.get_listing_furnished(html_tree)
        if type(tmp) == bool:
            listing.set_furnished(tmp)

        listing.set_bathrooms(self.get_listing_bathroom(html_tree))

        tmp = self.get_listing_petfriendly(html_tree)
        if type(tmp) == bool:
            listing.set_petfriendly(tmp)

        listing.set_description(self.get_listing_description(html_tree))
        listing.set_price(self.get_price(html_tree))
        listing.set_pubdate(datetime.now())

    # parse the description and return a list of strings
    def get_listing_description(self, html_tree):
        desc = html_tree.xpath('//div[@class="descriptionContainer-2832520341"]//div//p/text()')
        if not desc:
            raise UserWarning('Missing description.')
            return -1
        return desc

    # parse the value of "Location" and return a string
    def get_listing_loc(self, html_tree):
        loc = html_tree.xpath('//span[@class="address-2932131783"]/text()')
        if loc:
            loc = loc[0].strip()
        else:
            raise UserWarning('Missing location information.')
            return -1
        return loc

    # parse the value of "Pet Friendly" and return an int
    def get_listing_petfriendly(self, html_tree):
        petfriendly = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Pet Friendly")]/dd[@class="attributeValue-1550499923"]/text()')
        if petfriendly:
            petfriendly = petfriendly[0].strip()
        else:
            return -1
        if petfriendly == 'No':
            return False
        elif petfriendly == 'Yes':
            return True
        else:
            raise ValueError('Invalid "Furnished" value.')
            return -1

    # parse the value of "Furnished" and return an int
    def get_listing_size(self, html_tree):
        size = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Size")]/dd[@class="attributeValue-1550499923"]/text()')
        if size:
            size = size[0].strip()
        else:
            return -1
        return int(size)

    # parse the value of "Furnished" and return an int
    def get_listing_furnished(self, html_tree):
        furnished = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Furnished")]/dd[@class="attributeValue-1550499923"]/text()')
        if furnished:
            furnished = furnished[0].strip()
        else:
            return -1
        if furnished == 'No':
            return False
        elif furnished == 'Yes':
            return True
        else:
            raise ValueError('Invalid "Furnished" value.')
            return -1

    # parse the number of bathrooms and return a float

    def get_listing_bathroom(self, html_tree):
        bathroom = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Bathroom")]/dd[@class="attributeValue-1550499923"]/text()')[
            0]
        bathroom = re.search('[0-9.]+', bathroom)
        if bathroom:
            return float(bathroom.group(0))
        else:
            raise ValueError("Parsing failed for bathroom number.")
            return -1

    # parse the number of bedrooms and return a float
    # called in listing parsing
    def get_listing_bedroom(self, html_tree):
        bedroom = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Bedroom")]/dd[@class="attributeValue-1550499923"]/text()')
        if bedroom:
            bedroom = re.search('[0-9.]+', bedroom[0])
            if bedroom:
                return float(bedroom.group(0))
            else:
                raise ValueError("Parsing failed for bedroom number.")
                return -1
        else:
            return -1

    def parse_all_category(self, filename):
        self.subcategory_url_fetcher(self.cur_url, filename)
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
        start = re.search(self.KIJIJI_URL_PREFIX + '/([a-z]|[A-Z]|[-])+/([a-z]|[A-Z]|[-])+/', url)
        if not start:
            start = re.search(self.KIJIJI_URL_PREFIX + '/([a-z]|[A-Z]|[-])+/([a-z]|[A-Z]|[-])+/', url)

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
            raise ValueError('Cannot find the page number.')
            return -1

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

    # get price
    # called in listing parsing
    def get_price(self, html_tree):
        # extract prices into a list of prices
        price = html_tree.xpath(
            '//h1[@class="title-3283765216"]//div[@class="priceContainer-4015170679"]//span[@class="currentPrice-2872355490"]/text()')
        # remove useless characters from the extracted prices
        price = self.price_trim(price)

        if price == "Please Contact":
            price = 0
        else:
            price = float(price)

        return price

    def title_trim(self, title):
        # extract the title where only whitespaces, numbers and alphebetical characters are allowed
        trimmed = re.search('(([-/_!0-9\'":])|(\w+)| +)+', title.strip())
        if trimmed:  # if pattern is matched
            return trimmed.group(0)
        else:  # if pattern is not found
            # print(erpr(title))
            return -1  # -1 signal there is a problem

    # get listing title
    # called in listing parsing
    def get_postingtitle(self, html_tree):
        # extract product names into a list of names
        title = html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@class="title"]//a[@href and @class="title enable-search-navigation-flag "]/text()')
        # remove useless characters from the extracted titles

        if type(title) != str:
            raise TypeError('title has to be a str.')
            return -1

        return title

    # get listing ids
    # called in listing parsing
    def get_listingid(self, html_tree):
        # extract listing id
        id = html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@data-ad-id and @data-vip-url]/@data-ad-id')

        id = int(id)

        return id

    # get lising url
    # called in subcategory parsing
    def get_listingurls(self):
        # extract listing urls into a list of urls
        urls = self.html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@data-ad-id and @data-vip-url]/@data-vip-url')
        return urls

    # parse all listings on a page
    # compile all listings into a list of Listing objects.
    def get_listings(self):
        # get all the urls on the page
        urls = self.get_listingurls()

        # initiate list of parsed listing
        listings = []

        for i in range(len(urls)):
            # make an empty Listing object
            listing = Listing()

            # find the full url
            url = self.KIJIJI_URL_PREFIX + str(urls[i])

            # save the url
            listing.set_url(url)

            # reduce the request frequency
            time.sleep(0.5)

            # fill in the rest of the listing
            self.parse_listing(url, listing)

            # add the current listing to the list of listings
            listings += [listing]

        return listings
