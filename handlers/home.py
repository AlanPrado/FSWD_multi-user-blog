from common.database import Post
from common.request import BlogHandler

class WelcomeHandler(BlogHandler):
	def get(self):
		if self.is_user_authenticated():
			posts = Post.get_most_recent()
			self.render('welcome.html', username = self.user.name, posts = posts)

class NewPostHandler(BlogHandler):
	def render_blog(self, error = "", content = "", subject = ""):
		self.render('newpost.html', error = error, subject = subject, content = content)

	def get(self):
		if self.is_user_authenticated():
			self.render_blog();

	def post(self):
		if self.is_user_authenticated():
			subject = self.request.POST['subject']
			content = self.request.POST['content']

			if subject and content:
				post = Post.register(subject = subject, content = content, author = self.user)
				post_url = "/blog/%s" % post.key().id()
				self.redirect(post_url, permanent = True)
			else:
				error = 'subject and content, please!'
				self.render_blog(error, subject = subject, content = content);

class PostHandler(BlogHandler):
	def get(self, blog_id):
		if self.is_user_authenticated():
			post = Post.by_id(int(blog_id))
	        self.render('blog_detail.html', post = post)
