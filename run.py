#!/usr/bin/python

import sys
import os
import json
import logging
import time
import chomps.chomps as chomps
from BaseHTTPServer import HTTPServer
from multiprocessing import Process
from chomps.messagerouter import MessageRouter

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

print('Getting Logger...')
logger = logging.getLogger('chomps')

print('Starting...')
time.sleep(1)
try:
    print("It's showtime, baby.")
    chomps_proc = Process(target=chomps.listen, args=(HTTPServer, MessageRouter, config['listening_port'],)) # blocking call in separate process
    chomps_proc.start()
    while True:
        message = input("chomps: ")
        confirm = input("Type yes to confirm: ")
        if confirm.lower() == 'yes':
            print('Sending: "{}"'.format(message))
            time.sleep(1)
            chomps.bot.send_message(message)
except Exception as e:
    logger.error(str(e))
finally:
    chomps_proc.join()
