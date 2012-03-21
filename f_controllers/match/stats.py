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
    tag_stats = {}
    tag_to_x = {}
    for team in match['teams']:
        for p_id in team['players']:
            tag_stats[p_id] = matchStats(p_id, match, db)
            tagset = set(tag_stats[p_id].correct.keys() + tag_stats[p_id].incorrect.keys())
            tagset.remove('total')
            tag_to_x[p_id] = {}
            for i,tag in enumerate(tagset):
                tag_to_x[p_id][tag] = (1+i)*100
        team['players'] = [PlayerStats(p, matchStats(p['_id'], match, db))
                           for p in f_models.players.findMany(team['players'], db)]

    return render_template("f/matches/stats.html",
                           match=match,
                           tag_stats=tag_stats,
                           tag_to_x_map=tag_to_x)
