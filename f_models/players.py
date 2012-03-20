import config
from pymongo.objectid import ObjectId
from collections import namedtuple

'''
{
"_id"   : ObjectId("4f559ed5a174fb1b5d978ddb"),
"first" : "ryan",
"last"  : "young"
}

'''

def save(player, db):
    return db.players.save(player)

def find(player_id, db):
    return db.players.find_one({"_id": ObjectId(player_id)})

def findMany(player_ids, db):
    return db.players.find({"_id": {"$in": player_ids}})

def avatar(player_id):
    if config.isEnabled('gravatar'):
        return "http://www.gravatar.com/avatar/%s?d=retro&s=50" % (str(player_id))
    else:
        return ""

def name(player, full=True):
    if full: return "%s %s" % (player['first'], player['last'])
    else:    return player['first']

def statsForQuestions(player_id, questions):
    correct = {'total': 0}
    incorrect = {'total': 0}
    for q in questions:
        for a in q['answers']:
            if a['player_id'] != ObjectId(player_id): continue
            d = incorrect
            if a['correct']: d = correct
            d['total'] += 1
            for tag in q['tags']:
                val = d.get(tag, 0)
                d[tag] = val + 1
    total = correct['total'] + incorrect['total']
    percent = 0
    if total > 0:
        percent = 100 * correct['total'] / (total)
    Stats = namedtuple('Stats', 'correct incorrect total percent')
    return Stats(correct, incorrect, total, percent)

def statsForMatchId(player_id, match_id, db):
    match = db.matches.find_one({"_id": ObjectId(match_id)}, {'questions': 1})
    return statsForMatch(player_id, match, db)

def statsForMatch(player_id, match, db):
    question_ids = match['questions']
    questions = db.questions.find({"_id": {"$in": question_ids}})
    return statsForQuestions(player_id, questions)

def statsForAllTime(player_id, db):
    questions = db.questions.find({"answers.player_id": ObjectId(player_id)})
    return statsForQuestions(player_id, questions)
