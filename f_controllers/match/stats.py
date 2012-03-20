from config import config
from pymongo import Connection
from flask import render_template
from collections import namedtuple
import f_models.players
import f_models.matches

def getDB():
    '''
    this is a temporary hack until i can figure out where
    to put it
    '''
    host = config['DB']['host']
    port = config['DB']['port']
    db = config['DB']['name']
    return Connection(host=host, port=port)[db]

def render(match_id):
    matchStats = f_models.players.statsForMatch
    db = getDB()
    match = f_models.matches.find(match_id, db)

    PlayerStats = namedtuple('PlayerStats', 'player stats')
    for team in match['teams']:
        team['players'] = [PlayerStats(p, matchStats(p['_id'], match, db))
                           for p in f_models.players.findMany(team['players'], db)]
    return render_template("f/matches/stats.html",
                           match=match)
