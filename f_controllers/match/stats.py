import config
from flask import render_template, redirect

def render(match_id):
    return render_template("f/matches/stats.html",
                           match=self.match)
    # return "Match Stats OK"
