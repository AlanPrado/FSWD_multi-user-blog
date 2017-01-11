import re

from common.request import BlogHandler
from database import User

class SignIn(BlogHandler):
	def render_signin(self, user=None, user_error = "", password_error = ""):
		if user:
			self.login(user)
			self.redirect('/blog')
		else:
			self.render('signin.html', user_error = user_error, password_error = password_error)

	def get(self):
		self.render_signin(self.user)

	def post(self):
		username = self.request.POST['username']
		password = self.request.POST['password']

		user_error = ''
		password_error = ''

		if not username:
			user_error = "User is required"
		if not password:
			password_error = "Password is required"

		if user_error or password_error:
			self.render_signin(user_error = user_error, password_error = password_error)
		else:
			user = User.login(username, password)
			if not user:
				user_error = "Invalid user/password"
			self.render_signin(user, user_error, password_error)

class SignOut(BlogHandler):
	def get(self):
		self.logout()
		self.redirect('/blog/signup')

class SignUp(BlogHandler):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PWD_RE = re.compile(r"^.{3,20}$")
	EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

	def valid_username(self, username):
		if not self.USER_RE.match(username):
			return "That's not a valid username."

	def valid_password(self ,password):
		if not self.PWD_RE.match(password):
			return "That wasn't a valid password."

	def valid_email(self, email):
		if email and not self.EMAIL_RE.match(email):
			return "That's not a valid email."

	def valid_verify(self, p1, p2):
		if p1 != p2:
			return "Your passwords didn't match."

	def verify_already_exists(self, username):
		if User.by_name(username):
			return "User already exists"

	def get(self):
		self.render('signup.html')

	def post(self):
		username = self.request.POST['username']
		password = self.request.POST['password']
		verify = self.request.POST['verify']
		email = self.request.POST['email']

		user_error = self.valid_username(username) or ''
		password_error = self.valid_password(password) or ''
		verify_error = self.valid_verify(password, verify) or ''
		email_error = self.valid_email(email) or ''

		if not user_error:
			user_error = self.verify_already_exists(username) or ''

		if not (user_error or password_error or verify_error or email_error):
			user = User.register(username, password, email)
			self.login(user)
			self.redirect('/blog')
		else:
			self.render('signup.html',	 username = username,
										 email = email,
										 user_error = user_error ,
										 password_error = password_error,
										 verify_error = verify_error,
										 email_error = email_error)
