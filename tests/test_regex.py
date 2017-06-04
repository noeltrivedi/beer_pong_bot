import unittest
from mock import MagicMock
from bpbot import bpbot

class TestRegexAndMessageRouting(unittest.TestCase):
    def setUp(self):
        bpbot.initialize(debug=True, manual_push=True, use_spreadsheet=False)

    def test_matches_game_results(self):
        msg = 'Alice (4) Bob LastName (8) beat Eve LastName (3) Steve (2)'
        self.assertIsNotNone(bpbot.bot.game_results_regex.match(msg))

    def test_properly_routes_game_results(self):
        msg = 'Alice (4) Bob LastName (8) beat Eve LastName (3) Steve (2)'
        bpbot.bot.handle_game_results = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_game_results.assert_called_once()

    def test_matches_spreadsheet_request(self):
        msg = '!stats'
        self.assertIsNotNone(bpbot.bot.spreadsheet_request_regex.match(msg))

    def test_properly_routes_spreadsheet_request(self):
        msg = '!stats'
        bpbot.bot.handle_spreadsheet_request = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_spreadsheet_request.assert_called_once()

    def test_matches_player_stat_request(self):
        msg = '!stats Two Words'
        self.assertIsNotNone(bpbot.bot.player_stat_request_regex.match(msg))

    def test_properly_routes_player_stat_request(self):
        msg = '!stats Two Words'
        bpbot.bot.handle_player_stat_request = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_player_stat_request.assert_called_once()

    def test_matches_team_stat_request(self):
        msg = '!stats Two Words - Words Two'
        self.assertIsNotNone(bpbot.bot.team_stat_request_regex.match(msg))

    def test_properly_routes_team_stat_request(self):
        msg = '!stats Two Words - Words Two'
        bpbot.bot.handle_team_stat_request = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_team_stat_request.assert_called_once()

    def test_matches_register(self):
        msg = '!register Name One'
        self.assertIsNotNone(bpbot.bot.register_regex.match(msg))

    def test_properly_routes_register(self):
        msg = '!register Name One'
        bpbot.bot.handle_register = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_register.assert_called_once()

    def test_matches_new_nickname(self):
        msg = '!add nickname old name = new name'
        self.assertIsNotNone(bpbot.bot.new_nickname_regex.match(msg))

    def test_properly_routes_new_nickname(self):
        msg = '!add nickname old name = new name'
        bpbot.bot.handle_new_nickname = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_new_nickname.assert_called_once()

    def test_matches_update_command(self):
        msg = '!update'
        self.assertIsNotNone(bpbot.bot.update_regex.match(msg))

    def test_properly_routes_update_command(self):
        msg = '!update'
        bpbot.bot.handle_update_command = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_update_command.assert_called_once()

    def test_matches_list_nicknames(self):
        msg = '!nicknames nickname'
        self.assertIsNotNone(bpbot.bot.list_nicknames_request_regex.match(msg))

    def test_properly_routes_list_nicknames(self):
        msg = '!nicknames nickname'
        bpbot.bot.handle_list_nickname_request = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_list_nickname_request.assert_called_once()

    def test_matches_help(self):
        msg = '!help'
        self.assertIsNotNone(bpbot.bot.help_regex.match(msg))

    def test_properly_routes_help(self):
        msg = '!help'
        bpbot.bot.handle_help_request = MagicMock()
        #reconstruct the action map since the tuple is immutable
        bpbot.bot._construct_regex_action_map()
        bpbot.bot.receive_message(msg)
        bpbot.bot.handle_help_request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
