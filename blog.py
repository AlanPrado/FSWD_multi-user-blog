import webapp2
import os
import sys
import config

config.jinja_env = config.set_templates([
    os.path.join(os.path.dirname(__file__), 'handlers/login/views'),
    os.path.join(os.path.dirname(__file__), 'handlers/views'),
])

from common.request import BlogHandler
from handlers.home import WelcomeHandler, NewPostHandler, PostHandler
from handlers.login.login import SignIn, SignUp, SignOut

BlogHandler.login_page = '/blog/signup'

routes = [
	(BlogHandler.login_page, SignUp),
	('/blog/signin', SignIn),
	('/blog/logout', SignOut),
	(r'/blog/?', WelcomeHandler),
    (r'/?', WelcomeHandler),
    webapp2.Route('/blog/newpost', NewPostHandler, name='newpost'),
    webapp2.Route('/blog/<blog_id:\d+>', PostHandler, name='blog_id')
]

app = webapp2.WSGIApplication(routes, debug=True)
