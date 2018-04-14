import logging
import sys
import threading

from database.mysql import MySQLConnectionPool
from htmlscraper.html_scraper import KijijiScraper

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(filename)s: '
                                                                   '%(levelname)s: '
                                                                   '%(funcName)s(): '
                                                                   '%(lineno)d:\t'
                                                                   '%(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('Started')
    scraper = KijijiScraper()
    pool = MySQLConnectionPool('localhost', 'root', 'xxx', 'testdb1', 2)
    with open('urls.in', 'r') as f:
        for line in f:
            scraper.scrape_cat_page_ini(line)
            out = scraper.get_cat_page_listings()
            thread = threading.Thread(target=pool.update_table, args=(out,))
            thread.start()

            while True:
                out = scraper.scrape_next_page()
                if out == -1:
                    break
                thread = threading.Thread(target=pool.update_table, args=(out,))
                thread.start()

    logger.info('Terminated')
