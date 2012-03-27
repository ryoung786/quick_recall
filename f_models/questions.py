import config
from pymongo.objectid import ObjectId

'''
{
  "_id"         : ObjectId("4f5c4cf2161d1519bc000000"),
  "tags"        : [ "history", "european history" ],
  "score"       : 1,
  "answers"     : [ {"player_id"   : ObjectId("4f559ed5a174fb1b5d978ddb"),
                     "correct"     : true,
                     "time_left"   : 2000 }, ... ]
}

'''


def save(question, db):
    return db.questions.save(question)

def find(question_id, db):
    return db.questions.find_one({"_id": ObjectId(question_id)})
