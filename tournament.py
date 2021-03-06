#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from swisspairings import Draw


def connect():
    """Connect to the PostgreSQL database.
    Returns a database connection and a cursor."""
    connection = psycopg2.connect("dbname=tournament")
    cursor = connection.cursor()
    return [connection, cursor]


def closeConnection(connection, cursor):
    """Close connect to the PostgreSQL database."""
    cursor.close()
    connection.close()


def deleteMatches():
    """Remove all the match records from the database."""
    connection, cursor = connect()
    cursor.execute("DELETE FROM matches")
    connection.commit()
    closeConnection(connection, cursor)


def deletePlayers():
    """Remove all the player records from the database."""
    connection, cursor = connect()
    cursor.execute("DELETE FROM players")
    connection.commit()
    closeConnection(connection, cursor)


def countPlayers():
    """Returns the number (long type) of players currently registered."""
    connection, cursor = connect()
    cursor.execute("SELECT COUNT(*) FROM players AS count")
    count = cursor.fetchone()[0]
    closeConnection(connection, cursor)
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection, cursor = connect()
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    connection.commit()
    closeConnection(connection, cursor)


def getPlayerID(name):
    """Returns the player's ID given by the name."""
    connection, cursor = connect()
    cursor.execute("SELECT id FROM players WHERE name = %s", (name,))
    player_id = cursor.fetchone()
    closeConnection(connection, cursor)
    return player_id


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, ties, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        ties: the number of matches the player has tied
        matches: the number of matches the player has played
    """
    connection, cursor = connect()
    cursor.execute(
        """SELECT
        players.id,
        players.name,
        victories.won,
        ties.tied,
        games_played.played
        FROM players
        LEFT JOIN(
            SELECT * FROM games_won
            ) AS victories ON players.id = victories.player_id
        LEFT JOIN(
            SELECT * FROM games_tied
            ) AS ties ON players.id = ties.player_id
        LEFT JOIN(
            SELECT * FROM games_played
            ) AS games_played ON players.id = games_played.player_id
        ORDER BY
        victories.won DESC,
        ties.tied DESC;"""
    )
    standings = cursor.fetchall()
    closeConnection(connection, cursor)

    return standings


def reportMatch(player_1, player_2=0, player_1_result=1, player_2_result=0):
    """Records the outcome of a single match between two players.
    Default values are used for Bye rounds,
    when only the first player ID is passed.

    Args:
      player_1:  the id number of the first player
      player_2:  the id number of the second player
      player_1_result: player_1 outcome
      player_2_result: player_2 outcome
    """
    connection, cursor = connect()
    cursor.execute(
        "INSERT INTO matches (player_1, player_2) VALUES (%s, %s)",
        (player_1, player_2,)
    )
    cursor.execute('SELECT LASTVAL()')
    game_id = cursor.fetchone()

    cursor.execute(
        "INSERT INTO outcomes ( match_id, player, player_outcome) VALUES (%s, %s, %s)",  # noqa
        (game_id, player_1, player_1_result,)
    )

    # if it's not a Bye-round we insert the second
    # player outcome
    if player_2 != 0:
        cursor.execute(
            "INSERT INTO outcomes ( match_id, player, player_outcome) VALUES (%s, %s, %s)",  # noqa
            (game_id, player_2, player_2_result,)
        )

    connection.commit()
    closeConnection(connection, cursor)


def matchesHistory():
    """Helper function used inside swissPairings().
    Get the matches that have already been played.

    Returns:
      A list of tuples, each of which contains (id1, id2)
      id1: the first player's unique id
      id2: the second player's unique id"""

    connection, cursor = connect()
    cursor.execute("SELECT player_1, player_2 FROM matches")
    history = cursor.fetchall()
    closeConnection(connection, cursor)

    return history


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    sp_handler = Draw(playerStandings(), matchesHistory())

    return sp_handler.getPairings()
