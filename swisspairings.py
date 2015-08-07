
class Draw():

    """This class helps us make Swiss Pairings draw for
    a chess tournament"""

    def __init__(self):
        self.standings = []
        self.pairings = []
        self.bestScore = 0
        self.current_pair = []
        self.alreadyDrawn = []

    def setStandings(self, standings):
        for (i, n, w, t, m) in standings:
            aggregate_standing = w + (t * 0.5)
            self.standings.append((i, n, aggregate_standing))

    def setHistory(self, history):
        self.history = history

    def __alreadyByePlayed(self):
        return None

    def getPairings(self):
        self.__draw()
        return self.pairings

    def __reset(self):
        self.bestScore = 0
        self.current_pair = []

    def __draw(self):
        for player in self.standings:
            if (player[0] not in self.alreadyDrawn):

                if(player[2] >= self.bestScore and len(self.current_pair) == 0):  # noqa
                    self.bestScore = player[2]
                    self.current_pair.append((player[0], player[1]))

                elif(len(self.current_pair) == 1):
                    self.current_pair.append((player[0], player[1]))
                    self.pairings.append(
                        self.current_pair[0] + self.current_pair[1])
                    self.__reset()

                self.alreadyDrawn.append(player[0])
