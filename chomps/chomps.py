from BaseHTTPServer import HTTPServer
import re
import os.path
import json
import urllib2
import httplib
import logging

from .sheetsdecorator import SheetsDecorator
from .messagerouter import MessageRouter

log_file_name = os.path.join('.', 'data', 'stat_log.txt')
player_data_file = os.path.join('.', 'data', 'player_data.json')

class Chomps():
    def __init__(self, bot_id, debug=False, use_spreadsheet=True, google_credentials_filename=None):
        self.logger = logging.getLogger('chomps')
        if debug:
            self._attach_debug_handler()
        self.bot_id = bot_id
        self.debug = debug

        #should log to the stat log - only disabled when running over old data
        self.should_log = True

        if use_spreadsheet:
            credentials_path = os.path.join('.', 'data', google_credentials_filename)
            self.spread = SheetsDecorator(load_spreadsheet=True, credentials=credentials_path)
        else:
            self.spread = None

        self._init_regexes()
        self._load_player_data()

        if not os.path.exists(log_file_name):
            fn = open(log_file_name, "w")
            fn.close()

        self.logger.info("Chomps initialized; bot_id=%s; debug=%s; use_spreadsheet=%s", bot_id, debug, use_spreadsheet)

    def _attach_debug_handler(self):
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)


    def _init_regexes(self):
        #regex building blocks
        regex_name = r'((?:\w+ ?){1,2}) ?'
        regex_cup_count = r'\((\d+)\) ?'

        self.game_results_regex = re.compile(
            r'^' + regex_name + regex_cup_count + regex_name + regex_cup_count +
            'beat ' +
            regex_name + regex_cup_count + regex_name + regex_cup_count)
        self.spreadsheet_request_regex = re.compile(r"^!stats *$")
        self.player_stat_request_regex = re.compile(r'^!stats ' + regex_name + '$')
        self.team_stat_request_regex = re.compile(r'^!stats ' + regex_name + '- ' + regex_name)
        self.register_regex = re.compile(r'^!register ' + regex_name)
        self.new_nickname_regex = re.compile(r'^!add nickname ' + regex_name + '= ' + regex_name)
        self.update_regex = re.compile(r'^!update *$')
        self.list_nicknames_request_regex = re.compile(r'^!nicknames ' + regex_name)
        self.help_regex = re.compile(r'^!help *')

        self._construct_regex_action_map()

    def _construct_regex_action_map(self):
        self.regex_action_map = [
            ('Game Results', self.game_results_regex, self.handle_game_results),
            ('Spreadsheet Request', self.spreadsheet_request_regex, self.handle_spreadsheet_request),
            ('Player Stats Request', self.player_stat_request_regex, self.handle_player_stat_request),
            ('Team Stats Request', self.team_stat_request_regex, self.handle_team_stat_request),
            ('New Nickname Request', self.new_nickname_regex, self.handle_new_nickname),
            ('List Nicknames Request', self.list_nicknames_request_regex, self.handle_list_nickname_request),
            ('Help Request', self.help_regex, self.handle_help_request),
            ('Update Command', self.update_regex, self.handle_update_command),
            ('Register Command', self.register_regex, self.handle_register),
            ]

    def _load_player_data(self):
        self.nickname_map = {}
        if os.path.exists(player_data_file):
            with open(player_data_file) as data_file:
                self.player_data = json.load(data_file)
                for name in self.player_data:
                    for nn in self.player_data[name]['nicknames']:
                        self.nickname_map[nn] = name
        else:
            #create the player data file as an empty dict
            #when players are registered, they'll get added normally
            self.player_data = {}
            self.persist_player_data()

    def receive_message(self, message):
        for tag, regex, action in self.regex_action_map:
            m = regex.match(message)
            if m:
                self.logger.info('Received message of type %s; msg=\"%s\"', tag, message)
                action(m)
                break

    def register_user(self, name):
        name = name.title()
        self.logger.info("Registering user %s", name)

        #first add them to the spreadsheet if needed
        if self.spread is not None:
            self.spread.add_player(name)

        #next construct a blank teammate data structure and add to all current players
        tm = {
            'wins' : 0,
            'player_cups': 0,
            'games': 0,
            'teammate_cups': 0,
            'games_was_carried': 0,
            'cups_left': 0,
            'games_carried': 0
            }

        #add this new player to every current player's teammate_Stats
        for player in self.player_data:
            self.player_data[player]['teammate_stats'][name] = tm

        #construct the actual player ds
        new_player = {
            'games': 0,
            'games_was_carried': 0,
            'trolls': 0,
            'cups': 0,
            'beers_drank': 0,
            'games_carried': 0,
            'nicknames': [
              name.lower()
              ],
            'wins': 0,
            'teammate_stats' : {}
        }

        #add every existing player to this new player's teammate_stats
        self.player_data[name] = new_player
        for player in self.player_data:
            if player is not name:
                self.player_data[name]['teammate_stats'][player] = tm.copy()

        #write json to file
        self.persist_player_data()

        #players only begin with one nickname, which is name.lower()
        #add this to the nickname map
        self.nickname_map[name.lower()] = name

    def handle_spreadsheet_request(self, m):
        if self.spread is not None:
            url = self.spread.get_sheet_url()
            self.send_message(url)
        else:
            self.send_message('The Stats Spreadsheet is currently disabled. You may still request individual stats using "!stats <name>"')

    def handle_list_nickname_request(self, m):
        player_name = self.convert_nickname_to_name(m.group(1))
        if player_name in self.player_data:
            nicknames = 'Valid Names for {}:\n'.format(player_name)
            for nn in self.player_data[player_name]['nicknames']:
                nicknames += nn
                nicknames += '\n'

            self.send_message(nicknames)

        else:
            self.send_message('Cannot find any player with name {}'.format(player_name))

    def handle_help_request(self, m):
        help_message = 'Chomps Commands\n'
        help_message += '<name1> (cup_count) <name2> (cup_count) beat <name3> (cup_count) <name4> (cup_count) : Inputs stats for a given game\n\n'
        help_message += '!stats : Requests a link to the stats spreadsheets\n\n'
        help_message += '!stats <name> : Requests a stat printout of the specified player\n\n'
        help_message += '!stats <name1> - <name2> : Requests a stat printout of the specified team\n\n'
        help_message += '!nicknames <name> : Outputs all nicknames for the specified player\n\n'
        help_message += '!add nickname <name> = <new name> : Adds the specified nickname to the specified player if possible\n\n'
        help_message += '!register <name> : Registers the player. Only use this after their Trial By Beer\n\n'
        help_message += '!update : Forces the bot to reload all data. Do not use this if you don\' know what you\'re doing\n\n'
        self.send_message(help_message)

    def handle_update_command(self, m):
        self.send_message('Reloading data. This may take a few minutes...')
        reload_data()
        self.send_message('Finished reloading data and updating the spreadsheet')

    def handle_new_nickname(self, m):
        canonical_name = self.convert_nickname_to_name(m.group(1))
        nickname = m.group(2).strip().lower()

        if canonical_name not in self.player_data:
            self.send_message('Name {} was not found!'.format(canonical_name))
            return
        elif nickname in self.nickname_map:
            self.send_message('Player {} already has {} as a nickname!'.format(self.nickname_map[nickname], nickname))
        else:
            self.add_new_nickname(canonical_name, nickname)

    def handle_register(self, m):
        player_name = self.convert_nickname_to_name(m.group(1))
        if player_name not in self.player_data:
            self.send_message('Registering user {}. This will take a few minutes...'.format(player_name))
            self.register_user(player_name)
            self.send_message('Successfully registered player {}'.format(player_name))
        else:
            self.send_message('Player {} is already registered'.format(player_name))

    def handle_team_stat_request(self, m):
        player_one = self.convert_nickname_to_name(m.group(1))
        player_two = self.convert_nickname_to_name(m.group(2))

        stats = self.player_data[player_one]['teammate_stats'][player_two]
        if stats['games'] is 0:
            self.send_message('{} and {} have never played together!'.format(player_one, player_two))
            return

        stat_string = '{} & {} Team Stats:\nTotal Games: {}\nWin %: {}%\n{}\'s CPG: {}\n{}\'s CPG: {}\n{}\'s Carry %: {}%\n{}\'s Carry %: {}%\nAvg. Cups Left: {}'.format(
            player_one,
            player_two,
            stats['games'],
            round(float(stats['wins'])/stats['games']*100, 2),
            player_one,
            round(float(stats['player_cups'])/stats['games'], 2),
            player_two,
            round(float(stats['teammate_cups'])/stats['games'], 2),
            player_one,
            round(float(stats['games_carried'])/stats['wins']*100, 2) if stats['wins'] is not 0 else 0,
            player_two,
            round(float(stats['games_was_carried'])/stats['wins']*100, 2) if stats['wins'] is not 0 else 0,
            round(float(stats['cups_left'])/stats['wins'], 2) if stats['wins'] is not 0 else 0
            )
        self.send_message(stat_string)

    def handle_player_stat_request(self, m):
        player_name = self.convert_nickname_to_name(m.group(1))

        if player_name not in self.player_data:
            self.send_message("Unable to return stats. Player name \"{}\" not found in the nickname database".format(m.group(1)))
            return

        gameCount = self.player_data[player_name]['games']
        cupCount = self.player_data[player_name]['cups']
        winCount = self.player_data[player_name]['wins']
        was_carried_rate = self.player_data[player_name]['games_was_carried']/self.player_data[player_name]['wins']*100 if self.player_data[player_name]['wins'] is not 0 else 0
        carry_rate = self.player_data[player_name]['games_carried']/self.player_data[player_name]['wins']*100 if self.player_data[player_name]['wins'] is not 0 else 0
        trollCount = self.player_data[player_name]['trolls']
        beerCount = self.player_data[player_name]['beers_drank']
        commonPartner = self.get_most_common_partner(player_name)


        if(gameCount == 0):
            self.send_message("Player {} has not played any games yet\n".format(player_name))
            return

        stat_string = ("Player Name: {}\n"
        "Total Cups: {}\n"
        "Win %: {:0.2f}%\n"
        "Most Common Partner: {}\n"
        "% Wins Carried: {:0.2f}%\n"
        "% Wins Was Carried: {:0.2f}%\n"
        "Cups/Game: {:0.2f}\n"
        "Times Trolled: {}\n"
        "Total Beers Drank: {:0.2f}\n"
        "Total Win Count: {}\n"
        "Total Game Count: {}\n"
        ).format(player_name,
            cupCount,
            (float(winCount)/float(gameCount) * 100),
            commonPartner,
            carry_rate,
            was_carried_rate,
            float(cupCount)/float(gameCount),
            trollCount,
            beerCount,
            winCount,
            gameCount
            )
        self.send_message(stat_string)

    def handle_game_results(self, m):
        all_players_found = self.load_player_stats(m)
        if all_players_found:
            self.failure = False
            self.success_message = 'Successfully logged stats for '
            self.failure_message = 'Unsuccessfully logged stats for '

            ps = self.player_stats
            self.update_player_stats(ps[0], ps[1], 10 - (ps[2][1] + ps[3][1]), True)
            self.update_player_stats(ps[1], ps[0], 10 - (ps[2][1] + ps[3][1]), True)
            self.update_player_stats(ps[2], ps[3], 10 - (ps[0][1] + ps[1][1]), False)
            self.update_player_stats(ps[3], ps[2], 10 - (ps[0][1] + ps[1][1]), False)
            self.update_beer_count()

            if self.should_log:
                self.log_stats(m.group(0))
                self.update_spreadsheet()

            self.persist_player_data()

            if self.failure:
                self.send_message(self.failure_message)
            else:
                self.send_message(self.success_message)

    def add_new_nickname(self, canonical_name, nickname):
        self.player_data[canonical_name]['nicknames'].append(nickname)
        self.nickname_map[nickname] = canonical_name
        self.persist_player_data()
        self.send_message('Successfully registered {} with the nickname {}'.format(canonical_name, nickname))

    def get_most_common_partner(self, player):
        if player not in self.player_data:
            return 'N/A'

        ts = self.player_data[player]['teammate_stats']
        gameCount = 0
        mostCommonPartner = 'N/A'
        for teammate in ts:
            if ts[teammate]['games'] > gameCount:
                gameCount = ts[teammate]['games']
                mostCommonPartner = teammate

        return mostCommonPartner

    def load_player_stats(self, m):
        self.player_stats = []
        for i in range(4):
            self.player_stats.append((self.convert_nickname_to_name(m.group(i*2+1)), int(m.group(i*2+2))))

        all_players_found = True
        for player in self.player_stats:
            if player[0].strip().lower() not in self.nickname_map:
                all_players_found = False
                self.logger.warning('Unable to log stats. Player name \"%s\" not found in nickname database', player[0])
                self.send_message("Unable to log stats. Player name \"{}\" not found in nickname database".format(player[0]))
                break
        return all_players_found

    def update_beer_count(self):
        losing_team_cups = int(self.player_stats[2][1]) + int(self.player_stats[3][1])

        for i in range(4):
            beers_drank= 0
            if i < 2:
                beers_drank = float(losing_team_cups)/10
            else:
                beers_drank = (1 + (float((10 - losing_team_cups))/10))

            self.player_data[self.player_stats[i][0]]['beers_drank'] += beers_drank

    def send_message(self, message):
        self.logger.info("Sending message; msg=\"%s\"", message)
        if not self.debug:
            data = {"bot_id": self.bot_id, "text": str(message)}
            req = urllib2.Request('https://api.groupme.com/v3/bots/post')
            req.add_header('Content-Type', 'application/json')

            response = urllib2.urlopen(req, json.dumps(data))
            response.close()

    def update_player_stats(self, player, teammate, cups_left, won):
        if won:
            self.player_data[player[0]]['wins'] += 1
        self.player_data[player[0]]['games'] += 1
        self.player_data[player[0]]['cups'] += int(player[1])
        if player[1] is 0:
            self.player_data[player[0]]['trolls'] += 1
            self.send_message('HAHA {} IS A TROLL'.format(player[0].upper()))

        #use tmp here because the full thing is too long to consistently type
        #the = operator is a shallow copy so this is fine anyway (probably)
        tmp = self.player_data[player[0]]['teammate_stats'][teammate[0]]
        tmp['cups_left'] += cups_left
        if won:
            tmp['wins'] += 1
            if (player[1] - teammate[1]) >= 4:
                tmp['games_carried'] += 1
                self.player_data[player[0]]['games_carried'] += 1
            elif (teammate[1] - player[1]) >= 4:
                tmp['games_was_carried'] += 1
                self.player_data[player[0]]['games_was_carried'] += 1
        tmp['games'] += 1
        tmp['player_cups'] += player[1]
        tmp['teammate_cups'] += teammate[1]

        self.success_message += player[0]
        self.success_message += ' '

    def log_stats(self, message):
        with open(log_file_name, "a") as log_file:
            log_file.write(message)
            log_file.write('\n')

    def persist_player_data(self):
        if not self.debug:
            with open(player_data_file, 'w') as out:
                json.dump(self.player_data, out, indent=2)

    def clear_game_record(self):
        for name in self.player_data:
            self.player_data[name]['beers_drank'] = 0
            self.player_data[name]['cups'] = 0
            self.player_data[name]['wins'] = 0
            self.player_data[name]['games'] = 0
            self.player_data[name]['games_was_carried'] = 0
            self.player_data[name]['trolls'] = 0
            self.player_data[name]['games_carried'] = 0
            for teammate in self.player_data[name]['teammate_stats']:
                ts = self.player_data[name]['teammate_stats'][teammate]
                ts['wins'] = 0
                ts['player_cups'] = 0
                ts['games'] = 0
                ts['teammate_cups'] = 0
                ts['games_was_carried'] = 0
                ts['games_carried'] = 0
                ts['cups_left'] = 0

        self.persist_player_data()

    def convert_nickname_to_name(self, nickname):
        if nickname.strip().lower() in self.nickname_map:
            return self.nickname_map[nickname.strip().lower()]
        else:
            return nickname.strip()

    def update_spreadsheet(self):
        if self.spread is not None:
            for player in self.player_stats:
                self.spread.update_player_stats(player[0], self.player_data[player[0]])
            self.spread.update_game_participation(self.player_data)

    def full_update_spreadsheet(self):
        if self.spread is not None:
            for player in self.player_data:
                self.spread.update_player_stats(player, self.player_data[player])
            self.spread.update_game_participation(self.player_data)

def initialize(bot_id=0, debug=False, use_spreadsheet=True, service_credentials=None):
    global bot
    bot = Chomps(
        bot_id=bot_id,
        debug=debug,
        use_spreadsheet=use_spreadsheet,
        google_credentials_filename=service_credentials
        )
    return bot

def listen(server_class=HTTPServer, handler_class=MessageRouter, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.getLogger('chomps').info('Listening for messages on port %d...', port)
    httpd.serve_forever()

def reload_data():
    bot.should_log = False

    debug = bot.debug
    bot.debug = True #don't want to send messages here

    bot.clear_game_record()
    #load in stats and pass into bot
    with open(log_file_name) as stats:
        for line in stats:
            bot.receive_message(line)
        bot.full_update_spreadsheet()

    bot.should_log = True
    bot.debug = debug
