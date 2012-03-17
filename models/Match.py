from Model import Model, DB, BaseFinder
from Question import QuestionFinder
from Player import PlayerFinder

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

    def addPlayer(self, team, player):
        pass

    def addTeam(self, team):
        self.teams += [team.asJSON()]
        self.save()
        return self

    def addQuestion(self, question):
        '''
        Takes a Model.Question, adds it to its questions,
        and saves the match to the database

        '''
        self.questions += [question._id]
        self.save()
        return self

    def addQuestionAndAnswer(self, question, answer):
        self.questions += [question._id]
        if answer.correct:
            self.increaseTeamScoreOfPlayer(answer.player_id, question.score)
        self.save()
        return self

    def increaseTeamScoreOfPlayer(self, player_id, score):
        for team in self.teams:
            if player_id in team['players']:
                team['score'] += score
                return
        raise LookupError("Player id not in match" + player_id)

    def Teams(self, populate_players=False):
        return [Team.fromJSON(team, populate_players) for team in self.teams]

    def Questions(self, limit=0, skip=0):
        return QuestionFinder().findMany(self.questions)



class Team(object):

    def __init__(self, name, players=[], score=0):
        self.name = name
        self.players = players
        self.score = score

    def Players(self, limit=0, skip=0):
        return PlayerFinder().findMany(self.players)

    def asJSON(self):
        return vars(self).copy()

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
