from datetime import datetime

class Listing():
    def __init__(self):
        self.id = -1
        self.title = -1
        self.price = -1
        self.url = -1
        self.pubdate = -1
        self.location = -1
        self.bedrooms = -1
        self.bathrooms = -1
        self.pet_friendlly = -1
        self.bathrooms = -1
        self.size = -1
        self.furnished = -1
        self.description = -1

    def set_id(self, id):
        if (type(id) != str):
            raise TypeError('The id must be a str')
            return -1
        self.id = id

    def set_title(self, title):
        if (type(title) != str):
            raise TypeError('The title must be a str')
            return -1
        self.title = title

    def set_price(self, price):
        if (type(price) != str):
            raise TypeError('The price must be a str')
            return -1
        self.price = price

    def set_url(self, url):
        if (type(url) != str):
            raise TypeError('The url must be a str')
            return -1
        self.url = url

    def set_pubdate(self, pubdate):
        if (type(pubdate) != datetime):
            raise TypeError('The url must be a datetime')
            return -1
        self.pubdate = pubdate

    def set_location(self, loc):
        if (type(loc) != str):
            raise TypeError('Value for "Location" must be a str')
            return -1
        else:
            self.location = loc

    def set_description(self, des):
        self.description = des

    def set_bedrooms(self, br):
        try:
            br + 1
        except TypeError:
            print('Number of bedroom must be an integer')
            return

        self.bedrooms = br

    def set_bathrooms(self, br):
        try:
            br + 1
        except TypeError:
            print('Number of bathrooms must be an integer')
            return

        self.bathrooms = br

    def set_furnished(self, val):
        if (type(val) != int):
            raise TypeError('Value for "Furnished" must be an int')
            return
        else:
            self.furnished = val

    def set_petfriendly(self, val):
        if (type(val) != int):
            raise TypeError('Value for "Furnished" must be an int')
            return
        else:
            self.pet_friendlly = val

    def size(self, size):
        self.size = size
