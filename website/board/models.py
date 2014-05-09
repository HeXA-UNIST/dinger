import datetime
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

	def written_today(self):
		written = tuple(self.written.timetuple())[0:3]
		today = tuple(datetime.date.today().timetuple())[0:3]

		return written == today


class Comment(models.Model):
	content = models.CharField(max_length=140)
	written = models.DateTimeField(auto_now_add=True)

	article = models.ForeignKey(Article)
	author = models.ForeignKey(User)
	

class CommentInComment(models.Model):
	pass

class Likes(models.Model):
	when = models.DateTimeField(auto_now=True)
	who = models.ForeignKey(User)
	what = models.ForeignKey(Article)
