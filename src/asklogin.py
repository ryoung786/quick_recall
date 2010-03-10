from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Player

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        user = users.get_current_user()

        if user:
            q = db.GqlQuery("SELECT * FROM Player WHERE user = :1", user)
            player = q.get()
            if player:
                self.response.out.write("Found a Player: %s" % player.user.nickname())
            else:
                player = Player(user=user)
                player.put()
                self.response.out.write(
                    'Hello woo %s <a href="%s">Sign out</a><br>Is administrator: %s' % 
                    (user.nickname(), users.create_logout_url("/"), users.is_current_user_admin())
                )
        else:
            self.redirect(users.create_login_url(self.request.uri))


application = webapp.WSGIApplication([('/', MainPage)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
