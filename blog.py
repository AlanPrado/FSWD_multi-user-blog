import webapp2
import os
import sys
import config

config.jinja_env = config.set_templates([
    os.path.join(os.path.dirname(__file__), 'handlers/login/views'),
    os.path.join(os.path.dirname(__file__), 'handlers/views'),
])

from common.request import BlogHandler
from handlers.home import WelcomeHandler
from handlers.login.login import SignIn, SignUp, SignOut

routes = [
	('/blog/signup', SignUp),
	('/blog/signin', SignIn),
	('/blog/logout', SignOut),
	(r'/blog/?', WelcomeHandler),
    #webapp2.Route('/blog/newpost', BlogPostPage, name='newpost'),
    #webapp2.Route('/blog/<blog_id:\d+>', BlogGetPage, name='blog_id'),
]

app = webapp2.WSGIApplication(routes, debug=True)
