#!/usr/bin/env python
#
# Class for Swiss-system chess tournament drawing.

import math


class Draw():

    """This class helps us draw pairs for
    a Swiss-system chess tournament."""

    def __init__(self, standings, history):
        self.standings = []
        self.pairings = []

        # Helper list for holding the current
        # element we have to pair inside the loop.
        self.current_pair = []

        # List containing already drawn players' ID.
        self.alreadyDrawn = []

        self.numberOfPlayers = len(standings)
        self.roundsPlayed = standings[0][4]
        self.totalRounds = 0

        self.__setTotalRounds(self.numberOfPlayers)
        self.__setStandings(standings)

        # Store matches history inside a list of tuples (Id_1, Id_2).
        self.history = history
        # Store IDs for players who have already had a bye round.
        self.alreadyBye = self.__getPlayersWithByeRound()

    def __setStandings(self, standings):
        """Create an alternative ranking for later computations.
        Each victory gives 3 points.
        Each tie gives 1 point.
        Total points are then added toghether for each player.

        Args:
          standings: a list of tuples like
          (id, name, victories, ties, matches).
        """
        for (i, n, w, t, m) in standings:
            aggregate_standing = (w * 3) + t
            self.standings.append((i, n, aggregate_standing))

    def __setTotalRounds(self, n_of_players, add=0):
        """Find the exact number of rounds that must be played
        throughout the tournament.

        Args:
          n_of_players: number of players enrolled.
          add: the positive integer to be added to n_of_players in order
            to make that amount an exact power of two.
        """
        rounds = math.log((n_of_players + add), 2)

        if(rounds.is_integer()):
            self.totalRounds = rounds
        else:
            self.__setTotalRounds(n_of_players, (add + 1))

    def __getPlayersWithByeRound(self):
        """Look for players who have already been assigned to the Bye-Round.

        Returns:
          A list of integers containing the IDs of those players.
        """
        players_with_bye_round = []

        if(self.numberOfPlayers % 2 != 0):
            for (player_1, player_2) in self.history:
                if(player_2 == 0):
                    players_with_bye_round.append(player_1)

        return players_with_bye_round

    def __reset(self, *args):
        """Each player id passed as argument is put inside the
        self.alreadyDrawn helper list.
        Then the self.current_pair helper is set to empty so it can
        hold a new pair of players.

        Args:
          *args: Player IDs.
        """
        for player in args:
            self.alreadyDrawn.append(player)
        self.current_pair = []

    def __alreadyMatchedCheck(self, id_1, id_2):
        """Find if two players have already played against
        each other in some previous match.

        Args:
          id_1: first player to be checked.
          id_2: second player to be checked.

        Returns:
          Boolean
        """

        if((id_1, id_2) in self.history):
            return True
        if((id_2, id_1) in self.history):
            return True

        return False

    def __getMatchables(self, id_1):
        """Look for players that hasn't been drawn yet and that are
        matchable (i.e. haven't already played against the current player).

        Returns:
          A list of integers containing potentially-valid-opponent IDs.
        """

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
        """This function gets called for tournaments with an odd number of
        enrolled players. If the player who was left out of the draw can't
        be assigned with a Bye-Round (again),
        we have to proceed with a backwards search for a suitable pair
        which can be destroyed, and mixed with
        the single player who was previosly left alone.

        Example:

        - Joe has already had the Bye-Round but doesn't have any
        players left to be paired with.
        - (Mario, Susan) is the last pairing that was drawn
        before Joe was left alone.
        - (Mario, Susan) gets destroyed hoping that:
            - one of them hasn't played against Joe yet, and
            their ranking gap is smaller or equal than *delta*.
            - the other one hasn't already had the Bye-Round.

        If this is OK, Joe gets paired with either Mario or Susan,
        and the one left out gets assigned to the Bye-Round.

        If this check fails, we go backwards
        to the previous pair and do the same try.
        If all the loop fails, we increase *delta* by 1 and
        we try this whole process again, calling this method recursively.

        Args:
          player: the player ID that has to be paired with a physical player.
          delta: the desired ranking gap for making the new pair.
        """

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
        "The method where we actually make the pairings."

        # If we reach the expected number or rounds
        # to be played, no further pairing gets done.
        if(self.totalRounds == self.roundsPlayed):
            return False

        for player in self.standings:
            # If the player hasn't been already drawn
            if (player[0] not in self.alreadyDrawn):  # noqa

                if(len(self.current_pair) == 0):

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
                        # Append current player's id and name
                        # to the current_pair element
                        self.current_pair.append((player[0], player[1]))

                elif(len(self.current_pair) == 1):

                    # Check if we are trying to pair this player
                    # with himself or with someone who he has
                    # already played against.
                    if(self.__alreadyMatchedCheck(player[0], self.current_pair[0][0]) or player[0] == self.current_pair[0][0]):  # noqa

                        # Let's check if also the next elements have
                        # already played with the current player
                        matchables = self.__getMatchables(player[0])
                        if(len(matchables)):
                            # If there are still some matchables, no worries
                            pass
                        else:
                            # Destroy the previous pair
                            # and mix those players with the current player
                            previous_pair = self.pairings.pop()
                            self.alreadyDrawn.remove(previous_pair[0])
                            previous_player = [item for item in self.standings if previous_pair[2] in item]  # noqa

                            self.pairings.append(
                                (previous_player[0][0], previous_player[0][1],
                                 player[0], player[1])
                            )
                            self.__reset(player[0])
                    else:
                        # If everything is fine we create a pair
                        # with two players next to each other in the ranking
                        self.pairings.append(
                            self.current_pair[0] + (player[0], player[1])
                        )
                        self.__reset(self.current_pair[0][0], player[0])

        # If some player was left out of the draw,
        # we try it again
        if(len(self.alreadyDrawn) < len(self.standings)):
            self.__draw()

    def getPairings(self):
        """
        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        self.__draw()
        return self.pairings
