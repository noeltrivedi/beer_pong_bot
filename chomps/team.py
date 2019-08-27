from .stats import Stats
from .constants import BEERS_PER_CUP, MIN_CARRY_DIFFERENCE

class InvalidGameException(Exception):
    pass

class Team():
    # TODO(ntr) - probably create a representation of the stats of a team here?
    # otherwise, we can't get the stats of a team from the Team object itself, which sounds really dumb
    def __init__(self, playerOne, playerTwo):
        self._playerOne = playerOne
        self._playerTwo = playerTwo

    def AddGame(self, gameRecord):
        # Swap the stats if they were passed in in the wrong order
        playerOneRecord = gameRecord.GetPlayerRecord(self._playerOne.GetName())
        playerTwoRecord = gameRecord.GetPlayerRecord(self._playerTwo.GetName())

        if playerOneRecord is None:
            raise InvalidGameException('Player {} is not in this game record; Team="{}"; GameRecord="{}"'.format(self._playerOne.GetName(),
                                                                                                             str(self),
                                                                                                             str(gameRecord)))
        if playerTwoRecord is None:
            raise InvalidGameException('Player {} is not in this game record; Team="{}"; GameRecord="{}"'.format(self._playerTwo.GetName(),
                                                                                                             str(self),
                                                                                                             str(gameRecord)))

        self._playerOne.AddGame(playerOneRecord)
        self._playerTwo.AddGame(playerTwoRecord)

    def StatString(self):
        # TODO(ntr) probably extract this from the Team class?
        playerOneStats = self._playerOne.GetTeammateStats(self._playerTwo.GetName())
        playerTwoStats = self._playerTwo.GetTeammateStats(self._playerOne.GetName())

        # for these, it should be the same, so whether we grab it from p1 or p2 doesn't matter
        winCount = playerOneStats[Stats.TotalWins]
        gameCount = playerOneStats[Stats.GamesPlayed]
        winRate = (float(winCount)/float(gameCount) * 100)

        playerOneCupsMade = playerOneStats[Stats.CupsMade]
        playerOneCarryCount = playerOneStats[Stats.GamesCarried]
        playerOneCarryRate = playerOneCarryCount/float(winCount)*100 if winCount is not 0 else 0
        playerOneCPG = playerOneCupsMade/float(gameCount)

        playerTwoCupsMade = playerTwoStats[Stats.CupsMade]
        playerTwoCarryCount = playerTwoStats[Stats.GamesCarried]
        playerTwoCarryRate = playerTwoCarryCount/float(winCount)*100 if winCount is not 0 else 0
        playerTwoCPG = playerTwoCupsMade/float(gameCount)

        statString = ("{playerOne} and {playerTwo} Team Stats:\n"
                      "Total Games: {gamesPlayed}\n"
                      "Win %: {winRate:0.2f}%\n"
                      "{playerOne}'s CPG: {playerOneCPG:0.2f}\n"
                      "{playerTwo}'s CPG: {playerTwoCPG:0.2f}\n"
                      "{playerOne}'s Carry %: {playerOneCarryRate:0.2f}%\n"
                      "{playerTwo}'s Carry %: {playerTwoCarryRate:0.2f}%\n"
                      "Avg. Cups Left: {avgCupsLeft}"
        ).format(playerOne = self._playerOne.GetName(),
                 playerTwo = self._playerTwo.GetName(),
                 gamesPlayed = gameCount,
                 winRate = winRate,
                 playerOneCPG = playerOneCPG,
                 playerTwoCPG = playerTwoCPG,
                 playerOneCarryRate = playerOneCarryRate,
                 playerTwoCarryRate = playerTwoCarryRate,
                 avgCupsLeft = 0
        )
        return statString

    def __str__(self):
        return '{} and {}'.format(self._playerOne.GetName(), self._playerTwo.GetName())


class TeamCollection():
    def __init__(self, teams, playerCollection):
        self._teams = teams
        self._playerCollection = playerCollection

    def __getitem__(self, players):
        p1 = players[0]
        p2 = players[1]
        if (p1, p2) in self._teams:
            return self._teams[p1, p2]
        elif (p2, p1) in self._teams:
            return self._teams[p2, p1]

        # if both players are valid, construct a new team and return it
        playerOne = self._playerCollection.GetPlayer(p1)
        playerTwo = self._playerCollection.GetPlayer(p2)
        if playerOne is None or playerTwo is None:
            return None
        newTeam = Team(playerOne, playerTwo)
        self._teams[(p1, p2)] = newTeam
        return newTeam

if __name__ == '__main__':
    from .player import PlayerCollection
    from .records import GameRecord
    import string
    import random

    playerCollection = PlayerCollection()
    teamCollection = TeamCollection({}, playerCollection)
    players = []

    for char in string.ascii_lowercase:
        tmp = playerCollection.CreatePlayer(char)
        players.append(char)
    # a = playerCollection.CreatePlayer('a')
    # b = playerCollection.CreatePlayer('b')
    # c = playerCollection.CreatePlayer('c')
    # d = playerCollection.CreatePlayer('d')
    # e = playerCollection.CreatePlayer('e')

    # players = ['a', 'b', 'c', 'd']
    for i in range(100):
        w = [players[0], players[1]]
        l = [players[2], players[3]]

        tmpCupsMade = random.randint(0, 10)
        w = { players[0] : tmpCupsMade, players[1] : 10-tmpCupsMade}
        tmpCupsMade = random.randint(0, 10)
        l = { players[2] : tmpCupsMade, players[3] : 10-tmpCupsMade}
        r = GameRecord.Construct(w, l)
        teamCollection[players[0], players[1]].AddGame(r)
        teamCollection[players[2], players[3]].AddGame(r)

        random.shuffle(players)
