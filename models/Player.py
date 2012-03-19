from Model import Model, BaseFinder
# from Question import QuestionFinder
import config

class Player(Model):
    '''
    {
      "_id"   : ObjectId("4f559ed5a174fb1b5d978ddb"),
      "first" : "ryan",
      "last"  : "young"
    }

    '''

    collection = 'players'

    def __init__(self, first, last, _id=None):
        self.first = first
        self.last = last
        self._id = _id

    def avatar(self):
        if config.isEnabled('gravatar'):
            return "http://www.gravatar.com/avatar/%s?d=retro&s=50" % (str(self._id))
        else:
            return ""

    def name(self, full=True):
        if full: return "%s %s" % (self.first, self.last)
        else:    return self.first

    # for a player, return (num_correct, num_incorrect, percent_correct)
    def correctCountForMatch(self, match):
        return self.correctCountForQuestions(match.Questions())

    # def correctCountForAllQuestions(self):
    #     questions = QuestionFinder().findByPlayerId(self._id)
    #     return self.correctCountForQuestions(questions)

    def correctCountForQuestions(self, questions):
        correct = {'total': 0}
        incorrect = {'total': 0}
        for q in questions:
            for a in q.Answers():
                if a.player_id != self._id: continue
                d = incorrect
                if a.correct: d = correct
                d['total'] += 1
                for tag in q.tags:
                    val = d.get(tag, 0)
                    d[tag] = val + 1
        total = correct['total'] + incorrect['total']
        if total > 0:
            percent = 100 * correct['total'] / (total)
        else:
            percent = 0
        return (correct, incorrect, total, percent)

    @staticmethod
    def fromJSON(json):
        return Player(
            json['first'],
            json['last'],
            json.get('_id'))

class PlayerFinder(BaseFinder):
    collection = 'players'

    def toModel(self, json):
        return Player.fromJSON(json)
