#! /usr/bin/python

import sys
import os
import random
_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, _root_dir)

from config import config
from pymongo import Connection
from pymongo.objectid import ObjectId


host = config['DB']['host']
port = config['DB']['port']
db = config['DB']['name']
db = Connection(host=host, port=port)[db]

players = [
    [ObjectId("4f559ed5a174fb1b5d978ddb"), # young
     ObjectId("4f5ae1cd67a69c1f6bf97676"), # taber
     ObjectId("4f5d1a9e161d151563000001")  # katherine
     ],
    [ObjectId("4f5d86dd161d153ff4000000"), # wes
     ObjectId("4f61eed751ad6e44112c4cc2")  # jake
     ]
]

teams = [{'name': 'A',
          'players': players[0],
          'score': 0,
          'score_history': []},
         {'name': 'B',
          'players': players[1],
          'score': 0,
          'score_history': []}]

all_tags = ["history", "math", "science", "literature", "geography", "religion", \
            "mythology", "art", "music", "pop culture"]

def getTags():
    tags = {}
    num_tags = random.randint(1,3)
    for x in range(num_tags):
        tag = all_tags[random.randint(0, len(all_tags)-1)]
        tags[tag] = 1
    return tags.keys()

def randomPlayerOnTeam(team_index):
    team_players = players[team_index]
    return team_players[random.randint(0, len(team_players)-1)]


def buzz():
    return random.randint(0,1) == 1

wasCorrect = buzz

def addAnswer(m, question, was_correct, team_that_buzzed):
    player_id_that_buzzed = randomPlayerOnTeam(team_that_buzzed)
    score = question["score"] if was_correct else 0
    if was_correct:
        print "team %s buzzed, it was correct;   score: %s" % (team_that_buzzed, score)
    else:
        print "team %s buzzed, it was INcorrect; score: %s" % (team_that_buzzed, score)
    m["teams"][team_that_buzzed]["score"] += score
    m["teams"][team_that_buzzed]["score_history"][-1] = \
        m["teams"][team_that_buzzed]["score"]
    answer = {"player_id": player_id_that_buzzed,
              "correct" : was_correct,
              "time_left" : random.randint(0, 5000)}
    question["answers"] += [answer]

def addQuestion(m):
    # generate a question
    for team in m["teams"]:
        team["score_history"] += [team["score"]]

    question = {'tags': getTags(), 'score': 1, 'answers': []}
    was_correct = wasCorrect()
    if buzz():
        team_that_buzzed = random.randint(0,1)
        addAnswer(m, question, was_correct, team_that_buzzed)
        if (not was_correct) and buzz():
            addAnswer(m, question, wasCorrect(), 1-team_that_buzzed)
    db.questions.save(question)
    m['questions'] += [question["_id"]]

def populateMatch():
    m = {'teams': teams, 'questions': [], 'official': False}
    m_id = db.matches.save(m)
    for i in range(400):
        addQuestion(m)
        if m['teams'][0]['score'] != m['teams'][0]['score_history'][-1] or \
                m['teams'][1]['score'] != m['teams'][1]['score_history'][-1]:
            print "wtf: " + i
        
    db.matches.save(m)
    return m

if __name__ == '__main__':
    from pprint import pprint
    m = populateMatch()
    pprint(m)
    print "http://localhost:5000/matches/%s/stats" % m["_id"]
