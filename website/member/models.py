import hashlib

from django.db import models
from django.contrib.auth.models import User

def encrypt_password(plain):
    plain = str(plain)
    return hashlib.sha512(plain).hexdigest()

# Create your models here.
"""
class Member(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    level = models.IntegerField(default=0)

    joined = models.DateField(auto_now_add=True)

    def check_password(self, password):
        if not password:
            password = ''
        return self.password == encrypt_password(password)
            
    def change_password(self, password):
        if not password:
            password = ''

        self.password = encrypt_password(password)
"""

class Photo(models.Model):
    pass
    # image = models.ImageField()

class UserProfile(models.Model):

    # member = models.OneToOneField(Member)

    name = models.CharField(max_length=32)
    birthday = models.DateField()
    intro = models.TextField()
    phone = models.CharField(max_length=12)

    user = models.ForeignKey(User, unique=True)
    # photo = models.ForeignKey(Photo, db_column='photo_id')
    

