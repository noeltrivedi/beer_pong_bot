from .stats import Stats
from .constants import BEERS_PER_CUP, MIN_CARRY_DIFFERENCE

class GameRecord():
    def __init__(self):
        # shape is {Player Name : PlayerRecord}
        self._players = {}

    @staticmethod
    def Construct(winningTeamStats, losingTeamStats):
        # TODO(ntr) is it better to construct this from the game string?
        # the question really is - should this class know the string representation being passed in
        # or should some other translation class?

        # drink the cups the other team made
        winningTeamBeersPerPlayer = sum(losingTeamStats.values()) * BEERS_PER_CUP
        losingTeamBeersPerPlayer = sum(winningTeamStats.values()) * BEERS_PER_CUP

        winners = GameRecord.ConstructPlayerRecords(list(winningTeamStats.items()), winningTeamBeersPerPlayer, didWin=True)
        losers = GameRecord.ConstructPlayerRecords(list(losingTeamStats.items()), losingTeamBeersPerPlayer, didWin=False)

        record = GameRecord()
        for playerName, playerRecord in list(winners.items()):
            record.AddPlayerRecord(playerName, playerRecord)
        for playerName, playerRecord in list(losers.items()):
            record.AddPlayerRecord(playerName, playerRecord)
        return record

    @staticmethod
    def ConstructPlayerRecords(teamStats, beersDrank, didWin):
        playerOne = teamStats[0]
        playerTwo = teamStats[1]
        didPlayerOneCarry = playerOne[1] - playerTwo[1] >= MIN_CARRY_DIFFERENCE
        didPlayerTwoCarry = playerTwo[1] - playerOne[1] >= MIN_CARRY_DIFFERENCE

        playerOneGameRecord = PlayerGameRecord(cupsMade=playerOne[1],
                                               beersDrank=beersDrank,
                                               didWin=didWin,
                                               didCarry=didPlayerOneCarry,
                                               wasCarried=didPlayerTwoCarry,
                                               teammate=playerTwo[0])

        playerTwoGameRecord = PlayerGameRecord(cupsMade=playerTwo[1],
                                               beersDrank=beersDrank,
                                               didWin=didWin,
                                               didCarry=didPlayerTwoCarry,
                                               wasCarried=didPlayerOneCarry,
                                               teammate=playerOne[0])

        return { playerOne[0] : playerOneGameRecord,
                 playerTwo[0] : playerTwoGameRecord}

    def AddPlayerRecord(self, playerName, playerRecord):
        self._players[playerName] = playerRecord

    def GetPlayerRecord(self, playerName):
        if playerName not in self._players:
            return None
        return self._players[playerName]

    def OnSameTeam(self, playerOne, playerTwo):
        if playerOne not in self._players:
            return False
        return self._players[playerOne][Stats.Teammate] == playerTwo

    def __str__(self):
        # TODO(ntr) figure out a non-shitty way to do this
        winners = [(name, record) for name, record in list(self._players.items()) if record[Stats.DidWin] == True]
        losers = [(name, record) for name, record in list(self._players.items()) if record[Stats.DidWin] == False]

        recordString = ' '.join(['{} ({})'.format(name, record[Stats.CupsMade]) for (name, record) in winners])
        recordString += ' beat '
        recordString += ' '.join(['{} ({})'.format(name, record[Stats.CupsMade]) for (name, record) in losers])

        # should look like 'Alice (5) Bob (5) beat Charlie (3) David (2)'
        return recordString.strip()

class PlayerGameRecord():
    # The minimum amount of information to express what happened in one game for one player
    def __init__(self):
        self._stats = { Stats.CupsMade : 0,
                        Stats.BeersDrank : 0,
                        Stats.DidWin : False,
                        Stats.DidCarry : False,
                        Stats.WasCarried : False,
                        Stats.Teammate : 'NotSet'}

    def __init__(self, cupsMade, beersDrank, didWin, didCarry, wasCarried, teammate):
        self._stats = { Stats.CupsMade : int(cupsMade),
                        Stats.BeersDrank : float(beersDrank),
                        Stats.DidWin : didWin,
                        Stats.DidCarry : didCarry,
                        Stats.WasCarried : wasCarried,
                        Stats.Teammate : str(teammate)}

    def __getitem__(self, key):
        return self._stats[key]

    def __setitem__(self, key, value):
        self._stats[key] = value
        return self._stats[key]
