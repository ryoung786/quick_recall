'''
Created on Feb 13, 2010

@author: ryan
'''
import cgi, os, models
from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from models import Question, Answer, Player, PlayerAnswers, Tag, QuestionTagLink, Team, TeamPlayerLink 

class CreateMatch(webapp.RequestHandler):
        
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'createMatch.html')
        self.response.out.write(template.render(path, None))        
        
    def post(self):
        team1_txt = cgi.escape(self.request.get('team1'))
        team2_txt = cgi.escape(self.request.get('team2'))
        players1_txt = cgi.escape(self.request.get('players1'))
        players2_txt = cgi.escape(self.request.get('players2'))
        
        players1_arr = [x.strip() for x in players1_txt.split(',')]
        players1_arr = [x for x in players1_arr if '' != x]
        
        players2_arr = [x.strip() for x in players2_txt.split(',')]
        players2_arr = [x for x in players2_arr if '' != x]
        
        team1 = Team.gql('WHERE team_name = :1', team1_txt).get()
        if team1 == None:
            team1 = Team(team_name=team1_txt)
            team1.put()
        
        team2 = Team.gql('WHERE team_name = :1', team2_txt).get()
        if team2 == None:
            team2 = Team(team_name=team2_txt)
            team2.put()
            
        for name in players1_arr:
            player = Player(name=name)
            player.put()
            tplink = TeamPlayerLink(team=team1, player=player)
            tplink.put()
        for name in players2_arr:
            player = Player(name=name)
            player.put()
            tplink = TeamPlayerLink(team=team2, player=player)
            tplink.put()
        
#        I'm missing the ability to link Questions
#        to Matches.  I need to add this functionality
#        into the DB
        self.redirect('/Match/AddQuestion', False)
        
        
class NewQuestion(webapp.RequestHandler):
    def get(self):
        template_data = {
            'team1': {'name': 'team 1', 'score': 0},
            'team2': {'name': 'team 2', 'score': 0},
        }
        path = os.path.join(os.path.dirname(__file__), 'addQuestion.html')
        self.response.out.write(template.render(path, template_data))
        
    def post(self):
        question_txt = cgi.escape(self.request.get('question'))
        answer_txt = cgi.escape(self.request.get('answer'))
        tags_txt = cgi.escape(self.request.get('tags'))
        correct_txt = cgi.escape(self.request.get('correct'))
        incorrect_txt = cgi.escape(self.request.get('incorrect'))
                
        answer = Answer(answer=answer_txt)
        answer.put()
        question = Question(question=question_txt,
                            answer=answer)
        question.put()
        tags_arr = [x.strip() for x in tags_txt.split(',')]
        tags_arr = [x for x in tags_arr if '' != x]
        for tagname in tags_arr:
            tag = Tag.gql('WHERE tag = :1', tagname).get()
            if tag == None:
                tag = Tag(tag=tagname)
                tag.put()
            qtlink = QuestionTagLink(question=question,
                                     tag=tag)
            qtlink.put()
        
        correct_player = Player.gql('WHERE name = :1', correct_txt).get()
        correct_answer = PlayerAnswers(correct=True, player=correct_player, question=question)
        correct_answer.put()
        
        incorrect_players_arr = [x.strip() for x in incorrect_txt.split(',')]
        incorrect_players_arr = [x for x in incorrect_players_arr if '' != x]
        q = Player.gql('WHERE name in :1', incorrect_players_arr)
        for player in q:
            incorrect_answer = PlayerAnswers(correct=False, player=player, question=question)
            incorrect_answer.put()
            
        self.redirect('AddQuestion', False)
        
application = webapp.WSGIApplication([('/[Mm]atch/[Cc]reate', CreateMatch),
                                      ('/[Mm]atch/[Aa]dd[Qq]uestion', NewQuestion)
                                     ], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
