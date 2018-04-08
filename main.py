import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(filename)s: '
                                                                   '%(levelname)s: '
                                                                   '%(funcName)s(): '
                                                                   '%(lineno)d:\t'
                                                                   '%(message)s')
