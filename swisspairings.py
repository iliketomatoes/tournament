#!/usr/bin/env python
#
# Draw class for chess tournament drawing

import math


class Draw():

    """This class helps us make Swiss Pairings draw for
    a chess tournament"""

    def __init__(self, standings, history):
        self.standings = []
        self.pairings = []
        self.current_pair = []
        self.alreadyDrawn = []
        self.numberOfPlayers = len(standings)
        self.roundsPlayed = standings[0][4]
        self.totalRounds = 0
        self.__setTotalRounds(self.numberOfPlayers)
        self.__setStandings(standings)

        # Store matches history inside a list of tuples (Id_1, Id_2)
        self.history = history
        # Store IDs for players who have already had a bye round
        self.alreadyBye = self.__getPlayersWithByeRound()

    def __setStandings(self, standings):
        for (i, n, w, t, m) in standings:
            aggregate_standing = (w * 3) + t
            self.standings.append((i, n, aggregate_standing))

    def __setTotalRounds(self, n_of_players, add=0):

        rounds = math.log((n_of_players + add), 2)

        if(rounds.is_integer()):
            self.totalRounds = rounds
        else:
            self.__setTotalRounds(n_of_players, (add + 1))

    def __getPlayersWithByeRound(self):
        players_with_bye_round = []

        if(self.numberOfPlayers % 2 != 0):
            for (player_1, player_2) in self.history:
                if(player_2 == 0):
                    players_with_bye_round.append(player_1)

        return players_with_bye_round

    def __reset(self, *args):
        for player in args:
            self.alreadyDrawn.append(player)
        self.current_pair = []

    def __alreadyMatchedCheck(self, id_1, id_2):

        if((id_1, id_2) in self.history):

            return True

        if((id_2, id_1) in self.history):

            return True

        return False

    def __getMatchables(self, id_1):

        players_ids = [row[0] for row in self.standings]
        not_drawn_players_ids = list(
            set(players_ids) - set(self.alreadyDrawn)
        )

        matchables = []

        for p_id in not_drawn_players_ids:
            if(not self.__alreadyMatchedCheck(id_1, p_id) and id_1 != p_id):
                matchables.append(p_id)
                break

        return matchables

    def __swapWithPreviousPairs(self, player, delta=1):

        idStanding = {p[0]: p[2] for p in self.standings}

        found_swap = False
        element_to_be_swapped = None

        for i, (pair) in enumerate(self.pairings):

            if(abs(idStanding[pair[0]] - idStanding[player[0]]) <= delta):

                if(not self.__alreadyMatchedCheck(pair[0], player[0]) and pair[2] not in self.alreadyBye):  # noqa
                    element_to_be_swapped = (pair[2], pair[3])
                    element_to_be_kept = (pair[0], pair[1])
                    self.pairings.pop(i)
                    self.pairings.append(
                        element_to_be_kept + (player[0], player[1])
                    )
                    self.__reset(player[0])
                    found_swap = True
                    break

            if(abs(idStanding[pair[2]] - idStanding[player[0]]) <= delta):

                if(not self.__alreadyMatchedCheck(pair[2], player[0]) and pair[0] not in self.alreadyBye):  # noqa
                    element_to_be_swapped = (pair[0], pair[1])
                    element_to_be_kept = (pair[2], pair[3])
                    self.pairings.pop(i)
                    self.pairings.append(
                        (player[0], player[1]) + element_to_be_kept
                    )
                    self.__reset(player[0])
                    found_swap = True
                    break

        # Append the bye round for element_to_be_swapped
        if(element_to_be_swapped != None and found_swap):
            self.pairings.append(
                element_to_be_swapped + (0, None)
            )
        else:
            new_delta = delta + 1
            self.__swapWithPreviousPairs(player, new_delta)

    def __draw(self):

        if(self.totalRounds == self.roundsPlayed):
            return False

        for player in self.standings:
            # If the player hasn't been drawn already
            if (player[0] not in self.alreadyDrawn):  # noqa

                if(len(self.current_pair) == 0):
                    # Append current player's id and name
                    # to the current_pair element

                    if(self.numberOfPlayers % 2 != 0 and int(len(self.standings) / 2) == len(self.pairings)):  # noqa

                        if(player[0] in self.alreadyBye):
                            # Swap the remaining element with some
                            # elements in the previous pairs
                            self.pairings.reverse()
                            self.__swapWithPreviousPairs(player)

                        else:
                            self.pairings.append(
                                (player[0], player[1]) + (0, None)
                            )
                            self.__reset(player[0])

                    else:
                        self.current_pair.append((player[0], player[1]))

                elif(len(self.current_pair) == 1):

                    if(self.__alreadyMatchedCheck(player[0], self.current_pair[0][0]) or player[0] == self.current_pair[0][0]):  # noqa

                        # Let's check if also the next elements have
                        # already played with the current player

                        matchables = self.__getMatchables(player[0])
                        if(len(matchables)):
                            pass
                        else:
                            # Destroy the previous pair
                            previous_pair = self.pairings.pop()
                            self.alreadyDrawn.remove(previous_pair[0])
                            previous_player = [item for item in self.standings if previous_pair[2] in item]  # noqa

                            self.pairings.append(
                                (previous_player[0][0], previous_player[0][1],
                                 player[0], player[1])
                            )
                            self.__reset(player[0])
                    else:
                        self.pairings.append(
                            self.current_pair[0] + (player[0], player[1])
                        )
                        self.__reset(self.current_pair[0][0], player[0])

        if(len(self.alreadyDrawn) < len(self.standings)):
            self.__draw()

    def getPairings(self):
        self.__draw()
        return self.pairings
