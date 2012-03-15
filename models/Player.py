from Model import Model, BaseFinder
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
