from Model import Model, BaseFinder, DB
from Player import PlayerFinder
from pymongo.objectid import ObjectId

class Question(Model):
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

    collection = 'questions'

    def __init__(self, tags=[], score=1, answers=[], _id=None):
        self.tags = tags
        self.score = score
        self.answers = answers
        self._id = _id

    def addAnswer(self, answer):
        self.answers += [vars(answer)]
        self.save()
        return self

    def Answers(self):
        return [Answer.fromJSON(answer) for answer in self.answers]

    @staticmethod
    def fromJSON(json):
        return Question(
            json.get('tags', []),
            json.get('score', 1),
            json.get('answers', []),
            json.get('_id'))


class Answer(object):
    def __init__(self, player_id, correct, time_left=None):
        self.player_id = ObjectId(player_id)
        self.correct = correct
        self.time_left = time_left

    def Player(self):
        return PlayerFinder().find(self.player_id)

    @staticmethod
    def fromJSON(json):
        return Answer(
            json['player_id'],
            json['correct'],
            json.get('time_left'))



class QuestionFinder(BaseFinder):
    collection = 'questions'

    def toModel(self, json):
        return Question.fromJSON(json)
