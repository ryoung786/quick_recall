from flask import Flask, request, render_template, redirect, url_for
from models import Match, MatchFinder, Question, QuestionFinder, Answer, Player, PlayerFinder
import config

class Stats():
    def __init__(self, player_id):
        self.player = PlayerFinder().find(player_id)

    def render(self):
        return render_template("players/player/stats.html",
                               player=self.player)
