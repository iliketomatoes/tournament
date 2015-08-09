#!/usr/bin/env python
#
# Test cases for tournament.py

import random
import math
from tournament import *


class TournamentSimulation():

    def __init__(self, players_list):
        self.possibleOutcomes = [
            [1, 0],
            [0.5, 0.5],
            [0, 1]
        ]
        deletePlayers()
        deleteMatches()
        random.shuffle(players_list)
        for player in players_list:
            registerPlayer(player)

    def execute(self):

        pairings = swissPairings()

        if len(pairings):
            for pair in pairings:
                # Check if it was a Bye round
                # In that case player 1 wins
                if(pair[2] == 0 or pair[2] == None):
                    reportMatch(pair[0])
                else:
                    outcome = random.choice(self.possibleOutcomes)
                    reportMatch(pair[0], pair[2], outcome[0], outcome[1])
            self.execute()
        else:
            return False


def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "  # noqa
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have five columns.")
    [(id1, name1, wins1, ties1, matches1),
     (id2, name2, wins2, ties2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "  # noqa
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."  # noqa


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, 1, 0)
    reportMatch(id3, id4, 1, 0)
    standings = playerStandings()
    for (i, n, w, t, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, 1, 0)
    reportMatch(id3, id4, 1, 0)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testOddPlayersTournament():
    # 9 players
    players = [
        "Giancarlo Soverini",
        "Leonardo Sarallo",
        "Nicolo Micheletti",
        "Ugo Pecchioli",
        "Marco Van Basten",
        "Michele Pratesi",
        "Mario Suarez",
        "Superman",
        "Donald Trump"
    ]

    simulation = TournamentSimulation(players)
    simulation.execute()
    standings = playerStandings()
    rounds_played = standings[0][4]

    match_history = matchesHistory()

    print "ODD TOURNAMENT SIMULATION"
    print "Rounds played: ", rounds_played
    print "Standings: ", playerStandings()

    for (p_id, name, won, tied, played) in standings:
        matches = []
        for (id_1, id_2) in match_history:
            if(id_1 == p_id or id_2 == p_id):
                match = frozenset([id_1, id_2])
                matches.append(match)
        if len(matches) != len(set(matches)):
            raise ValueError("ODD TOURNAMENT: Some players have either re-matched or have more than one Bye-round")  # noqa

    print """9. ODD TOURNAMENT:
    There are no rematches among players,
    nor players with multiple Bye-rounds"""

    if(rounds_played >= math.log((countPlayers()), 2)):
        print """10. ODD TOURNAMENT:
        Number of rounds played is equal
        or greater than log2(n_of_players)"""
    else:
        raise ValueError(
            "ODD TOURNAMENT: Number of rounds to be played must be equal or greater than log2(n_of_players)")  # noqa


def testEvenPlayersTournament():
    # 8 players
    players = [
        "Giancarlo Soverini",
        "Leonardo Sarallo",
        "Nicolo Micheletti",
        "Ugo Pecchioli",
        "Marco Van Basten",
        "Michele Pratesi",
        "Mario Suarez",
        "Superman"
    ]

    simulation = TournamentSimulation(players)
    simulation.execute()
    standings = playerStandings()
    rounds_played = standings[0][4]

    match_history = matchesHistory()

    print "EVEN TOURNAMENT SIMULATION"
    print "Rounds played: ", rounds_played
    print "Standings: ", playerStandings()

    for (p_id, name, won, tied, played) in standings:
        matches = []
        for (id_1, id_2) in match_history:
            if(id_1 == p_id or id_2 == p_id):
                match = frozenset([id_1, id_2])
                matches.append(match)
        if len(matches) != len(set(matches)):
            raise ValueError("EVEN TOURNAMENT: Some players have either re-matched or have more than one Bye-round")  # noqa

    print """11. EVEN TOURNAMENT:
    There are no rematches among players,
    nor players with multiple Bye-rounds"""

    if(rounds_played >= math.log((countPlayers()), 2)):
        print """12. EVEN TOURNAMENT:
        Number of rounds played is equal
        or greater than log2(n_of_players)"""
    else:
        raise ValueError(
            "EVEN TOURNAMENT: Number of rounds to be played must be equal or greater than log2(n_of_players)")  # noqa


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testOddPlayersTournament()
    testEvenPlayersTournament()
    print "Success!  All tests pass!"
