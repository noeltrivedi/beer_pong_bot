import logging

def _init_logger():
        logger = logging.getLogger('chomps')
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler('data/log.txt', delay=False)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

_init_logger()
