#!/usr/bin/python

import sys
import logging
import time
import chomps.chomps as chomps
import variables
from http.server import HTTPServer
from multiprocessing import Process
from chomps.messagerouter import MessageRouter


chomps.initialize(bot_id=variables.BOT_ID, debug=variables.DEBUG, use_spreadsheet=variables.USE_SPREADSHEET,
                  service_credentials=variables.SERVICE_CREDENTIALS)

print('Getting Logger...')
logger = logging.getLogger('chomps')

print('Starting...')
time.sleep(1)
try:
    print("It's showtime, baby.")
    # Blocking call in separate process
    chomps_proc = Process(target=chomps.listen, args=(HTTPServer, MessageRouter, variables.LISTENING_PORT))
    chomps_proc.start()
    while True:
        message = raw_input("chomps: ")
        confirm = raw_input("Type yes to confirm: ")
        if confirm.lower() == 'yes':
            print('Sending: "{}"'.format(message))
            time.sleep(1)
            chomps.bot.send_message(message)
except Exception as e:
    logger.error(str(e))
finally:
    chomps_proc.join()
