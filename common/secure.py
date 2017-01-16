"""
    Secure helper features.
"""
import random
import string
import hmac
import hashlib
from config import config

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pwd, salt=None):
    if not salt:
        salt = make_salt()
    shash = hashlib.sha256(name + pwd + salt).hexdigest()
    return '%s|%s' % (shash, salt)

def valid_pw(name, pwd, shash):
    h_split = shash.split('|')

    if len(h_split) == 2:
        salt = h_split[1]
        return make_pw_hash(name, pwd, salt) == shash

    return False

def hash_str(text):
    return hmac.new(config.SECRET, text).hexdigest()

def make_secure_val(text):
    return "%s|%s" % (text, hash_str(text))

def check_secure_val(shash):
    if shash:
        key = shash.split('|')
        if len(key) == 2 and shash == make_secure_val(key[0]):
            return key[0]
