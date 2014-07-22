import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=32, unique=True)

    readable = models.IntegerField()
    writable = models.IntegerField()

class Article(models.Model):
    subject = models.CharField(max_length=256)
    content = models.TextField()
    private = models.BooleanField()
    hit = models.IntegerField(default=0)
    written = models.DateTimeField(auto_now_add=True)

    board = models.ForeignKey(Board)
    author = models.ForeignKey(User)

    liked_by = models.ManyToManyField(User, related_name='likes')

    def written_today(self):
        written = tuple(self.written.timetuple())[0:3]
        today = tuple(datetime.date.today().timetuple())[0:3]

        return written == today

    def is_liked_by(self, user):
        ###! the following code is not efficiently, so we need better one.
        return self in user.likes.all()

class Comment(models.Model):
    content = models.CharField(max_length=140)
    written = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey(Article)
    author = models.ForeignKey(User)
    

class Attachment(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachement/')
    article = models.OneToOneField(Article)
    uploaded = models.DateTimeField(auto_now_add=True)