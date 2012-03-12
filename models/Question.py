from Model import Model, BaseFinder

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
        self.player_id = player_id # ObjectId
        self.correct = correct
        self.tags = tags
        self._id = _id
        self.player = None

    @staticmethod
    def fromJSON(json):
        return Question(
            json['player_id'],
            json['correct'],
            json.get('tags'),
            json.get('_id'))

    def Player(self):
        if self.player:
            return self.player
        db = self.getDB()
        return db.players.find_one({"_id": self.player_id})

class QuestionFinder(BaseFinder):
    collection = 'questions'
