from django.db import models
from django.contrib.auth.models import User
import base64
import datetime
import string

ALPHABET = string.ascii_lowercase + string.digits 
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
SIGN_CHARACTER = '$'

def num_encode(n):
    if n < 0:
        return SIGN_CHARACTER + num_encode(-n)
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0: break
    return ''.join(reversed(s))

def num_decode(s):
    if s[0] == SIGN_CHARACTER:
        return -num_decode(s[1:])
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n



class Pledge(models.Model):
    user = models.ForeignKey(User, db_index=True)
    party = models.CharField(max_length=40, db_index=True)
    code = models.CharField(max_length=40, db_index=True)
    created_at = models.DateTimeField(null=True, db_index=True, auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, db_index=True)
    verified_by = models.ForeignKey(User, null=True, db_index=True, related_name='verifier')
    
    @classmethod
    def user_create(cls, user, party):
        pledge = cls.get_user_pledge(user)
        if pledge:
            return pledge
        pledge = cls(user=user, party=party, code='')
        pledge.save()
        # turn the id into a base64 code, and save it
        pledge.code = num_encode(pledge.id)
        pledge.save()
        return pledge
    
    @classmethod
    def get_user_pledge(cls, user):
        try:
            pledge = cls.objects.filter(user=user)[0]
            return pledge
        except:
            return None

    @classmethod
    def get_by_code(cls, code):
        try:
            pledge = cls.objects.filter(code=code)[0]
            return pledge
        except:
            return None
    
    @classmethod
    def verify(cls, user, code):
        pledge = cls.get_by_code(code)
        if not pledge:
            return None
        if pledge.user == user:
            return None
        pledge.verified = True
        pledge.verified_at = datetime.datetime.now()
        pledge.verified_by = user
        pledge.save()
        return pledge
    
    def __str__(self):
        if self.verified:
            return "{}, {}, verified by: {}".format(self.user.email, self.party, self.verified_by.email)
        else:
            return "{}, {}, not verified".format(self.user.email, self.party)