# Kijiji Housing Scraper

A Python 3 automated scraper that scrapes student housing listings on Kijiji (designed and tested only for "Room Rentals & Roommates", "Apartments & Condos for Rent", "House Rental" and "Short Term Rentals" categories) and stores the data on a MySQL server.

## Features

- Fetches the given Kijiji category links and iterate through every page and scrape all the found listings.
- Stores the scraped data on a provided MySQL server using a MySQL Connection Pool.
- Has a moderate rate of scraping. For now there is at least 1 second between requests to Kijiji server.
- Avoids scraping already scraped data by looking up the listing ID on the MySQL server before scraping to minimize the amount of request to Kijiji server.

## Setting Up

These instructions will help you get a functional copy of this project for your own deployment and testing purposes.

### Dependencies

Kijiji Housing Scraper relies on [requests](http://docs.python-requests.org/en/master/ "requests"), [lxml](http://lxml.de "lxml") and [mysqlclient](https://pypi.python.org/pypi/mysqlclient "mysqlclient"). You can install these dependencies using `pip` as follows:

```sh
$ pip install requests, lxml, mysqlclient
```

### Input File

Place all the Kijiji housing links you want the scrape into the input file [urls.in](/urls.in). Each line contains a link. Each link has to be a link of the first page (i.e. there is no page tag in the url). For example:

```
https://www.kijiji.ca/b-house-rental/kitchener-waterloo/c43l1700212
https://www.kijiji.ca/b-room-rental-roommate/kitchener-waterloo/c36l1700212
https://www.kijiji.ca/b-apartments-condos/kitchener-waterloo/c37l1700212
```

It is read once at the start, so you need to restart the scraper for any change to this file to take effect.

### MySQL Database Structure

Since the description of a Kijiji listing can contain `utf-8mb4` characters, we need to make sure our MySQL database also supports `utf-8mb4` by initializing a database with the following command:

```mysql
CREATE database <database_name> character set UTF8mb4 COLLATE utf8mb4_bin
```

The data will be stored in tables of the following structure:

```mysql
CREATE TABLE c43(
  id INT,
  title VARCHAR(128) NOT NULL,
  publish_date DATETIME NOT NULL,
  location_id INT NOT NULL,
  address VARCHAR(256) NOT NULL,
  bedroom_qty INT,
  bathroom_qty INT,
  price FLOAT,
  pet_friendly_flag INT,
  furnished_flag INT,
  urgent_flag INT,
  url VARCHAR(256) NOT NULL,
  size FLOAT,
  description TEXT,
  PRIMARY KEY (id)
);
```

`c43` is the table name for Kijiji category with ID 43. The category ID can be extracted from the url.
For example, [https://www.kijiji.ca/b-room-rental-roommate/kitchener-waterloo/c36l1700212](https://www.kijiji.ca/b-room-rental-roommate/kitchener-waterloo/c36l1700212) has ID 36 from the last part of the url: "c36l1700212".

## Usage

You can edit [scraper.py](/scraper.py) directly to run the bot. You just need to change the MySQL authentication information in

```python
if __name__ == '__main__':
    scraper = KijijiHousingBot(host_address, username, password, databasename)
    scraper.start()
```

Or, you can import `KijijiHousingBot` and use the syntax above to run the bot.

The input filename where Kijiji category links are read from is customizable, but is set to [urls.in](/urls.in) by default. You can change it by passing the new name as the value for the argument `inputfilename` of `KijijiHousingBot.start()` like so: `KijijiHousingBot.start(inputfilename=newfilename)`.

## Built With
- [PyCharm](https://www.jetbrains.com/pycharm/ "PyCharm")
- [requests](http://docs.python-requests.org/en/master/ "requests")
- [lxml](http://lxml.de "lxml")
- [mysqlclient](https://pypi.python.org/pypi/mysqlclient "mysqlclient")
