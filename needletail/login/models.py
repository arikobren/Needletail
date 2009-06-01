from django.db      import models
from django.contrib import admin

from django.contrib.auth.models import User

class Band(models.Model):
    name     = models.CharField(max_length = 500)
    genre    = models.CharField(max_length = 50 ) 
    location = models.CharField(max_length = 200)
    bio      = models.CharField()


class User_Profile(models.Model):
    user  = models.OneToOneField(User)
    bands = models.ManyToManyField(Band) 


admin.site.register(Band)

