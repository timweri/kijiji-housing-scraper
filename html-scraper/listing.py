#!/usr/bin/python3

from datetime import datetime


class Listing:
    def __init__(self):
        # unique id of a posting
        self.id = -1

        # unique id of a category
        self.category_id = -1

        # title of the category
        self.category = -1

        # title of the posting
        self.title = -1

        # price of the posting
        self.price = -1

        # the listing url
        self.url = -1

        # publish date
        # currently derived from the time the listing is scraped
        self.pubdate = -1

        # location
        # is a string describing the location
        self.location = -1

        # number of bedrooms
        self.bedrooms = -1

        # number of bathrooms
        self.bathrooms = -1

        # pet friendly flag
        # whether the place is pet friendly
        self.pet_friendlly = -1

        # size of the place, in square
        self.size = -1

        # urgent posting flag
        self.urgent = -1

        # furnished flag
        # whether the place is furnished
        self.furnished = -1

        # the description
        self.description = -1

    def __repr__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Listing) and self.id == other.id

    def __ne__(self, other):
        return isinstance(other, Listing) and self.id != other.id

    def set_id(self, id):
        if (type(id) != int):
            raise TypeError('The id must be an int.')
            return -1
        self.id = id

    def set_title(self, title):
        if (type(title) != str):
            raise TypeError('The title must be a str.')
            return -1
        self.title = title

    def set_price(self, price):
        if (type(price) != float):
            raise TypeError('The price must be a float.')
            return -1
        self.price = price

    def set_url(self, url):
        if (type(url) != str):
            raise TypeError('The url must be a str.')
            return -1
        self.url = url

    def set_pubdate(self, pubdate):
        if (type(pubdate) != datetime):
            raise TypeError('The url must be a datetime.')
            return -1
        self.pubdate = pubdate

    def set_location(self, loc):
        if (type(loc) != str):
            raise TypeError('Value for "Location" must be a str.')
            return -1
        else:
            self.location = loc

    def set_description(self, des):
        self.description = des

    def set_bedrooms(self, br):
        try:
            br + 1
        except TypeError:
            print('Number of bedroom must be a number.')
            return -1

        self.bedrooms = br

    def set_bathrooms(self, br):
        try:
            br + 1
        except TypeError:
            print('Number of bathrooms must be a number.')
            return -1

        self.bathrooms = br

    def set_furnished(self, val):
        if (type(val) != bool):
            raise TypeError('Value for "Furnished" must be a bool.')
            return
        else:
            self.furnished = val

    def set_petfriendly(self, val):
        if (type(val) != bool):
            raise TypeError('Value for "Furnished" must be an bool.')
            return
        else:
            self.pet_friendlly = val

    def size(self, size):
        self.size = size
