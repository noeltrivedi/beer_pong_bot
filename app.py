import json
import logging
import os
from flask import Flask, render_template
from chomps.chomps import initialize
from chomps.sheetsdecorator import SheetsDecorator

logger = logging.getLogger(__name__)

class WebChomps(object):
    def __init__(self):
        self.credentials_path = os.path.join('.', 'data', 'client_secret_debug.json')
        self.config_file = os.path.join('.', 'data', 'config.json')
        assert os.path.exists(self.credentials_path)
        assert os.path.exists(self.config_file)
        with open(self.config_file) as data_file:
            config = json.load(data_file)

        self.app = Flask(__name__)
        self.spreadsheet = self.init_spreadsheet(config['email_address'])
        self.chomps_instance = initialize(
            bot_id=config['bot_id'],
            debug=config['debug'],
            use_spreadsheet=config['use_spreadsheet'],
            service_credentials=config['service_credentials'])

        self.chomps_instance.listen(port=config['listening_port'])  # blocking call

    def init_spreadsheet(self, email_address):
        logger.info('Preparing to initialize stats spreadsheet')
        spread = None
        if os.path.exists(self.credentials_path):
            spread = SheetsDecorator(load_spreadsheet=False, credentials=self.credentials_path)
            spread.init_spreadsheet(email=email_address)
            logger.info('Successfully created spreadsheet!')
        else:
            logger.error('Credentials file not found in path {}'.format(self.credentials_path))
        return spread

web_chomps = WebChomps()

@web_chomps.app.route('/')
def hello_world():
    context = web_chomps.chomps_instance # GET STATS HERE AS DICT
    return render_template(template_name_or_list='spread.html', context=context)
