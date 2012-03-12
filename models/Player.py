from Model import Model

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

    @staticmethod
    def fromJSON(json):
        return Player(
            json['first'],
            json['last'],
            json.get('_id'))
