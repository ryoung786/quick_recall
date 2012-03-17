from flask import Flask, request, render_template, redirect, url_for
from models import Match, MatchFinder, Question, QuestionFinder, Answer
import config

class Stats():
    def render(self, match_id):
        match = MatchFinder().find(match_id)
        return render_template("matches/stats.html",
                               match=match)
