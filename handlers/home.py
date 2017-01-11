from database import Post
from common.request import BlogHandler, AuthenticatedHandler

class WelcomeHandler(AuthenticatedHandler):
	def get(self):
		posts = Post.get_most_recent()
		self.render('welcome.html', username = self.user.name, posts = posts)
