from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):              # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text


class Mn_Name(models.Model):
    mn_name = models.CharField(max_length=20)
    mn_url =  models.CharField(max_length=60)

    def __str__(self):              # __unicode__ on Python 2
        return self.mn_name

class Ma_Part(models.Model):
    ma_id = models.IntegerField(primary_key=True)
    mn_nr = models.CharField(max_length=40)
    mn_desc = models.CharField(max_length=40)
    mn_id = models.ForeignKey(Mn_Name, null=True)

    ma_desc = models.CharField(max_length=60)

    def __unicode__(self):              # __unicode__ on Python 2
        return str(self.ma_id) +': '+ self.ma_desc


class Thing(models.Model):
    ma_id = models.ForeignKey(Ma_Part)
    thing_desc =  models.CharField(max_length=60)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.ma_id) +': '+ self.thing_desc


class Part(models.Model):
    thing = models.ForeignKey(Thing)
    ma_id = models.ForeignKey(Ma_Part, default=0)
    part_desc =  models.CharField(max_length=60)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.ma_id) +': '+ self.part_desc