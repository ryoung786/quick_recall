from Model import Model, DB, BaseFinder
from Question import Question
from Player import Player

class Match(Model):
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

    collection = 'matches'

    def __init__(self, official=False, teams=[], questions=[], _id=None):
        self.official = official
        self.teams = teams
        self.questions = questions
        self._id = _id

    @staticmethod
    def fromJSON(json):
        return Match(
            json.get('official', False),
            json.get('teams', []),
            json.get('questions', []),
            json.get('_id'))

    def addPlayer(team, player):
        pass

    def addQuestion(question_or_id):
        '''
        Takes a Model.Question or ObjectId, adds it to its questions,
        and saves the match to the database

        '''
        question_id = question_or_id
        if isinstance(question_or_id, Question):
            question_id = question_or_id._id
        self.questions += [question_id]
        self.save()
        return self

    def Teams(self, populate_players=False):
        return [Team.fromJSON(team, populate_players) for team in self.teams]

    def Questions(self, limit=0, skip=0):
        db = self.getDB()
        questions = db.questions.find({"_id": {"$in": self.questions}}).skip(skip).limit(limit)
        return [Question.fromJSON(q) for q in questions]

class Team(DB):

    def __init__(self, name, players=[], score=0):
        self.name = name
        self.players = players
        self.score = score

    def Players(self, limit=0, skip=0):
        db = self.getDB()
        players = db.players.find({"_id": {"$in": self.players}}).skip(skip).limit(limit)
        return [Player.fromJSON(p) for p in players]

    @staticmethod
    def fromJSON(json, populate_players=False):
        team = Team(
            json['name'],
            json.get('players', []),
            json.get('score', 0))
        if populate_players:
            team.players = team.Players()
        return team

class MatchFinder(BaseFinder):
    collection = 'matches'

    def toModel(self, json):
        return Match.fromJSON(json)
