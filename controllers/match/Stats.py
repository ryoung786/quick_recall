from flask import Flask, request, render_template, redirect, url_for
from models import Match, MatchFinder, Question, QuestionFinder, Answer
import config

class Stats():
    def __init__(self, match_id):
        self.match = MatchFinder().find(match_id)

    def render(self):
        return render_template("matches/stats.html",
                               match=self.match)
