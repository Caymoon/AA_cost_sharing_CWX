from __future__ import unicode_literals

from django.db import models

<<<<<<< HEAD

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
=======
>>>>>>> 54f479e04df4510eab85bffd66fffe40d274ff2b
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=15)
    nickname = models.CharField(max_length=20)    
    password = models.CharField(max_length=20)
    age      = models.IntegerField()
    sex      = models.BooleanField()    
<<<<<<< HEAD
    avatar   = models.ImageField(upload_to='avatars/',default='avatars/huaji2')
    mnum     = models.IntegerField(default=0)
    def __unicode__(self):
        return self.username
=======
    
    def __unicode__(self):
        return self.username
        
>>>>>>> 54f479e04df4510eab85bffd66fffe40d274ff2b

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
<<<<<<< HEAD
    twp     = models.ManyToManyField(User,related_name='twp_acts')
    status  = models.IntegerField(default=0)
    tp      = models.IntegerField(default=0)
    p1      = models.IntegerField(default=0)
    p2      = models.IntegerField(default=0)
    p3      = models.IntegerField(default=0)
    p4      = models.IntegerField(default=0)
    p5      = models.IntegerField(default=0)
    fin     = models.ManyToManyField(User,related_name='fin_acts')
    def __unicode__(self):
        return self.actname
=======
    
    def __unicode__(self):
        return self.actname
        
        
        
>>>>>>> 54f479e04df4510eab85bffd66fffe40d274ff2b
    