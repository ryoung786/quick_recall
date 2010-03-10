# models.py
 
from google.appengine.ext import db
 
class Visitor(db.Model):
    ip = db.StringProperty()
    added_on = db.DateTimeProperty(auto_now_add=True)

class Player(db.Model):
    user = db.UserProperty(required=False)
    name = db.StringProperty()

class Answer(db.Model):
    answer = db.TextProperty(required=True)

class Question(db.Model):
    question = db.TextProperty(required=True)
    answer = db.ReferenceProperty(Answer, required=True,
                                  collection_name='questions')
class PlayerAnswers(db.Model):
    correct = db.BooleanProperty(required=True)
    player = db.ReferenceProperty(Player, required=True,
                                  collection_name ='player_answers')
    question = db.ReferenceProperty(Question, required=True,
                                    collection_name='player_answers')

class Team(db.Model):
    team_name = db.StringProperty(required=True)

class TeamPlayerLink(db.Model):
    team = db.ReferenceProperty(Team, required=True,
                                collection_name='players')
    player = db.ReferenceProperty(Player, required=True,
                                  collection_name='teams')

class Match(db.Model):
    team = db.ReferenceProperty(Team, required=True,
                                collection_name='matches')
    score = db.IntegerProperty(required=False)
    win = db.BooleanProperty(required=False)
    time = db.DateTimeProperty(required=False)

class MatchStats(db.Model):
    match = db.ReferenceProperty(Match, required=True,
                                 collection_name='match_stats')
    team_miss = db.IntegerProperty(required=True)
    team_correct = db.IntegerProperty(required=True)
    player_miss = db.IntegerProperty(required=True)
    player_correct = db.IntegerProperty(required=True)

class Tag(db.Model):
    tag = db.CategoryProperty(required=True)

class QuestionTagLink(db.Model):
    question = db.ReferenceProperty(Question, required=True,
                                    collection_name='tags')
    tag = db.ReferenceProperty(Tag, required=True,
                               collection_name='questions')

def getQuestionsWithTag(tag):
    '''
    lit_questions = getQuestionsWithTag("Literature")
    for question in lit_questions:
      print "Q: %s" % (question.question)
      print "A: %s" % question.answer.answer
      print "Tagged with %s" % [t.tag.tag for t in question.tags]
    '''
    res = []
    for q in Question.all():
        tag_strings = [t.tag.tag for t in q.tags]
        if tag in tag_strings:
            res += [q]
    return res

def getPlayerAnswers(player_or_question):
    playerAnswers = player_or_question.player_answers
    return (len([answer for answer in playerAnswers if answer.correct]), playerAnswers.count())
