from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Table(models.Model):
    currentplayer = models.IntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=100)
    username= models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    balance = models.IntegerField()
    picture = models.CharField(max_length=100)
    table = models.ForeignKey(Table, blank=True, null=True)
