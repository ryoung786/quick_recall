from flask import Flask, request, render_template, redirect, url_for
from pymongo import Connection
from pymongo.objectid import ObjectId
from util import *
from config import config as cfg
from models import Match, MatchFinder

app = Flask(__name__)
conn = Connection(cfg['DB']['host'], cfg['DB']['port'])
db = conn.foo

@app.route('/matches/', methods=['POST'])
def createMatch():
    foo = request.form['foo']
    match = {
        'official': False,
        'questions': [],
        'teams': []
    }
    match = db.matches.save(match)

    # watch out, the below url_for doesn't work
    # TODO figure it out
    return redirect(url_for('matches', match_id=str(match._id)))

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
    question = {
        'player_id': ObjectId(player_id),
        'correct': correct,
        'tags': tags
    }
    question_id = db.questions.save(question)

    match = db.matches.find_one({"_id": ObjectId(match_id)})
    match['questions'] = match['questions'] + [question_id]
    db.matches.save(match)
    return redirect('/matches/' + match_id)

@app.route('/matches/<match_id>/stats/')
def matchStats(match_id):
    match = db.matches.find_one({"_id": ObjectId(match_id)})
    populateMatch(match, db)
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
