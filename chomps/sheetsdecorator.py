import pygsheets
import sys
import logging

spreadsheet_name = 'Beer Pong Club Stats'
worksheet_name = 'Stats'

name_col = 1
win_percent_col = 2
mcp_col = 3
cpg_col = 4
cups_col = 5
win_col = 6
games_col = 7
wins_carried_col = 8
wins_was_carried_col = 9
trolls_col = 10
beers_drank_col = 11
game_participation_col = 12

class SheetsDecorator():
    def __init__(self, load_spreadsheet, credentials):
        self.credentials = credentials
        self._init_pygsheets()
        if load_spreadsheet:
            self._load_spreadsheet()
            self._init_name_map()

    def _load_spreadsheet(self):
        try:
            self.spreadsheet = self.gc.open(spreadsheet_name)
            self.stats_worksheet = self.spreadsheet.worksheet_by_title(worksheet_name)
        except (pygsheets.SpreadsheetNotFound, pygsheets.WorksheetNotFound):
            print('Spreadsheet was not properly intialized! Follow the instructions in README.md to initialize the spreadsheet')
            logger = logging.getLogger('chomps')
            logger.error('Spreadsheet was not initialized. Exiting...')
            sys.exit()

    def _init_name_map(self):
        self.name_to_row_map = {}
        for i, name in enumerate(self.stats_worksheet.get_col(1)):
            if name is not 'Name':
                self.name_to_row_map[name] = i+1

    def _init_pygsheets(self):
        self.gc = pygsheets.authorize(service_file=self.credentials)


    def get_sheet_url(self):
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet.id

    def find_next_available_row(self):
        min_row = 4

        col_values = self.stats_worksheet.get_col(1)
        next_available = len(col_values)+1
        next_available = next_available if next_available >=4 else min_row
        return next_available

    def update_player_stats(self, player_name, player):
        #This isn't great, but we can't import chomps at the full level since it attempts to import this file
        #TODO: Probably a sign of bad design, so this should be fixed later
        import chomps

        self.stats_worksheet
        row = self.name_to_row_map[player_name]

        win_percent = 0
        cpg = 0
        wins_carried = 0
        wins_was_carried = 0
        if player['games'] is not 0:
            win_percent = round(float(player['wins'])/player['games'], 4)
            cpg = round(float(player['cups'])/player['games'], 4)
        if player['wins'] is not 0:
            wins_carried = round(float(player['games_carried'])/player['wins'], 4)
            wins_was_carried = round(float(player['games_was_carried'])/player['wins'], 4)

        vals = [
            win_percent,
            chomps.bot.get_most_common_partner(player_name),
            cpg,
            player['cups'],
            player['wins'],
            player['games'],
            wins_carried,
            wins_was_carried,
            player['trolls'],
            player['beers_drank']
            ]
        self.stats_worksheet.update_row(row, vals, 1)

    def update_game_participation(self, player_data):
        total_games = 0
        for name in player_data:
            total_games += player_data[name]['games']
        total_games /= 4

        if total_games is 0:
            return

        game_participation_vals = [0 for i in range(len(player_data))]
        index_of_first_name = 4
        precision = 5
        for name in player_data:
            index = self.name_to_row_map[name] - index_of_first_name
            game_participation_vals[index] = round(float(player_data[name]['games'])/total_games, precision)

        self.stats_worksheet.update_col(game_participation_col, game_participation_vals, index_of_first_name-1)

    def add_player(self, player_name):
        row = self.find_next_available_row()

        self.name_to_row_map[player_name] = row

        vals = [player_name, 0, 'N/A', 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.stats_worksheet.update_row(row, vals)

    def init_spreadsheet(self, email=None):
        #This is a identifier for a public spreadsheet with all the formulas and formatting preloaded
        template_tuple = (u'1W9rPJcpZFNtAtiaMUZJzKbfDejTG9LLvO_pnRJcVwKg', 468279265)

        sheets = self.gc.list_ssheets()
        for sheet in sheets:
            if sheet['name'] == spreadsheet_name:
                print('Sheet already exists! Exiting...')
                sys.exit()

        self.spreadsheet = self.gc.create(title=spreadsheet_name)
        self.stats_worksheet = self.spreadsheet.add_worksheet(title=worksheet_name, src_tuple=template_tuple)
        self.spreadsheet.del_worksheet(self.spreadsheet.worksheet_by_title('Sheet1'))
        if email is not None:
            self.spreadsheet.share(email, role='writer')
