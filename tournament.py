#!/usr/bin/env python
"""
Implementation of a Swiss-system tournament

Interacts with the tournament database to add and remove players, add matches
get player stadings, and pair players.
"""

from __future__ import division
import operator
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("delete from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("delete from players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("select count(distinct id) from players;")
    results = cursor.fetchall()
    DB.close()
    return int(results[0][0])


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("insert into players values (DEFAULT,%s)", (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("select id, name, wins, total_matches from player_totals;")
    results = cursor.fetchall()
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("insert into matches values(DEFAULT,%s,%s)", (winner, loser))
    DB.commit()
    DB.close()

 
 
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
    DB = connect()
    cursor = DB.cursor()
    
    # Query to get players and their win record
    cursor.execute("select id, name, wins, total_matches from player_totals;")
    results = cursor.fetchall()
    player_win_record = sorted(results,key=lambda record: record[2] / record[3])
    pairs = []
    print player_win_record
    num_players = len(player_win_record)
   
    # Pair users with adjacent win records
    for i in range(0, num_players, 2):
        user_one = player_win_record[i]
        user_two = player_win_record[i+1]
        pairs.append(
            (user_one[0], user_one[1], user_two[0], 
            user_two[1]))
    return pairs

