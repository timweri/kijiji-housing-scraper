#!/usr/bin/python3

import logging

from datetime import datetime

logger = logging.getLogger(__name__)


class Listing:
    def __init__(self):
        # unique id of a posting
        self._id = -1

        # unique id of a category
        self._cat_id = -1

        # unique id of a location
        self._loc_id = -1

        # title of the posting
        self._title = -1

        # price of the posting
        self._price = -1

        # the listing url
        self._url = -1

        # publish date
        # currently derived from the time the listing is scraped
        self._pubdate = -1

        # address
        # is a string describing the address
        self._addr = -1

        # number of bedrooms
        self._bedroomqty = -1

        # number of bathrooms
        self._bathroomqty = -1

        # pet friendly flag
        # whether the place is pet friendly
        self._pet_friendly_flag = -1

        # size of the place, in square
        self._size = -1

        # urgent posting flag
        self._urgent_flag = -1

        # furnished flag
        # whether the place is furnished
        self._furnished_flag = -1

        # the description
        self._description = -1

    def __repr__(self):
        pass

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
    def set_description(self, value):
        if type(value) != str:
            logger.error('TypeError: description must be a str')
            raise TypeError('description must be a str')
        self.description = value

    @property
    def bedroomqty(self):
        return self._bedroomqty

    @bedroomqty.setter
    def bedroomqty(self, value):
        try:
            value + 1
        except TypeError:
            logger.error('TypeError: bedroomqty must be a number')
            raise TypeError('bedroomqty must be a number')
        self._bedroomqty = value

    @property
    def bathroomqty(self):
        return self._bathroomqty

    @bathroomqty.setter
    def bathroomqty(self, value):
        try:
            value + 1
        except TypeError:
            logger.error('TypeError: bathroomqty must be a number')
            raise TypeError('bathroomqty must be a number')
        self._bathroomqty = value

    @property
    def furnished_flag(self):
        return self._furnished_flag

    @furnished_flag.setter
    def furnished_flag(self, value):
        if type(value) != bool:
            logger.error('TypeError: furnished_flag must be a bool')
            raise TypeError('furnished_flag must be a bool')
        self._furnished_flag = value

    @property
    def pet_friendly_flag(self):
        return self._pet_friendly_flag

    @pet_friendly_flag.setter
    def pet_friendly_flag(self, value):
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
