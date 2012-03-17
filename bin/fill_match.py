#! /usr/bin/python

import sys
import os
import random
_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, _root_dir)

from models import *

# if (len(sys.argv) < 3):
#     print "Usage:" + sys.argv[0] + " first_name last_name"
#     sys.exit()


players = [
    ["4f559ed5a174fb1b5d978ddb", # young
     "4f5ae1cd67a69c1f6bf97676", # taber
     "4f5d1a9e161d151563000001"  # katherine
     ],
    ["4f5d86dd161d153ff4000000", # wes
     "4f61eed751ad6e44112c4cc2"  # jake
     ]
]

teams = [Team('A', players[0]), Team('B', players[1])]

all_tags = ["history", "math", "science", "literature", "geography", "religion", \
            "mythology", "art", "music", "pop culture"]


def getTags():
    tags = {}
    num_tags = random.randint(0,3)
    for x in range(num_tags):
        tag = all_tags[random.randint(0, len(all_tags)-1)]
        tags[tag] = 1
    return tags.keys()

def addQuestion(m):
    question = Question(getTags(), answers=[]) # why do i have to specify the default?
    question.save()
    buzz = random.randint(0,1) == 1
    if buzz:
        team_index = random.randint(0,1)
        team_players = players[team_index]
        player_id = team_players[random.randint(0, len(team_players)-1)]

        correct = random.randint(0,1) == 1
        answer = Answer(player_id, correct)
        question.addAnswer(answer)
        if correct: m.increaseTeamScoreOfPlayer(player_id, 1)

        if (not correct) and (random.randint(0,1) == 1):
            team_index = 1 - team_index
            team_players = players[team_index]
            player_id = team_players[random.randint(0, len(team_players)-1)]

            correct = random.randint(0,1) == 1
            answer = Answer(player_id, correct)
            question.addAnswer(answer)
            if correct: m.increaseTeamScoreOfPlayer(player_id, 1)
    m.addQuestion(question)


def go():
    m = Match()
    for team in teams:
        m.addTeam(team)
    for i in range(40):
        addQuestion(m)
    m.save()
    return m

if __name__ == '__main__':
    from pprint import pprint
    pprint(go().asJSON())
