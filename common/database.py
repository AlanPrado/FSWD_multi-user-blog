from common import secure
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)

    @classmethod
    def by_name(cls, name):
        user = cls.all().filter('name =', name).get()
        return user

    @classmethod
    def register(cls, name, pwd, email=None):
        pw_hash = secure.make_pw_hash(name, pwd)
        user = cls(name=name,
                   pw_hash=pw_hash,
                   email=email)
        user.put()
        return user

    @classmethod
    def login(cls, name, pwd):
        user = cls.by_name(name)
        if user and secure.valid_pw(name, pwd, user.pw_hash):
            return user

class Post(db.Model):
    subject = db.StringProperty(required=True)
    author = db.ReferenceProperty(User)
    likes = db.ListProperty(db.Key)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def get_most_recent(cls):
        #return db.GqlQuery("SELECT * FROM %s ORDER BY created DESC LIMIT 10" % cls.__name__)
        return cls.all().order("-created").run(limit=10)

    @classmethod
    def by_id(cls, pid):
        return cls.get_by_id(pid)

    @classmethod
    def register(cls, subject, content, author):
        post = cls(subject=subject,
                   content=content,
                   author=author)
        post.put()
        return post

    def user_liked(self, user_key):
        if user_key in self.likes:
            return True
        else:
            return False


    def toogle_like(self, user):
        user_key = user.key()

        if self.user_liked(user_key):
            self.likes.remove(user_key)
        else:
            self.likes.append(user_key)

        self.put()

    def update(self, subject, content):
        self.subject = subject
        self.content = content
        self.put()
