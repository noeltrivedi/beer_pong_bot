from .stats import Stats, PlayerStats

class PlayerAlreadyExistsException(Exception):
    pass

class Player():
    def __init__(self, canonicalName, stats=None):
        self._canonicalName = canonicalName
        self._nicknames = [canonicalName]
        self._teammateGameCounts = {}
        if stats is not None:
            self._stats = stats
        else:
            self._stats = PlayerStats()

    def RegisterNickname(self, nickname):
        # NOTE: this should only be called from a PlayerCollection
        # otherwise, you could have colliding nicknames
        self._nicknames.append(nickname)

    def GetNicknames(self):
        return self._nicknames

    def GetName(self):
        return self._canonicalName

    def GetTeammateStats(self, teammate):
        return self._stats.GetTeammateStats(teammate)

    def AddGame(self, playerRecord):
        self._stats.AddGame(playerRecord)

    def StatString(self):
        statString = 'Player Name: {playerName}\n{stats}'.format(playerName=self._canonicalName, stats=str(self._stats))
        return statString

class PlayerCollection():
    def __init__(self):
        self._players = []

    def CreatePlayer(self, playerName):
        p = self.GetPlayer(playerName)
        if p is not None:
            raise PlayerAlreadyExistsException('Player Name {} is already taken by {}. Cannot register'.format(playerName, p.GetName()))
        player = Player(playerName)
        self._players.append(player)
        return player

    def RegisterNickname(self, playerName, newNickname):
        p = self.GetPlayer(newNickname)
        if p is not None:
            raise PlayerAlreadyExistsException('Player Name {} is already taken by {}. Cannot register nickname'.format(playerName, p.GetName()))
        p = self.GetPlayer(playerName)
        p.RegisterNickname(newNickname)

    def GetPlayer(self, nickname):
        # need to iterate over all players because we don't know if a player has gotten a nickname and it's not in our map
        for player in self._players:
            if nickname in player.GetNicknames():
                return player
        return None

# if __name__ == '__main__':
#     p = Player('Gnole')
#     p.AddGame(cupsMade=5, teammate='Dan', didWin=True, didCarry=False, wasCarried=False, beersDrank=1.2)
#     p.AddGame(cupsMade=2, teammate='Satish', didWin=True, didCarry=False, wasCarried=False, beersDrank=0.2)
#     p.AddGame(cupsMade=8, teammate='Dan', didWin=False, didCarry=False, wasCarried=False, beersDrank=0.3)
#     print(p.StatString())
