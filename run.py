#!/usr/bin/python

import sys
import os
import json

import chomps.chomps as chomps

if len(sys.argv) is 2: #config file is specified
    config_file = os.path.normpath(sys.argv[1])
else:
    config_file = os.path.join('.', 'data', 'config.json')

with open(config_file) as data_file:
    config = json.load(data_file)

chomps.initialize(
    bot_id=config['bot_id'],
    debug=config['debug'],
    use_spreadsheet=config['use_spreadsheet'],
    service_credentials=config['service_credentials']
    )

chomps.listen(port=config['listening_port']) #blocking call
