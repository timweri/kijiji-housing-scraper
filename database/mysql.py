#!/usr/bin/python3

import logging
from queue import Queue

import MySQLdb


class MySQLConnectionPool:
    _fields_dict = {'id': 'ID', 'title': 'TITLE', 'cat_id': 'CATEGORY_ID', 'category': 'CATEGORY',
                    'pub_date': 'PUBLISH_DATE', 'locid': 'LOCATION_ID', 'addr': 'ADDRESS',
                    'bedrooms': 'BEDROOM_QUANTITY', 'bathrooms': 'BATHROOM_QUANTITY', 'price': 'PRICE',
                    'pet_friendly': 'PET_FRIENDLY_FLAG', 'furnished': 'FURNISHED_FLAG', 'urgent': 'URGENT_FLAG',
                    'url': 'URL', 'size': 'SIZE', 'des': 'DESCRIPTION'}

    def __init__(self, hostaddr, usr, pwd, dbname, size):
        logging.info('Initializing an instance of MySQLConnectionPool')
        logging.debug('Type checking for host addresses, username, password, database name and pool size')
        if type(hostaddr) != str:
            raise TypeError('hostaddr has to be a str')
        if type(usr) != str:
            raise TypeError('usr has to be a str')
        if type(pwd) != str:
            raise TypeError('pwd has to be a str')
        if type(dbname) != str:
            raise TypeError('dbname has to be a str')
        logging.debug('All type checks passed')

        logging.info('Initializing class variables')

        # set the host address
        self._hostaddr = hostaddr

        # set the username
        self._usr = usr

        # set the password
        self._pwd = pwd

        # set the database name
        self._dbname = dbname

        logging.info('Initializing MySQL connection pool')
        # initiate an empty Queue of required size
        self._pool = Queue(size)

        # fill the pool up
        for i in range(size):
            self._pool.put(MySQLdb.connect(hostaddr, usr, pwd, dbname), block=False)
        logging.info('Initialized MySQL connection pool')

    # return an available connection from the pool
    def get_connection(self):
        db = self._pool.get()

        logging.debug('Type checking connection')
        if not isinstance(db, MySQLdb.connections.Connection):
            raise TypeError('A connection has to be of type MySQLdb.connections.Connection')

        logging.info('Successful MySQL connection get request')
        return db

    # queue a connection to the pool
    def put_connection(self, connection):
        logging.debug('Type checking connection')
        if not isinstance(connection, MySQLdb.connections.Connection):
            raise TypeError('A connection has to be of type MySQLdb.connections.Connection')

        self._pool.put_nowait(connection)
        self._pool.task_done()
        logging.info('Successful MySQL connection put request')
        return 0

    # close all connections
    def clear_pool(self):
        logging.info('Closing the MySQL connection pool (id {})'.format(id(self)))
        while not self._pool.empty():
            db = self._pool.get()
            if not isinstance(db, MySQLdb.connections.Connection):
                raise TypeError('A non-Connection object found in the connection pool')
            db.close()
            self._pool.task_done()
        logging.info('Closed all connections in the MySQL connection pool (id {})'.format(id(self)))
        return 0

    # generate sql from a listing
    def gen_sql(self, listing):
        sql = ""

        id = listing.id

    # add a list of listings into an existing table
    def update_table(self, listings, table):
        logging.info('Updating table {} in the MySQL database'.format(table))
        logging.info('Requesting for MySQL connection')

        db = self.get_connection()
        cursor = db.cursor()

        for l in listings:
            if not isinstance(l, MySQLdb.connections.Connection):
                raise TypeError('Expected a Listing instance')
            sql = "INSERT INTO {}"


test = MySQLConnectionPool('localhost', 'root', 'rakion', 'TESTDB1', 3)
