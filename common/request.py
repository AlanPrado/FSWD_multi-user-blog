"""
    This module has common features for webapp2 handlers.
    Manages the user session and provide jinja templates
    for subclasses.
"""
import os
import webapp2
from config import config
from common import secure
from common.database import User
from jinja2 import Environment
from jinja2 import FileSystemLoader

def load_templates(path, template_dir):
    """
        Load template helper function.
        Based on the file path, configure
        templates for each item in template_dir.
    """
    files = []
    for template in template_dir:
        files.append(os.path.join(os.path.dirname(path), template))

    return Environment(loader=FileSystemLoader(files), autoescape=True)

class Page(object):
    """
        Page object used to create
        a navigation component.
    """
    def __init__(self, label, url):
        self.label = label
        self.url = url

    def get_label(self):
        """ get label """
        return self.label

    def get_url(self):
        """ get url """
        return self.url

class BlogHandler(webapp2.RequestHandler):
    """
        Provide the user logged based on the cookie session.
        Enable subclasses to use jinja templates.
        Also provide a mechanism to use cookie values in
        a secure way.
    """
    login_page = "login"

    def write(self, *a, **kw):
        """ write a http response """
        self.response.write(*a, **kw)

    def render(self, template, **kw):
        """ render a template to http response """
        page = config.jinja_env.get_template(template)
        response = page.render(**kw)
        self.write(response)

    def set_cookie(self, name, val, path="Path=/"):
        """ set a cookie keypair name/val """
        cookie = '%s=%s; %s' % (name, val, path)
        self.response.headers.add_header('Set-Cookie', cookie)

    def read_cookie(self, name):
        """ read a cookie """
        cookies = hasattr(self.request, 'cookies')
        return cookies and self.request.cookies.get(name)

    def set_secure_cookie(self, name, val):
        """
            set a cookie keypair name/val
            with a hash
        """
        cookie_val = secure.make_secure_val(val)
        self.set_cookie(name, cookie_val)

    def read_secure_cookie(self, name):
        """ read a cookie with a hash """
        cookie_val = self.read_cookie(name)
        return cookie_val and secure.check_secure_val(cookie_val)

    def login(self, user):
        """ creates session cookie """
        user_id = str(user.key().id())
        self.set_secure_cookie('user_id', user_id)

    def logout(self):
        """ remove session cookie """
        self.set_cookie('user_id', '')

    def initialize(self, *a, **kw):
        """ add the logged in user """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def get_page_stack(self):
        """
            Stack of current page label and url.
            Used to create a navigation component.
        """
        return [Page(label='Home', url='/')]

    def is_user_authenticated(self):
        """
            Checks if the user is authenticated,
            otherwise redirects to login page
        """
        if self.user:
            return True
        else:
            self.redirect(self.login_page, permanent=True)
