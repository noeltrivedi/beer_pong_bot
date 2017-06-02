import bpbot
import pygsheets

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
    def __init__(self, google_credentials_file):
        self.init_pygsheets(google_credentials_file)

        self.name_to_row_map = {}
        for i, name in enumerate(self.stats_worksheet.get_col(1)):
            if name is not 'Name':
                self.name_to_row_map[name] = i+1

    def init_pygsheets(self, google_credentials_file):
        gc = pygsheets.authorize(service_file=google_credentials_file)
        self.spreadsheet = gc.open('Beer Pong Club Stats')
        self.stats_worksheet = self.spreadsheet.worksheet_by_title('Stats')

    def get_sheet_url(self):
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheet.id

    def find_next_available_row(self):
        col_values = self.stats_worksheet.get_col(1)
        return len(col_values)+1

    def update_player_stats(self, player_name, player):
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
            bpbot.bot.get_most_common_partner(player_name),
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
