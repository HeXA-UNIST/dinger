import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=128)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
class PhotoDetail(models.Model):
    file = models.ImageField(upload_to='photos/')
    width = models.IntegerField()
    height = models.IntegerField()
    
class Photo(models.Model):
    caption = models.CharField(max_length=128)
    uuid = models.BigIntegerField()
    details = models.OneToOneField(PhotoDetail)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    album = models.ForeignKey(Album, null=True)
    author = models.ForeignKey(User)
    