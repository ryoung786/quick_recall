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
        "score" : 0,
        "name" : "A"
    }
  ],
  "questions" : [
      ObjectId("4f5b0c62161d151920000000"),
      ObjectId("4f5b0c62161d151920000001")
  ]
}

'''

def save(match, db):
    return db.matches.save(match)

def find(match_id, db):
    return db.matches.find_one({"_id": ObjectId(match_id)})
