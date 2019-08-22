import json
import os
from flask import Flask, send_from_directory, jsonify
from chomps.chomps import initialize
from chomps.sheetsdecorator import SheetsDecorator


class WebChomps(object):
    def __init__(self):
        self.credentials_path = os.path.join('.', 'data', 'client_secret_debug.json')
        self.config_file = os.path.join('.', 'data', 'config.json')
        assert os.path.exists(self.credentials_path)
        assert os.path.exists(self.config_file)
        with open(self.config_file) as data_file:
            config = json.load(data_file)
        self.bot_id = config['bot_id']
        self.debug = config['debug']
        self.use_spreadsheet = config['use_spreadsheet']
        self.service_credentials = config['service_credentials']
        self.email_address = config['email_address']
        self.listening_port = config['listening_port']
        self.app = Flask(__name__, static_folder='react/build')
        self.spreadsheet = self.init_spreadsheet()
        self.chomps_instance = initialize(bot_id=self.bot_id, debug=self.debug, use_spreadsheet=self.use_spreadsheet,
                                          service_credentials=self.service_credentials)
        self.chomps_instance.listen(port=self.listening_port)  # Blocking call

    def init_spreadsheet(self):
        self.app.logger.info('Preparing to initialize stats spreadsheet')
        spread = None
        if os.path.exists(self.credentials_path):
            spread = SheetsDecorator(load_spreadsheet=False, credentials=self.credentials_path)
            spread.init_spreadsheet(email=self.email_address)
            self.app.logger.info('Successfully created spreadsheet!')
        else:
            self.app.logger.error('Credentials file not found in path {}'.format(self.credentials_path))
        return spread

    def main(self):
        host = '0.0.0.0'
        port = 5000
        self.app.logger.info('Starting on {host}:{port}.'.format(host=host, port=port))
        self.app.run(host=host, port=port, debug=self.debug, use_reloader=True, threaded=True)

web_chomps = WebChomps()


@web_chomps.app.route('/', defaults={'path': ''})
@web_chomps.app.route('/<path:path>')
def serve(path):
    # Serve React App
    if path != "" and os.path.exists(web_chomps.app.static_folder + path):
        return send_from_directory(web_chomps.app.static_folder, path)
    else:
        return send_from_directory(web_chomps.app.static_folder, 'index.html')


@web_chomps.app.route('/api/table', methods=['GET', 'POST'])
def api_table():
    response = jsonify({})
    response.status_code = 200
    return response


@web_chomps.app.route('/api/players', methods=['POST'])
def api_players():
    response = jsonify({})
    response.status_code = 200
    return response


@web_chomps.app.route('/api/seasons', methods=['POST'])
def api_seasons():
    response = jsonify({})
    response.status_code = 200
    return response


@web_chomps.app.route('/api/teams', methods=['POST'])
def api_teams():
    response = jsonify({})
    response.status_code = 200
    return response


if __name__ == '__main__':
    web_chomps.main()
