import webapp2
from config import config
from common.request import BlogHandler, load_templates
from handlers.home import WelcomeHandler, NewPostHandler, PostHandler, EditPostHandler
from handlers.login.login import SignIn, SignUp, SignOut

template_dir = ['handlers/login/views', 'handlers/views']
config.jinja_env = load_templates(__file__, template_dir)
BlogHandler.login_page = '/blog/signup'

routes = [
	(BlogHandler.login_page, SignUp),
	('/blog/signin', SignIn),
	('/blog/logout', SignOut),
	(r'/blog/?', WelcomeHandler),
    (r'/?', WelcomeHandler),
    ('/blog/newpost', NewPostHandler),
    webapp2.Route(r'/blog/<post_id:\d+>', PostHandler, name='post_id'),
    webapp2.Route(r'/blog/edit/<post_id:\d+>', EditPostHandler, name='post_id')
]

app = webapp2.WSGIApplication(routes, debug=True)
