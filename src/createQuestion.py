'''
Created on Feb 13, 2010

@author: ryan
'''
import cgi, os, models
from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from models import Question, Answer, Player, PlayerAnswers, Tag, QuestionTagLink 

class CreateQuestion(webapp.RequestHandler):
    
    
    def get(self):
        self.response.out.write('''
        <html>
            <body>
                <form action="/questions/created" method="post">
                    <div><textarea name="question" rows="3" cols="60"></textarea></div>
                    <div><textarea name="answer" rows="3" cols="60"></textarea></div>
                    <div><textarea name="tags" rows="1" cols="60"></textarea></div>
                    <div><input type="submit" value="Create"></div>
              </form>
            </body>
        </html>
        ''')
        
class CreatedQuestion(webapp.RequestHandler):
    def post(self):
        question_txt = cgi.escape(self.request.get('question'))
        answer_txt = cgi.escape(self.request.get('answer'))
        tags_txt = cgi.escape(self.request.get('tags'))
                
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
            
        self.response.out.write('Created!')
        
class GetQuestions(webapp.RequestHandler):
    def get(self):
        template_values = {
            'questions': Question.all().fetch(10) 
                           }        
        path = os.path.join(os.path.dirname(__file__), 'questions.html')
        self.response.out.write(template.render(path, template_values))
        
class GetQuestionsByTag(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
        <html>
            <body>
                <p>Get all questions tagged with:</p>
                <form action="/questions/ByTag" method="post">
                    <div><textarea name="tag" rows="1" cols="60"></textarea></div>
                    <div><input type="submit" value="Get Questions"></div>
              </form>
            </body>
        </html>
        ''')
        
    def post(self):
            tag = cgi.escape(self.request.get('tag'))
            
            template_values = {
                'questions': models.getQuestionsWithTag(tag) 
            }
            path = os.path.join(os.path.dirname(__file__), 'questions.html')
            self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/[Qq]uestions/[Cc]reate', CreateQuestion),
                                      ('/[Qq]uestions/[Cc]reated', CreatedQuestion),
                                      ('/[Qq]uestions/[Bb]y[Tt]ag', GetQuestionsByTag),
                                      ('/[Qq]uestions/[Aa]ll', GetQuestions)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
