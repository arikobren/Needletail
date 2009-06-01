from django.db      import models
from django.contrib import admin

from django.contrib.auth.models import User

class Band(models.Model):
    name = models.CharField(max_length = 500)

#class Band_Member(models.Model):
#    first     = models.CharField( max_length = 100)
#    last      = models.CharField( max_length = 100)
#    username  = models.CharField( max_length = 100)
#    password  = models.CharField( max_length = 100)
#    email     = models.EmailField(max_length = 100)
#    bands     = models.ManyToManyField(Band)
    

class User_Profile(models.Model):
    user  = models.OneToOneField(User)
    bands = models.ManyToManyField(Band) 


admin.site.register(Band)
#admin.site.register(Band_Member)
