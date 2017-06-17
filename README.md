# Chomps

Chomps is a GroupMe bot written in Python which can log and track beer pong stats for multiple players, and create/update a Google sheet containing stats for all players. It was designed to be simple enough for someone several games deep to use it, while still providing enough functionality to make it a useful tool.

## Features
* Log game results
* Support multiple nicknames for players up to two words
* Provide a stat printout directly to GroupMe upon request
* Update a Google Sheet with relevant stats, such as win percent, average cups made per game, and most common partner
* Register new players directly from GroupMe
* Maintain a list of all logged games, which can be updated in case of misreported stats

## Getting Started

1. Run the command `pip install -r requirements.txt` to install required dependencies
2. [Create a GroupMe bot.](https://dev.groupme.com/bots/new) Set the callback url to the IP on which you plan to run the bot, with an arbitrary port.
3. If you're planning on using the spreadsheet functionality, you'll need signed credentials from Google. (Note: [A sample spreadsheet is located here](assets/spreadsheet_sample.PNG)). I recommend following [the instructions for 'Signed Credentials' from pygsheets](http://pygsheets.readthedocs.io/en/latest/authorizing.html). Then rename your credentials to `client_secret.json` and place it in the `data/` folder. Next, run `make setup` and follow the prompts. I highly recommend adding an email address. After setting this up, add any formatting you'd like to the Stats sheet. A link to the spreadsheet should have been sent to your email.
4. Setup the config file and save it as `data/config.json`. There's an example in the data folder.
5. Run `make startup-daemon`to create a background process running the bot.
6. Finally, register some players using `!register <name>` and start playing!


## Basic Usage
Note: Whenever a name is required, any valid nickname will work.
### Logging the results of a game
#### Format

`<player1> (cups made) <player2> (cups made) beat <player3> (cups made) <player4> (cups made)`

#### Example

`Alice (6) Bob (4) beat Eve (3) Chuck (4)`

### Requesting Stats for a Player
In addition to the Stats spreadsheet, Chomps can compile and format stats to be sent to the GroupMe.
#### Format


`!stats <player>`

#### Example:

Input: `!stats Alice`

Output:
```
Player Name: Alice
Total Cups: 78
Win %: 28.57%
Most Common Partner: Bob
% Wins Carried: 12.50%
% Wins Was Carried: 0.00%
Cups/Game: 4.71
Times Trolled: 0
Total Beers Drank: 24.10
Total Win Count: 6
Total Game Count: 21
```

### Nicknames
Nicknames allow for users to refer to a single player by multiple names. Nicknames are case insensitive, and unique across a playerbase. You can view a player's nicknames with the `!nicknames <player>` command.
#### Adding a Nickname
`!add nickname <player> = <new nickname>`

#### Example
`!add nickname Eve = Erin`

### Other
The functions listed above are only a few of the features of Chomps. Sending  the `!help` command will output a printout of all available commands and their format.


## License
This project is licensed under the [MIT License](LICENSE.md)

## Acknowledgements
A special thanks to all of the following:

* [pygsheets](https://github.com/nithinmurali/pygsheets)
* GroupMe
* University of Southern California's Beer Pong Club

## Todo:
In order of priority:

* Write a script to set up a GroupMe bot
* Write more unit tests
* Convert player stat into named tuple
* Implement functionality to archive stats, and reset all data (new seasons)
