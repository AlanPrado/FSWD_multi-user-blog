import random
import string
import hmac
import hashlib
from config import SECRET

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=None):
    if not(salt):
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(name, pw, h):
    h_split = h.split('|')

    if len(h_split) == 2:
        salt = h_split[1]
        return make_pw_hash(name, pw, salt) == h

    return False

def hash_str(s):
    return hmac.new(SECRET , s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    if h:
       k = h.split('|')
       if len(k) == 2 and h == make_secure_val(k[0]):
           return k[0]
