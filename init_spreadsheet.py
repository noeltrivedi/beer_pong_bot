#!/usr/bin/python
import logging
import os
from chomps.sheetsdecorator import SheetsDecorator
from chomps.constants import email_address


logger = logging.getLogger(__name__)


def init_spreadsheet():
    logger.info('Preparing to initialize stats spreadsheet')
    credentials_path = os.path.join('.', 'data', 'client_secret_debug.json')
    spread = None
    if os.path.exists(credentials_path):
        spread = SheetsDecorator(load_spreadsheet=False, credentials=credentials_path)
        spread.init_spreadsheet(email=email_address)
        logger.info('Successfully created spreadsheet!')
    else:
        logger.error('Credentials file not found in path {}'.format(credentials_path))
    return spread
