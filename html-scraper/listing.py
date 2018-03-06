class Listing():
    def __init__(self):
        self.id = -1
        self.title = -1
        self.price = -1
        self.url = -1
        self.pubdate = -1
        self.location = -1
        self.bedrooms = -1
        self.pet_friendlly = -1
        self.bathrooms = -1
        self.size = -1
        self.furnished = -1
        self.description = -1

    def set_id(self, id):
        self.id = id

    def set_title(self, title):
        self.title = title

    def set_price(self, price):
        self.price = price

    def set_url(self, url):
        self.url = url

    def set_pubdate(self, pubdate):
        self.pubdate = pubdate

    def set_location(self, loc):
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

    def set_furnished(self, val):
        if (type(val) != bool):
            raise TypeError('Value for "Furnished" must be a boolean')
            return
        else:
            self.furnished = val

    def set_petfriendly(self, val):
        if (type(val) != bool):
            raise TypeError('Value for "Furnished" must be a boolean')
            return
        else:
            self.pet_friendlly = val

    def size(self, size):
        self.size = size
