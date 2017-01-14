from common.database import Post
from common.request import BlogHandler, Page
import json

class WelcomeHandler(BlogHandler):
	def get_page_stack(self):
		return [Page(label = 'Home', url = '/blog')]

	def get(self):
		if self.is_user_authenticated():
			posts = Post.get_most_recent()
			self.render('welcome.html', page = self, posts = posts)

class NewPostHandler(WelcomeHandler):
	def get_page_stack(self):
		pages = super(NewPostHandler, self).get_page_stack()
		pages.append(Page(label = 'New Post', url = '/blog/newpost'))
		return pages

	def render_blog(self, error = "", content = "", subject = ""):
		self.render('newpost.html', page = self, error = error, subject = subject, content = content)

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
				self.render_blog(error = error, subject = subject, content = content);

class PostHandler(WelcomeHandler):
	def get_page_stack(self):
		pages = super(PostHandler, self).get_page_stack()
		pages.append(Page(label = 'Post detail', url = '/blog/%s' % self.post_id))
		return pages

	def get(self, post_id):
		if self.is_user_authenticated():
			self.post_id = post_id
			post = Post.by_id(int(post_id))
			if not post:
				self.redirect("/blog", permanent = True)
			else:
				self.render('blog_detail.html', page = self, post = post)

	def delete(self, post_id):
		if self.is_user_authenticated():
			post = Post.by_id(int(post_id))

			if post:
				self.write(json.dumps({"message": "Post already removed!"}))
			elif post.author.key().id() == self.user.key().id():
				post.delete()
				self.write(json.dumps({"message": "Post removed!"}))
			else:
				self.response.set_status(401)
				self.write("Remove other people posts is not allowed.")
