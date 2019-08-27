from enum import Enum
from .constants import BEERS_PER_CUP, MIN_CARRY_DIFFERENCE

class Stats(Enum):
    GamesPlayed = 0
    TotalWins = 1
    CupsMade = 2
    GamesCarried = 3
    GamesWasCarried = 4
    Trolls = 5
    BeersDrank = 6
    TeammateStats = 7

    # Game Record Stats
    WasCarried = 8
    DidCarry = 9
    DidWin = 10
    Teammate = 11

class PlayerStatsDict():
    @staticmethod
    def Construct():
        return {
            Stats.GamesPlayed : 0,
            Stats.TotalWins : 0,
            Stats.CupsMade : 0,
            Stats.GamesCarried : 0,
            Stats.GamesWasCarried : 0,
            Stats.Trolls : 0,
            Stats.BeersDrank : 0.0,
            Stats.TeammateStats : {}
        }

class PlayerStats():
    def __init__(self):
        # _stats is a dict from teammateName : PlayerStatsDict
        # basically represents your stats playing with that person
        self._stats = {}

    def AddGame(self, playerRecord):
        teammate = playerRecord[Stats.Teammate]
        if teammate not in self._stats:
            self._stats[teammate] = PlayerStatsDict.Construct()

        stats = self._stats[teammate]
        stats[Stats.GamesPlayed] += 1
        stats[Stats.CupsMade] += playerRecord[Stats.CupsMade]
        stats[Stats.BeersDrank] += playerRecord[Stats.BeersDrank]

        if playerRecord[Stats.CupsMade] == 0: stats[Stats.Trolls] += 1
        if playerRecord[Stats.DidWin]: stats[Stats.TotalWins] += 1
        if playerRecord[Stats.WasCarried]: stats[Stats.GamesWasCarried] += 1
        if playerRecord[Stats.DidCarry]: stats[Stats.GamesCarried] += 1

    def GetTeammateStats(self, teammate):
        return self._stats[teammate].copy()

    def _getMostCommonPartner(self):
        mostGames = 0
        mostCommonPartner = 'None'
        for teammate, stats in list(self._stats.items()):
           if stats[Stats.GamesPlayed] > mostGames:
                mostGames = stats[Stats.GamesPlayed]
                mostCommonPartner = teammate
        return mostCommonPartner

    def _getCumulativeStatValue(self, key):
        sum = 0
        for stats in list(self._stats.values()):
            sum += stats[key]
        return sum

    def __getitem__(self, key):
        return self._getCumulativeStatValue(key)

    def __str__(self):
        gameCount = self._getCumulativeStatValue(Stats.GamesPlayed)
        if gameCount == 0:
            return 'No games played!'
        cupCount = self._getCumulativeStatValue(Stats.CupsMade)

        winCount = self._getCumulativeStatValue(Stats.TotalWins)
        trollCount = self._getCumulativeStatValue(Stats.Trolls)
        beerCount = self._getCumulativeStatValue(Stats.BeersDrank)
        wasCarriedCount = self._getCumulativeStatValue(Stats.GamesWasCarried)
        didCarryCount = self._getCumulativeStatValue(Stats.GamesCarried)

        wasCarriedRate = wasCarriedCount/float(winCount)*100 if winCount is not 0 else 0
        carryRate = didCarryCount/float(winCount)*100 if winCount is not 0 else 0
        cupsPerGame = float(cupCount)/float(gameCount)
        winRate = (float(winCount)/float(gameCount) * 100)
        mostCommonPartner = self._getMostCommonPartner()

        statString = ("Total Cups: {}\n"
                      "Win %: {:0.2f}%\n"
                      "Most Common Partner: {}\n"
                      "% Wins Carried: {:0.2f}%\n"
                      "% Wins Was Carried: {:0.2f}%\n"
                      "Cups/Game: {:0.2f}\n"
                      "Times Trolled: {}\n"
                      "Total Beers Drank: {:0.2f}\n"
                      "Total Win Count: {}\n"
                      "Total Game Count: {}\n"
        ).format(cupCount,
                 winRate,
                 mostCommonPartner,
                 carryRate,
                 wasCarriedRate,
                 cupsPerGame,
                 trollCount,
                 beerCount,
                 winCount,
                 gameCount)
        return statString
