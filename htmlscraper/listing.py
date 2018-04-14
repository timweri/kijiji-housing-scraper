#!/usr/bin/python3

import logging

from datetime import datetime

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
            logger.debug('value == -1: bedroomqty not updated')
            return
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
        if value == -1:
            logger.debug('value == -1: bathroomqty not updated')
            return
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
