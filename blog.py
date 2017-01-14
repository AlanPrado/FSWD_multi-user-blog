import webapp2
import os
import sys
import config

config.jinja_env = config.set_templates([
    os.path.join(os.path.dirname(__file__), 'handlers/login/views'),
    os.path.join(os.path.dirname(__file__), 'handlers/views'),
])

from common.request import BlogHandler
from handlers.home import WelcomeHandler, NewPostHandler, PostHandler, EditPostHandler
from handlers.login.login import SignIn, SignUp, SignOut

BlogHandler.login_page = '/blog/signup'

routes = [
	(BlogHandler.login_page, SignUp),
	('/blog/signin', SignIn),
	('/blog/logout', SignOut),
	(r'/blog/?', WelcomeHandler),
    (r'/?', WelcomeHandler),
    ('/blog/newpost', NewPostHandler),
    webapp2.Route('/blog/<post_id:\d+>', PostHandler, name='post_id'),
    webapp2.Route('/blog/edit/<post_id:\d+>', EditPostHandler, name='post_id')
]

app = webapp2.WSGIApplication(routes, debug=True)
