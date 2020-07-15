import json
import threading
import logging
import os
import variables
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from chomps.chomps import initialize
from chomps.sheetsdecorator import SheetsDecorator


class WebChomps(object):
    def __init__(self):
        self.credentials_path = os.path.join('.', 'data', 'client_secret.json')
        assert os.path.exists(self.credentials_path)
        self.bot_id = variables.BOT_ID
        self.debug = variables.DEBUG
        self.web_port = variables.WEB_PORT
        self.use_spreadsheet = variables.USE_SPREADSHEET
        self.service_credentials = variables.SERVICE_CREDENTIALS
        self.email_address = variables.EMAIL_ADDRESS
        self.listening_port = variables.LISTENING_PORT
        self.app = Flask(__name__, static_folder='react/build')
        self.app.url_map.strict_slashes = False

        self.spreadsheet = self.init_spreadsheet()
        self.chomps_instance = initialize(bot_id=self.bot_id, debug=self.debug, use_spreadsheet=self.use_spreadsheet,
                                          service_credentials=self.service_credentials)
        threading.Thread(target=self.start_server)

    def start_server(self):
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


web_chomps = WebChomps()
cors = CORS(web_chomps.app, resources={r'/api/*': {'origins': variables.ACCEPTED_ORIGINS}}, supports_credentials=True)


@web_chomps.app.route('/', defaults={'path': ''}, methods=['GET'])
@web_chomps.app.route('/<path:path>', methods=['GET'])
def serve(path):
    # Serve React App
    if path != '' and os.path.exists(web_chomps.app.static_folder + path):
        message = 'Serving path: {}'.format(os.path.join(web_chomps.app.static_folder, path))
        web_chomps.app.logger.info(message)
        print(message)
        return send_from_directory(web_chomps.app.static_folder, path)
    else:
        message = 'Serving path: {}'.format(os.path.join(web_chomps.app.static_folder, 'index.html'))
        web_chomps.app.logger.info(message)
        print(message)
        return send_from_directory(web_chomps.app.static_folder, 'index.html')


@web_chomps.app.route('/api/context', methods=['GET', 'POST'])
def api_context():
    canonical_names = web_chomps.chomps_instance.canonical_names
    season_stats = web_chomps.chomps_instance.season_stats
    response = jsonify({'names': canonical_names, 'season': season_stats})
    response.status_code = 200
    return response


@web_chomps.app.route('/api/table', methods=['GET', 'POST'])
def api_table():
    context = web_chomps.chomps_instance.get_table_data()
    response = jsonify(context)
    response.status_code = 200
    return response


@web_chomps.app.route('/api/players', methods=['POST'])
def api_players():
    context = web_chomps.chomps_instance.nickname_map  # GET STATS HERE AS DICT
    response = jsonify({})
    response.status_code = 200
    return response


@web_chomps.app.route('/api/seasons', methods=['POST'])
def api_seasons():
    context = web_chomps.chomps_instance.nickname_map  # GET STATS HERE AS DICT
    response = jsonify({})
    response.status_code = 200
    return response


@web_chomps.app.route('/api/teams', methods=['GET', 'POST'])
def api_teams():
    request_json = request.get_json()
    player_one = request_json.get('player1')
    player_two = request_json.get('player2')
    team_stats = web_chomps.chomps_instance.get_team_stats(player_one, player_two)
    response = jsonify(team_stats)
    response.status_code = 200
    return response


if __name__ == '__main__':
    logging_format = '%(asctime)s %(name)s [%(filename)s:%(lineno)d][%(process)d] [%(levelname)s] %(message)s'
    debug = bool(web_chomps.debug)
    port = int(web_chomps.web_port)
    host = '0.0.0.0'
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format=logging_format)
    web_chomps.app.logger.info('Starting server on {host}:{port}. Debug: {debug}.'.format(host=host, port=port, debug=debug))
    web_chomps.app.run(host=host, port=port, debug=debug, threaded=True)
