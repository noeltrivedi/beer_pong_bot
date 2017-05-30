import unittest
from bpbot import bpbot

class TestRegex(unittest.TestCase):
    def setUp(self):
        bpbot.initialize(debug=True, manual_push=True)

    def test_matches_game_results(self):
        msg = 'Alice (4) Bob LastName (8) beat Eve LastName (3) Steve (2)'
        self.assertIsNotNone(bpbot.bot.game_results_regex.match(msg))

    def test_matches_spreadsheet_request(self):
        msg = '!stats'
        self.assertIsNotNone(bpbot.bot.spreadsheet_request_regex.match(msg))

    def test_matches_player_stat_request(self):
        msg = '!stats Two Words'
        self.assertIsNotNone(bpbot.bot.player_stat_request_regex.match(msg))

    def test_matches_team_stat_request(self):
        msg = '!stats Two Words - Words Two'
        self.assertIsNotNone(bpbot.bot.team_stat_request_regex.match(msg))

    def test_matches_register(self):
        msg = '!register Name One'
        self.assertIsNotNone(bpbot.bot.register_regex.match(msg))

    def test_matches_new_nickname(self):
        msg = '!add nickname old name = new name'
        self.assertIsNotNone(bpbot.bot.new_nickname_regex.match(msg))

    def test_matches_update(self):
        msg = '!update'
        self.assertIsNotNone(bpbot.bot.update_regex.match(msg))

    def test_matches_list_nicknames(self):
        msg = '!nicknames nickname'
        self.assertIsNotNone(bpbot.bot.list_nicknames_request_regex.match(msg))

    def test_matches_help(self):
        msg = '!help'
        self.assertIsNotNone(bpbot.bot.help_regex.match(msg))

if __name__ == '__main__':
    unittest.main()
