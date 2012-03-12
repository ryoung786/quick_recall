from flask import Flask, request, render_template, redirect, url_for
from pymongo import Connection
from pymongo.objectid import ObjectId
from util import *
from config import config as cfg
from models import Match, MatchFinder, Question

app = Flask(__name__)
conn = Connection(cfg['DB']['host'], cfg['DB']['port'])
db = conn.foo

@app.route('/matches/', methods=['POST'])
def createMatch():
    match_id = Match().save()
    # watch out, the below url_for doesn't work
    # TODO figure it out
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
    correct = 'correct' in request.form
    tags = request.form.getlist('tags')
    question_id = Question(player_id, correct, tags).save()

    match = MatchFinder().find(match_id)
    match.addQuestion(question_id)
    return redirect(url_for('match', match_id=str(match_id)))

@app.route('/matches/<match_id>/stats/')
def matchStats(match_id):
    match = MatchFinder().find(match_id)
    return render_template("matches/stats.html",
                           match=match)

@app.route('/')
def helloWorld():
    return "<a href='matches/4f5ae40867a69c1f6bf97677'>first match</a>"



if __name__ == '__main__':
    if cfg['production']:
        app.run(host='0.0.0.0', port=80, debug=False)
    else:
        app.run(debug=True)
