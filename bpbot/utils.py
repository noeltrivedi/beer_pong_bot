from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1
import gspread
import SocketServer
import json

import bpbot

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

class SpreadsheetConnector():
    def __init__(self, google_credentials_file):
        self.init_gspread(google_credentials_file)

        self.name_to_row_map = {}
        i = 1
        for name in self.stats_worksheet.col_values(1):
            if name is not 'Name':
                self.name_to_row_map[name] = i
            i += 1


    def init_gspread(self, google_credentials_file):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_file, scope)
        gc = gspread.authorize(credentials)
        sh = gc.open('Beer Pong Club Stats')
        self.stats_worksheet = sh.worksheet('Stats')

    def find_next_available_row(self, worksheet, offset=1):
        try:
            col_values = worksheet.col_values(1)
            for i in range(len(col_values)-offset):
                if col_values[i+offset] is '':
                    #empty cell
                    return i+offset+1
        except:
            self.init_gspread()
            return self.find_next_available_row(worksheet, offset)


    def find_next_available_col(self, worksheet):
        try:
            i = 1
            for val in worksheet.row_values(1):
                if val is '':
                    #empty cell
                    return i
                i += 1
        except:
            self.init_gspread()
            return self.find_next_available_col(worksheet)

    def update_cell(self, row, col, val):
        try:
            self.stats_worksheet.update_cell(row, col, val)
        except:
            #sometimes if we don't use gspread, our connection can timeout
            #this raises a value error on the update cell function, so we just reinitialize gspread and try again
            self.init_gspread()
            self.update_cell(row, col, val)

    def update_player_stats(self, player_name, player):
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

        self.update_cell(row, win_percent_col, win_percent)
        self.update_cell(row, mcp_col, bpbot.bot.get_most_common_partner(player_name))
        self.update_cell(row, cpg_col, cpg)
        self.update_cell(row, cups_col, player['cups'])
        self.update_cell(row, win_col, player['wins'])
        self.update_cell(row, games_col, player['games'])
        self.update_cell(row, wins_carried_col, wins_carried)
        self.update_cell(row, wins_was_carried_col, wins_was_carried)
        self.update_cell(row, trolls_col, player['trolls'])
        self.update_cell(row, beers_drank_col, player['beers_drank'])

    def update_game_participation(self, player_data):
        total_games = 0
        for name in player_data:
            total_games += player_data[name]['games']
        total_games /= 4

        if total_games is 0:
            return

        for name in player_data:
            self.update_cell(self.name_to_row_map[name], game_participation_col, round(float(player_data[name]['games'])/total_games, 5))

    def add_player(self, player_name):
        row = self.find_next_available_row(self.stats_worksheet, offset=4) #offset is 4 because that's where the names begin in the spreadsheet

        self.name_to_row_map[player_name] = row

        self.update_cell(row, name_col, player_name)
        self.update_cell(row, win_percent_col, 0)
        self.update_cell(row, mcp_col, 'N/A')
        self.update_cell(row, cpg_col, 0)
        self.update_cell(row, cups_col, 0)
        self.update_cell(row, win_col, 0)
        self.update_cell(row, games_col, 0)
        self.update_cell(row, wins_carried_col, 0)
        self.update_cell(row, wins_was_carried_col, 0)
        self.update_cell(row, trolls_col, 0)
        self.update_cell(row, beers_drank_col, 0)
        self.update_cell(row, game_participation_col, 0)

#route messages to the bot
class MessageRouter(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)

        bpbot.bot.receive_message(data['text'])
