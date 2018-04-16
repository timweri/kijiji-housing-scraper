#!/usr/bin/python3

import logging
import re
import sys
import threading
import time
from datetime import datetime
from queue import Queue

import MySQLdb
import requests
from lxml import html

logging.basicConfig(handlers=[logging.FileHandler('main.log'), logging.StreamHandler(sys.stdout)], level=logging.INFO,
                    format='%(filename)8s: '
                           '%(levelname)8s: '
                           '%(funcName)25s(): '
                           '%(lineno)d:\t'
                           '%(message)s')
logger = logging.getLogger(__name__)


class Listing:
    def __init__(self, id=-1, cat_id=-1, loc_id=-1, title=-1, price=-1, url=-1, pubdate=-1, addr=-1, bedroomqty=-1,
                 bathroomqty=-1, pet_friendly=-1, size=-1, urgent=0, furnished=-1, description=-1):
        # unique id of a posting
        self._id = id

        # unique id of a category
        self._cat_id = cat_id

        # unique id of a location
        self._loc_id = loc_id

        # title of the posting
        self._title = title

        # price of the posting
        self._price = price

        # the listing url
        self._url = url

        # publish date
        # currently derived from the time the listing is scraped
        self._pubdate = pubdate

        # address
        # is a string describing the address
        self._addr = addr

        # number of bedrooms
        self._bedroomqty = bedroomqty

        # number of bathrooms
        self._bathroomqty = bathroomqty

        # pet friendly flag
        # whether the place is pet friendly
        self._pet_friendly_flag = pet_friendly

        # size of the place, in square
        self._size = size

        # urgent posting flag
        self._urgent_flag = urgent

        # furnished flag
        # whether the place is furnished
        self._furnished_flag = furnished

        # the description
        self._description = description

    def __repr__(self):
        output = 'Listing:'
        output += '\nid: {:d}'.format(self.id)
        output += '\ncat_id: {:d}'.format(self.cat_id)
        output += '\nloc_id: {:d}'.format(self.loc_id)
        output += '\ntitle: {:s}'.format(self.title)
        output += '\nurl: {:s}'.format(self.url)
        output += '\nprice: {:f}'.format(self.price)
        output += '\nbedroom quantity: {:f}'.format(self.bedroomqty)
        output += '\nbathroom quantity: {:f}'.format(self.bathroomqty)
        output += '\nfurnished: {:b}'.format(self.furnished_flag)
        output += '\npet friendly: {:b}'.format(self.pet_friendly_flag)
        output += '\nsize: {:f}'.format(self.size)
        output += '\ndescription:\n' + self.description
        return output

    def __eq__(self, other):
        return isinstance(other, Listing) and self.id == other.id

    def __ne__(self, other):
        return isinstance(other, Listing) and self.id != other.id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) != int:
            logger.error('TypeError: id must be an int')
            raise TypeError('id must be an int')
        self._id = value

    @property
    def loc_id(self):
        return self._loc_id

    @loc_id.setter
    def loc_id(self, value):
        if type(value) != int:
            logger.error('TypeError: loc_id must be an int')
            raise TypeError('loc_id must be an int')
        self._loc_id = value

    @property
    def cat_id(self):
        return self._cat_id

    @cat_id.setter
    def cat_id(self, value):
        if type(value) != int:
            logger.error('TypeError: cat_id must be an int')
            raise TypeError('cat_id must be an int')
        self._cat_id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value == -1:
            logger.error('title not updated')
            return
        if type(value) != str:
            logger.error('TypeError: title must be an str')
            raise TypeError('title must be a str')
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if type(value) != float:
            logger.error('TypeError: price must be a float')
            raise TypeError('price must be a float')
        self._price = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if type(value) != str:
            logger.error('TypeError: url must be a str')
            raise TypeError('url must be a str')
        self._url = value

    @property
    def pubdate(self):
        return self._pubdate

    @pubdate.setter
    def pubdate(self, value):
        if type(value) != datetime:
            logger.error('TypeError: pubdate must be a datetime')
            raise TypeError('pubdate must be a datetime')
        self._pubdate = value

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        if type(value) != str:
            logger.error('TypeError: addr must be a str')
            raise TypeError('addr must be a str')
        self._addr = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value == -1:
            logger.debug('value == -1: description not updated')
            return
        if type(value) != str:
            logger.error('TypeError: description must be a str')
            raise TypeError('description must be a str')
        self._description = value

    @property
    def bedroomqty(self):
        return self._bedroomqty

    @bedroomqty.setter
    def bedroomqty(self, value):
        if value == -1:
            logger.debug('bedroomqty not updated')
            return
        if type(value) != int:
            logger.error('TypeError: bedroomqty must be an int')
            raise TypeError('bedroomqty must be an int')
        self._bedroomqty = value

    @property
    def bathroomqty(self):
        return self._bathroomqty

    @bathroomqty.setter
    def bathroomqty(self, value):
        if value == -1:
            logger.debug('bathroomqty not updated')
            return
        if type(value) != int:
            logger.error('TypeError: bathroomqty must be an int')
            raise TypeError('bathroomqty must be a int')
        self._bathroomqty = value

    @property
    def furnished_flag(self):
        return self._furnished_flag

    @furnished_flag.setter
    def furnished_flag(self, value):
        if value == -1:
            logger.debug('value == -1: furnished_flag not updated')
            return
        if type(value) != bool:
            logger.error('TypeError: furnished_flag must be a bool')
            raise TypeError('furnished_flag must be a bool')
        self._furnished_flag = value

    @property
    def pet_friendly_flag(self):
        return self._pet_friendly_flag

    @pet_friendly_flag.setter
    def pet_friendly_flag(self, value):
        if value == -1:
            logger.debug('value == -1: pet_friendly_flag not updated')
            return
        if type(value) != bool:
            logger.error('TypeError: pet_friendly_flag must be a bool')
            raise TypeError('pet_friendly_flag must be an bool')
        self._pet_friendly_flag = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def urgent_flag(self):
        return self._urgent_flag

    @urgent_flag.setter
    def urgent_flag(self, value):
        if type(value) != bool:
            logger.error('TypeError: urgent_flag must be a bool')
            raise TypeError('urgent_flag must be a pool')
        self._urgent_flag = value


class MySQLConnectionPool:
    def __init__(self, hostaddr, usr, pwd, dbname, poolsize=2):
        logger.info('Initializing an instance of MySQLConnectionPool')
        logger.debug('Type checking for host address, username, password, database name and pool size')
        if type(hostaddr) != str:
            raise TypeError('hostaddr has to be a str')
        if type(usr) != str:
            raise TypeError('usr has to be a str')
        if type(pwd) != str:
            raise TypeError('pwd has to be a str')
        if type(dbname) != str:
            raise TypeError('dbname has to be a str')
        logger.debug('All type checks passed')

        logger.info('Initializing class variables')
        # save MySQL server authentication
        self._hostaddr = hostaddr
        self._usr = usr
        self._pwd = pwd
        self._dbname = dbname

        logger.info('Initializing MySQL connection pool')
        # initiate an empty Queue of required size
        self._pool = Queue(poolsize)

        # fill the pool up
        for i in range(poolsize):
            connection = MySQLdb.connect(hostaddr, usr, pwd, dbname)

            # use utf8mb4 encoder
            # Kijiji description contains utf8 characters that requires
            # 4 bytes to store
            connection.set_character_set('utf8mb4')
            connection.cursor().execute('SET NAMES utf8mb4;')
            connection.cursor().execute('SET CHARACTER SET utf8mb4;')
            connection.cursor().execute('SET character_set_connection=utf8mb4;')

            self._pool.put(connection, block=False)
        logger.info('Initialized MySQL connection pool')

    # return an available connection from the pool
    def get_connection(self):
        logger.debug('Retrieving connection from the pool')
        db = self._pool.get()

        logger.debug('Type checking connection')
        if not isinstance(db, MySQLdb.connections.Connection):
            raise TypeError('A connection has to be of type MySQLdb.connections.Connection')

        logger.info('Successful MySQL connection get request')
        return db

    # queue a connection to the pool
    def put_connection(self, connection):
        logger.debug('Type checking connection')
        if not isinstance(connection, MySQLdb.connections.Connection):
            raise TypeError('A connection has to be of type MySQLdb.connections.Connection')

        self._pool.put_nowait(connection)
        self._pool.task_done()
        logger.info('Successful MySQL connection put request')
        return 0

    # close all connections
    def clear_pool(self):
        logger.info('Closing the MySQL connection pool (id {})'.format(id(self)))
        while not self._pool.empty():
            db = self._pool.get()
            if not isinstance(db, MySQLdb.connections.Connection):
                raise TypeError('A non-Connection object found in the connection pool')
            db.close()
            self._pool.task_done()
        logger.info('Closed all connections in the MySQL connection pool (id {})'.format(id(self)))
        return 0


class KijijiScraper:
    KIJIJI_URL_PREFIX = 'kijiji.ca'
    MAX_ATTEMPTS = 2

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
    def scrape_cat_page_ini(self, url, page=1):
        if type(url) != str:
            logger.error('TypeError: The url has to be a str')
            raise TypeError('The url has to be a str')

        # ini class parameters
        self._cur_url = url
        self._cur_page = page

        # fetch the webpage
        page = requests.get(url)

        # parse the webpage
        self._html_tree = html.fromstring(page.content)

        self._cur_cat_id = self._get_cat_id(url)
        self._cur_loc_id = self._get_loc_id(url)

    # extract the cat_id from the given url
    # return the cat_id as an int
    @staticmethod
    def _get_cat_id(url):
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
    def _get_loc_id(url):
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
    def _get_listing_description(html_tree):
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
    def _get_listing_addr(html_tree):
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
    def _get_listing_pet_friendly(html_tree):
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
    def _get_listing_furnished(html_tree):
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

    # parse the number of bathrooms and return an int identifier
    # called in listing scraping
    @staticmethod
    def _get_listing_bathroomqty(html_tree):
        value_dict = {'1 bathroom': 1, '1.5 bathrooms': 2, '2 bathrooms': 3, '2.5 bathrooms': 4, '3 bathrooms': 5,
                      '3.5 bathrooms': 6, '4 bathrooms': 7, '4.5 bathrooms': 8, '5 bathrooms': 9,
                      '5.5 bathrooms': 10,
                      '6 or more bathrooms': 11}
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Bathroom")]/dd[@class="attributeValue-1550499923"]/text()')
        if raw:
            key = raw[0].strip()
            return value_dict[key]

        logger.debug('"bathroom quantity" attribute not found')
        return -1

    # parse the number of bedrooms and return an int identifier
    # called in listing scraping
    @staticmethod
    def _get_listing_bedroomqty(html_tree):
        value_dict = {'1 Bedroom': 1, '1 bedroom': 1, '1 bedroom + den': 2, '1 bedroom and den': 2,
                      '1 Bedroom + Den': 2, '2 bedrooms': 3, '2 Bedroom': 3, '2 bedrooms and den': 4,
                      '3 Bedroom': 5,
                      '3 bedrooms': 5, '4 bedrooms': 6, '5 bedrooms': 7, '6 or more bedrooms': 8,
                      'Bachelor or studio': 9,
                      '4+ Bedroom': 10, 'Bachelor & Studio': 9}
        keys = ['1 Bedroom', '1 Bedroom + Den', '2 Bedroom', '3 Bedroom', '4+ Bedroom', 'Bachelor & Studio']
        raw = html_tree.xpath(
            '//dl[@class="itemAttribute-304821756" and contains(.,"Bedroom")]/dd[@class="attributeValue-1550499923"]/text()')
        if raw:
            key = raw[0].strip()
            return value_dict[key]

        raw = html_tree.xpath(
            '//li[@class="crumbItem-1566965652"]//h1[@class="crumbH1-75073251"]//a[@class="crumbLink-3348846382"]//span[@itemprop="name"]/text()')
        if raw:
            for k in keys:
                if raw[0].find(k) != -1:
                    return value_dict[k]

        logger.debug('"bedroom quantity" attribute not found')
        return -1

    # get price
    # called in listing parsing
    @staticmethod
    def _get_listing_price(html_tree):
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
    def _get_listing_title(html_tree):
        # extract product names into a list of names
        raw = html_tree.xpath(
            '//h1[@class="title-3283765216"]/text()')

        if not raw:
            logger.error('title not found')
            return -1

        # process the raw strings:
        value = ' '.join(raw)

        value = re.sub(' +', ' ', value)

        logger.debug('title extraction successful')
        return value

    # get listing ids
    # called in listing parsing
    @staticmethod
    def _get_listing_id(html_tree):
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

        html_tree = self._get_html_tree(listing_url)

        # scrape all the individual listing attributes
        # try for a limited amount of time before throwing error if no title is found
        listing.title = self._attempt(self._get_listing_title, self.MAX_ATTEMPTS, html_tree)
        if listing.title == -1:
            raise ValueError('title not found')

        listing.id = self._get_listing_id(html_tree)
        listing.addr = self._get_listing_addr(html_tree)
        listing.price = self._get_listing_price(html_tree)
        listing.pubdate = datetime.now()

        listing.bedroomqty = self._get_listing_bedroomqty(html_tree)
        listing.bathroomqty = self._get_listing_bathroomqty(html_tree)

        listing.furnished_flag = self._get_listing_furnished(html_tree)
        listing.pet_friendly_flag = self._get_listing_pet_friendly(html_tree)

        listing.description = self._get_listing_description(html_tree)

        logger.info('Listing #{:d} successfully scraped'.format(listing.id))
        return listing

    # parse the next page of the given url
    def scrape_next_page(self):
        # check if the current page is already the last page
        if self._is_last_cat_page():
            logger.info('Last page reached')
            return -1

        self._cur_page += 1
        logger.info('Scraping page number: {:d}'.format(self._cur_page))

        # generate the url of the next page
        next_url = self._gen_cat_page_url(self._cur_url, self._cur_page)

        # parse the generated url
        self.scrape_cat_page_ini(next_url, self._cur_page)
        return self.get_cat_page_listings()

    # generate url to the specified page
    def _gen_cat_page_url(self, url, page):
        start = re.search(self.KIJIJI_URL_PREFIX + '/[a-zA-Z-]+/[a-zA-Z-]+/', url)
        end = re.search('/[a-zA-z0-9]+$', url)
        return 'https://www.{:s}page-{:d}{:s}'.format(start.group(0), page, end.group(0))

    # parse the "current ads/max ads"
    # check if current ads == max ads
    def _is_last_cat_page(self):
        # parsed text will give "Showing <Nat> - <Nat> out of <Nat> Ads"
        text = self._html_tree.xpath('//div[@class="col-2"]//div[@class="top-bar"]//div[@class="showing"]/text()')[
            0].strip()

        matches = re.findall('[0-9,]+', text)
        if matches:
            cur = matches[1]
            max = matches[2]
        else:
            raise ValueError('Page number not found')

        return cur == max

    # get listing urls from the current category
    # called in category parsing
    def _get_cat_urls(self):
        # extract listing urls into a list of urls
        raws = self._html_tree.xpath(
            '//div[@class="container-results large-images"]//div[@data-ad-id and @data-vip-url]/@data-vip-url')
        if not raws:
            logger.error('No listing urls found in the category')
            return -1
        logger.debug('Category urls extraction successful')
        return raws

    # try a function
    def _attempt(self, func, max_attempts, *args):
        tmp = -1
        attempts = 1
        while tmp == -1 and attempts <= max_attempts:
            if attempts == 1:
                logger.debug('Trying {:s}: {:d} attempt(s)'.format(func.__name__, attempts))
            else:
                time.sleep(1)
                logger.error('Trying {:s}: {:d} attempt(s)'.format(func.__name__, attempts))
            tmp = func(*args)
            attempts += 1
        logger.debug('{:s} applied successfully'.format(func.__name__))
        return tmp

    # scrape all listings on a category page
    # compile all listings into a list of Listing objects.
    def get_cat_page_listings(self):
        logger.info('Scraping listings from {:s}'.format(self._cur_url))

        # get all listing urls from the page
        urls = self._attempt(self._get_cat_urls, self.MAX_ATTEMPTS)
        # throw error if no listing is found
        if urls == -1:
            raise UserWarning('No listing is found')

        # initiate list of Listing objects
        listings = []

        for i in range(len(urls)):
            url = 'https://www.' + self.KIJIJI_URL_PREFIX + str(urls[i])
            listing = self.scrape_listing(url)
            listings += [listing]
            time.sleep(0.5)

        logger.info('Category successfully scraped')
        return listings

    @staticmethod
    def _get_html_tree(url):
        page = requests.get(url)
        html_tree = html.fromstring(page.content)
        return html_tree


class KijijiHousingBot(KijijiScraper):
    FIELDS_DICT = {'id': 'id', 'title': 'title', 'pubdate': 'publish_date',
                   'loc_id': 'location_id', 'addr': 'address', 'bedrooms': 'bedroom_qty',
                   'bathrooms': 'bathroom_qty', 'price': 'price', 'pet_friendly': 'pet_friendly_flag',
                   'furnished': 'furnished_flag', 'urgent': 'urgent_flag',
                   'url': 'url', 'size': 'size', 'desc': 'description'}

    def __init__(self, hostaddr, usr, pwd, dbname, poolsize=2):
        super(KijijiHousingBot, self).__init__()
        self._connectionpool = MySQLConnectionPool(hostaddr, usr, pwd, dbname, poolsize)

    # returns the list of completed Listings objects that are not logged
    def get_cat_page_listings(self):
        logger.info('Scraping listings from {:s}'.format(self._cur_url))

        # get all listing urls from the page
        urls = self._attempt(self._get_cat_urls, self.MAX_ATTEMPTS)
        # throw error if no listing is found
        if urls == -1:
            logger.error('No listing is found')
            raise UserWarning('No listing is found')

        urls = self._filter_logged_listing(urls)

        # initiate list of Listing objects
        listings = []

        for i in range(len(urls)):
            url = 'https://www.' + self.KIJIJI_URL_PREFIX + str(urls[i])
            listing = self.scrape_listing(url)
            listings += [listing]
            time.sleep(0.5)

        logger.info('Category successfully scraped')
        return listings

    # parse the next page of the given url
    def scrape_next_page(self):
        # check if the current page is already the last page
        if self._is_last_cat_page():
            logger.info('Last page reached')
            return -1

        self._cur_page += 1
        logger.info('Scraping page number: {:d}'.format(self._cur_page))

        # generate the url of the next page
        next_url = self._gen_cat_page_url(self._cur_url, self._cur_page)

        # parse the generated url
        self.scrape_cat_page_ini(next_url, self._cur_page)
        return self.get_cat_page_listings()

    # filters out listing that are already logged, using the id entry
    # returns a new list of urls which are not logged
    # to reduce the amount of requests needed
    def _filter_logged_listing(self, urls):
        logger.debug('Filtering out logged listings')
        connection = self._connectionpool.get_connection()
        cursor = connection.cursor()

        # extract ids from the urls
        ids = list(map(lambda x: re.search('(?<=/)[0-9]+$', x)[0], urls))

        output = []
        logged_ids = []
        unlogged_ids = []

        count = 0
        for i in range(len(urls)):
            if not self._is_logged(self.FIELDS_DICT['id'], ids[i], cursor):
                count += 1
                output.append(urls[i])
                unlogged_ids.append(ids[i])
            else:
                logged_ids.append(ids[i])
        self._connectionpool.put_connection(connection)
        logger.info('Filtered out {:d}/{:d} logged listings'.format(len(urls) - count, len(urls)))
        logger.debug('Already logged ids: {:s}'.format(str(logged_ids)))
        logger.debug('Unlogged ids: {:s}'.format(str(unlogged_ids)))
        return output

    # checks if an entry is present in the database
    # returns bool
    def _is_logged(self, field_id, id, cursor):
        sql = """SELECT id FROM c{:d} WHERE {:s} = %s""".format(self._cur_cat_id, field_id)
        try:
            cursor.execute(sql, [id])
            output = cursor.rowcount
            return bool(output)
        except:
            logger.exception('Unable to fetch data:')
            raise

    # generate sql from a listing
    def _gen_sql_insert(self, listing, cat_id):
        logger.debug('Generating MySQL command for insertion/update for table c{:d}'.format(cat_id))
        if listing.id < 0:
            logger.error('TypeError: id must be non-negative')
            logger.error('Skipping the Listing')
            return -1
        if type(listing.pubdate) != datetime:
            logger.error('TypeError: pubdate must be a datetime')
            return -1

        sql_cols = """INSERT INTO c{cat_id:d}({id:s}, {url:s}, {loc_id:s}, {title:s}, {pubdate:s}, {desc:s}""".format(
            cat_id=cat_id,
            **self.FIELDS_DICT)
        sql_vals = """) VALUES (%s, %s, %s, %s, %s, %s"""
        sql_pars = [listing.id, listing.url, listing.loc_id, listing.title,
                    listing.pubdate.strftime('%Y-%m-%d %H:%M:%S'), listing.description]

        col_list = [self.FIELDS_DICT['addr'], self.FIELDS_DICT['price'], self.FIELDS_DICT['bedrooms'],
                    self.FIELDS_DICT['bathrooms'], self.FIELDS_DICT['pet_friendly'], self.FIELDS_DICT['furnished'],
                    self.FIELDS_DICT['urgent'], self.FIELDS_DICT['size']]
        val_list = [listing.addr, listing.price, listing.bedroomqty, listing.bathroomqty, listing.pet_friendly_flag,
                    listing.furnished_flag, listing.urgent_flag, listing.size]

        for i in range(len(col_list)):
            if val_list[i] != -1:
                sql_cols += ", " + col_list[i]
                sql_vals += ", %s"
                sql_pars.append(val_list[i])

        cmd = sql_cols + sql_vals + ')'
        logger.debug('MySQL command generation successful')
        return (cmd, sql_pars)

    # add a list of listings into an existing table
    def _update_table(self, listings):
        if not listings:
            logger.warning('Did not update table. listings is empty.')
            return 0

        cat_id = listings[0].cat_id

        logger.info('Updating table c{} in the MySQL database'.format(cat_id))
        logger.info('Requesting for MySQL connection')

        db = self._connectionpool.get_connection()
        cursor = db.cursor()
        count = 0

        for l in listings:
            if not isinstance(l, Listing):
                logger.error('TypeError: Expected a Listing instance')
                logger.error('Skipping this listing')
                continue

            (sql, pars) = self._gen_sql_insert(l, cat_id)
            if sql == -1:
                # Failed to generate SQL command
                logger.error('Skipping the listing')
                continue

            try:
                logger.debug('Executing SQL command')
                cursor.execute(sql, pars)
                logger.debug('Committing changes to the database')
                db.commit()
                count += 1
                logger.info('Successfully added a listing to table c{:d}'.format(cat_id))
            except:
                db.rollback()
                logger.exception('Exception:')
                logger.error('Failed to add a listing to table c{:d}'.format(cat_id))
                logger.error('Listing url: {:s}'.format(l.url))
                logger.error('Rolled back the database changes')

        self._connectionpool.put_connection(db)
        logger.info('Released MySQL connection')
        logger.info('Successfully added {:d}/{:d} listings'.format(count, len(listings)))
        return 0

    def start(self, inputfilename='urls.in'):
        while True:
            with open(inputfilename, 'r') as f:
                for line in f:
                    self.scrape_cat_page_ini(line, 0)
                    while not self._is_last_cat_page():
                        out = self.scrape_next_page()
                        thread = threading.Thread(target=self._update_table, args=(out,))
                        thread.start()


if __name__ == '__main__':
    scraper = KijijiHousingBot('localhost', 'root', 'password', 'testdb1')
    scraper.start()
