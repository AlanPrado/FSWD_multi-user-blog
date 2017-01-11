from common import secure
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = secure.make_pw_hash(name, pw)
        user = cls(name = name,
                    pw_hash = pw_hash,
                    email = email)
        user.put()
        return user

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and secure.valid_pw(name, pw, u.pw_hash):
            return u

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def get_most_recent(cls):
        return db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")

    @classmethod
    def by_id(cls, pid):
        return cls.get_by_id(pid)

    @classmethod
    def register(cls, subject = subject, content = content):
        post = cls(subject = subject,
                   content = content)
        post.put()
        return post
