from config import config
from pymongo import Connection
from flask import render_template
import f_models.players

def getDB():
    '''
    this is a temporary hack until i can figure out where
    to put it
    '''
    host = config['DB']['host']
    port = config['DB']['port']
    db = config['DB']['name']
    return Connection(host=host, port=port)[db]

def render(player_id):
    db = getDB()
    player = f_models.players.find(player_id, db)

    name = f_models.players.name(player)
    stats = f_models.players.statsForAllTime(player_id, db)
    tagset = set(stats.correct.keys() + stats.incorrect.keys())
    tagset.remove('total')
    tag_to_x = {}
    for i,tag in enumerate(tagset):
        tag_to_x[tag] = (1+i)*100
    return render_template("f/players/stats.html",
                           stats=stats,
                           name=name,
                           tag_to_x_map=tag_to_x)
