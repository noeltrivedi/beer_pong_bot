#!/usr/bin/python

import sys
import os
import json
from chomps.sheetsdecorator import SheetsDecorator

print('Preparing to initialize stats spreadsheet')
credentials_path = os.path.join('.', 'data', 'client_secret_debug.json')
if os.path.exists(credentials_path):
    print('Your email is used to share the spreadsheet with you and give you Writer privileges, which allow you to manually edit the spreadsheet, and share it with other people.\n'
        'If you\'d prefer not to use this, insert \"N/A\"'
        )

    email = raw_input('Email: ')
    if email == "N/A":
        email = None
    spread = SheetsDecorator(load_spreadsheet=False, credentials=credentials_path)
    spread.init_spreadsheet(email=email)
    print('Successfully created spreadsheet!')
else:
    print('Credentials file not found in path {}'.format(credentials_path))

