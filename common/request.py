import os
import webapp2
from config import config
from common import secure
from common.database import User
from jinja2 import Environment
from jinja2 import FileSystemLoader

def load_templates(path, template_dir):
    files = []
    for template in template_dir:
        files.append(os.path.join(os.path.dirname(path), template))

    return Environment(loader=FileSystemLoader(files), autoescape=True)

class Page(object):
    def __init__(self, label, url):
        self.label = label
        self.url = url

    def get_label(self):
        return self.label

    def get_url(self):
        return self.url

class BlogHandler(webapp2.RequestHandler):
    login_page = "login"

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        page = config.jinja_env.get_template(template)
        return page.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, name, val, path="Path=/"):
        cookie = '%s=%s; %s' % (name, val, path)
        self.response.headers.add_header('Set-Cookie', cookie)

    def read_cookie(self, name):
        return hasattr(self.request, 'cookies') and self.request.cookies.get(name)

    def set_secure_cookie(self, name, val):
        cookie_val = secure.make_secure_val(val)
        self.set_cookie(name, cookie_val)

    def read_secure_cookie(self, name):
        cookie_val = self.read_cookie(name)
        return cookie_val and secure.check_secure_val(cookie_val)

    def login(self, user):
        user_id = str(user.key().id())
        self.set_secure_cookie('user_id', user_id)

    def logout(self):
        self.set_cookie('user_id', '')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def get_page_stack(self):
        return [Page(label='Home', url='/')]

    def is_user_authenticated(self):
        if self.user:
            return True
        else:
            self.redirect(self.login_page, permanent=True)
