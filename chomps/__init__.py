import logging
import sys
import traceback

def _exception_handler(type, value, tb):
    logger = logging.getLogger('chomps')
    #TODO: figure out how to properly format the stack trace
    logger.error('Exception %s: %s\n\t%s', type.__name__, value, traceback.format_tb(tb))

def _init_logger():
        logger = logging.getLogger('chomps')
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler('data/log.txt', delay=False)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        sys.excepthook = _exception_handler

_init_logger()
