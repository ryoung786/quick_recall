from flask import Flask, request, render_template, redirect, url_for
from pymongo import Connection
from pymongo.objectid import ObjectId
from util import *
from config import config as cfg
from models import Match, MatchFinder, Question, QuestionFinder, Answer
import controllers
import f_controllers
import f_models

app = Flask(__name__)

@app.route('/matches/', methods=['POST'])
def createMatch():
    match_id = Match().save()
    return redirect(url_for('match', match_id=str(match_id)))

@app.route('/players/', methods=['POST'])
def createPlayer():
    player = Player(request.form['first'], request.form['last'])
    player_id = player.save()
    return 'Created'

@app.route('/matches/<match_id>/')
def match(match_id):
    match = MatchFinder().find(match_id)
    return render_template(
        "in_game.html",
        teams=match.Teams(populate_players=True))

@app.route('/matches/<match_id>/questions', methods=['POST'])
def createQuestion(match_id):
    player_id = request.form['player_id']
    correct = request.form['correct'] == '1'
    tags = request.form.getlist('tags[]')

    answer = Answer(player_id, correct)
    question = Question(tags, answers=[answer.asJSON()])
    question.save()

    match = MatchFinder().find(match_id)
    match.addQuestionAndAnswer(question, answer)
    return "OK " + str(question._id)

@app.route('/matches/<match_id>/questions/<question_id>/answers', methods=['POST'])
def addAnswer(match_id, question_id):
    question = QuestionFinder().find(question_id)
    player_id = request.form['player_id']
    correct = 'correct' in request.form
    question.addAnswer(Answer(player_id, correct))

@app.route('/matches/<match_id>/stats/')
def matchStats(match_id):
    return f_controllers.match.stats.render(match_id)

@app.route('/players/<player_id>/stats/')
def playerStats(player_id):
    return f_controllers.players.stats.render(player_id)

@app.route('/')
def helloWorld():
    return "<a href='matches/4f5ae40867a69c1f6bf97677'>first match</a>"



if __name__ == '__main__':
    if cfg['production']:
        app.run(host='0.0.0.0', port=80, debug=False)
    else:
        app.run(debug=True)
