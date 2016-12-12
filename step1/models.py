from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15)
    nickname = models.CharField(max_length=20)    
    password = models.CharField(max_length=20)
    age      = models.IntegerField()
    sex      = models.BooleanField()    
    
    def __unicode__(self):
        return self.username
        

class Act(models.Model):
    actname = models.CharField(max_length=15)
    actdate = models.DateField()
    location= models.CharField(max_length=100)
    before  = models.BooleanField()
    budget  = models.FloatField()
    cost    = models.FloatField()
    recive  = models.FloatField(default=0.0)
    owner   = models.IntegerField()
    partner = models.ManyToManyField(User)
    able    = models.BooleanField(default=True)
    accept  = models.ManyToManyField(User,related_name='accept_acts')
    
    def __unicode__(self):
        return self.actname
        
        
        
    