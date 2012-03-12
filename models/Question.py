from Model import Model, BaseFinder
from Player import PlayerFinder
from pymongo.objectid import ObjectId

class Question(Model):
    '''
    {
      "_id"       : ObjectId("4f5c4cf2161d1519bc000000"),
      "player_id" : ObjectId("4f559ed5a174fb1b5d978ddb"),
      "correct"   : true,
      "tags"      : [ "history" ]
    }

    '''

    collection = 'questions'

    def __init__(self, player_id, correct, tags=[], _id=None):
        self.player_id = ObjectId(player_id)
        self.correct = correct
        self.tags = tags
        self._id = _id

    @staticmethod
    def fromJSON(json):
        return Question(
            json['player_id'],
            json['correct'],
            json.get('tags'),
            json.get('_id'))

    def Player(self):
        return PlayerFinder().find(self.player_id)

class QuestionFinder(BaseFinder):
    collection = 'questions'

    def toModel(self, json):
        return Question.fromJSON(json)
