import config
from pymongo.objectid import ObjectId

'''
{
  "_id" : ObjectId("4f5ae40867a69c1f6bf97677"),
  "official" : false,
  "teams" : [
    {
        "players" : [
            ObjectId("4f559ed5a174fb1b5d978ddb"),
            ObjectId("4f5ae1cd67a69c1f6bf97676")
        ],
        "score": 3,
        "name" : "A",
        "score_history" : [0,0,0,1,2,2,2,3,4,2,2,2,3]
    }
  ],
  "questions" : [
      ObjectId("4f5b0c62161d151920000000"),
      ObjectId("4f5b0c62161d151920000001")
  ],
}

'''

def save(match, db):
    return db.matches.save(match)

def find(match_id, db):
    return db.matches.find_one({"_id": ObjectId(match_id)})

def matchOrId(match_or_id, db):
    return find(match_or_id, db) if isinstance(match_or_id, ObjectId) \
                                 else match_or_id

def playerToTeamDict(match_or_id, db):
    match = matchOrId(match_or_id, db)
    players = {}
    for i, team in enumerate(match['teams']):
        for player_id in team['players']:
            players[player_id] = i
    return players

def scoreTracker(match_id, db):
    match = find(match_id, db)
    questions = db.questions.find({"_id": {"$in": match['questions']}})

def addQuestion(match_or_id, question, db):
    m = matchOrId(match_or_id, db)
    m['questions'] += [question["_id"]]
    player_to_team = playerToTeamDict(m, db)
    correct_teams = [player_to_team[answer['player_id']] \
                     for answer in question['answers'] if answer['correct'] ]
    for i, team in enumerate(m['teams']):
        score = 0
        if i in correct_teams:
            score = 1
        team['score'] += score
        team['score_history'] += [score]
    db.matches.save(m)
    return m
